"""A live unlabeled-query -> labeled-learning stream with readiness waiting."""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT/'results/otb19_learning_readiness_guard/main'
LOCAL = ROOT/'.cache/oscillator-night-pydeps'
if LOCAL.exists():
    sys.path.insert(0, str(LOCAL))
# Dynamically imported frozen kernels need a study-local cache namespace; an
# earlier generic module name such as `model` may be embedded in shared caches.
os.environ['NUMBA_CACHE_DIR'] = str(ROOT/'.cache/otb19-numba')
from numba import njit


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


L = module(ROOT/'experiments/otb15_local_error_learning/model.py', 'otb19_original_learning')
Q = module(ROOT/'experiments/otb17_learning_readiness/model.py', 'otb19_query')
SEEDS = tuple(range(24001,24009))
POLICIES = ('usual', 'guard', 'fixed_once', 'zero_error')
EPISODES = 4
HCRIT = 2/(3*np.sqrt(3))


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, default=json_default)
        stream.write('\n')


def json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f'Cannot encode {type(value).__name__}')


def noncurrent(pair):
    return np.array([i for i in range(8) if i//2 != pair], dtype=int)


def bound(mem, pair, config):
    cells = noncurrent(pair)
    max_e = float(np.max(mem[cells,5]))
    max_s = float(np.max(np.abs(mem[cells,6])))
    return dict(max_e=max_e, max_abs_s=max_s,
                tilt_bound=float(config['hold_eta']+config['alpha']*max(max_e,max_s)))


def required_wait(mem, pair, theta, config):
    state = bound(mem,pair,config)
    e, s = state['max_e'], state['max_abs_s']
    ne = max(0, int(math.ceil(config['tau_e']*math.log(e/theta)))) if e > theta else 0
    ns = max(0, int(math.ceil(math.log(s/theta)/(-math.log1p(-1/config['tau_s']))))) if s > theta else 0
    return max(ne,ns)


@njit(cache=False)
def work_restoration(work, steps):
    """Read-only effort monitor, independently reproducing query=False work."""
    w = work.copy()
    effort = 0.
    for _ in range(steps):
        for j in range(3):
            m,p,cd = w[j,:3]
            prep = .01*(-1.2-m)
            effort += abs(prep)
            pn = p+2*np.pi/258+.025*m
            fired = pn >= 2*np.pi and cd == 0
            drive = 6.5e-5*(-1.2)+prep
            w[j,0] = (1-6.5e-5)*m+drive-.6*int(fired)
            w[j,1] = 0. if fired else pn%(2*np.pi)
            w[j,2] = 512 if fired else max(cd-1,0)
            w[j,3] = 1. if fired else 0.
    return w,effort


def canonical_probes(mem, config):
    work = np.zeros((3,4))
    work[:,0] = -1.2
    work[:,1] = np.arange(3)*2*np.pi/3
    data = Q.query_batch(np.repeat(mem[None],4,axis=0),np.repeat(work[None],4,axis=0),
                         np.arange(4),4096,np.full(4,128),np.full(4,.01),np.ones((4,3),bool),config=config)
    return dict(predictions=data['pred'].tolist(),counts=data['counts'].tolist(),
                first=data['first'].tolist(),bands=Q.memory_bands(mem).tolist())


def unchanged_cells(initial_mem, current_mem, cells):
    return bool(np.array_equal(Q.memory_bands(initial_mem)[cells],Q.memory_bands(current_mem)[cells]))


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    config = load(ROOT/'experiments/otb15_local_error_learning/MAIN_CONFIG.json')['base']
    assert config['tau_s'] >= 1 and config['hold_eta'] < HCRIT and config['alpha'] > 0
    theta = .95*(HCRIT-config['hold_eta'])/config['alpha']
    fixed_steps = max(int(math.ceil(config['tau_e']*math.log(1/theta))),
                      int(math.ceil(math.log(1/theta)/(-math.log1p(-1/config['tau_s'])))))
    paths = [HERE/'DESIGN.md',HERE/'run.py',
             ROOT/'experiments/otb15_local_error_learning/model.py',
             ROOT/'experiments/otb15_local_error_learning/MAIN_CONFIG.json',
             ROOT/'experiments/otb17_learning_readiness/model.py']
    paths += [ROOT/f'results/otb15_local_error_learning/main_runs/normal_{s}.json' for s in SEEDS]
    hashes = {p.relative_to(ROOT).as_posix():sha(p) for p in paths}
    OUT.mkdir(parents=True)
    (OUT/'traces').mkdir()
    for p in paths:
        dest = OUT/'source_snapshot'/p.relative_to(ROOT)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(p.read_bytes())
    dump(OUT/'source_freeze.json',dict(kind='exploratory_live_stream_stress_test',
        frozen_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),hashes=hashes,
        seeds=SEEDS,old_pairs=[2,3],current_pairs=[0,1],worlds=['stable','reversed'],
        policies=POLICIES,episodes=EPISODES,config=config,theta=theta,hcrit=HCRIT,
        conservative_fixed_wait_once=fixed_steps,live_state_resets=False,
        probes_return_to_learner=False))
    records=[]
    state_records=[]
    trace_checks=[]
    begin=time.perf_counter()
    for seed in SEEDS:
        saved=load(ROOT/f'results/otb15_local_error_learning/main_runs/normal_{seed}.json')
        initial_mem=np.array(saved['stage_states']['retained']['mem'])
        initial_work=np.array(saved['stage_states']['retained']['work'])
        initial_bands=Q.memory_bands(initial_mem)
        assert np.all(initial_bands != 0)
        assert np.all((initial_mem[:,5]>=0)&(initial_mem[:,5]<=1)) and np.max(np.abs(initial_mem[:,6]))<=1
        old_truth=np.array([(p%2)^saved['initial_flips'][p//2] for p in range(4)])
        initial_probe=canonical_probes(initial_mem,config)
        for old_pair in (2,3):
            oldquery=Q.query(initial_mem,initial_work,old_pair,4096,128,.01,config=config)
            post_old_mem=oldquery['final_mem'];post_old_work=oldquery['final_work']
            post_old_probe=canonical_probes(post_old_mem,config)
            for current_pair in (0,1):
                cells=noncurrent(current_pair)
                for reverse in (False,True):
                    truth=old_truth.copy()
                    if reverse:truth[:2]^=1
                    for policy in POLICIES:
                        lane=len(records)
                        mem,work=post_old_mem.copy(),post_old_work.copy()
                        lane_record=dict(lane=lane,seed=seed,old_pair=old_pair,current_pair=current_pair,
                            world='reversed' if reverse else 'stable',policy=policy,
                            initial_truth=old_truth.tolist(),world_truth=truth.tolist(),
                            old_prediction=oldquery['pred'],old_counts=oldquery['counts'].tolist(),
                            initial_probe=initial_probe,post_old_probe=post_old_probe,episodes=[])
                        lane_states=dict(initial_mem=initial_mem.copy(),initial_work=initial_work.copy(),
                            post_old_mem=post_old_mem.copy(),post_old_work=post_old_work.copy(),
                            pre_wait_mem=[],pre_wait_work=[],post_wait_mem=[],post_wait_work=[],
                            post_query_mem=[],post_query_work=[],post_write_mem=[],post_write_work=[])
                        for ep in range(EPISODES):
                            trace_lane=(seed==SEEDS[0] and old_pair==2 and current_pair==1 and reverse
                                        and policy in ('usual','guard') and ep==0)
                            lane_states['pre_wait_mem'].append(mem.copy());lane_states['pre_wait_work'].append(work.copy())
                            before_wait=bound(mem,current_pair,config)
                            wait=(required_wait(mem,current_pair,theta,config) if policy=='guard'
                                  else fixed_steps if policy=='fixed_once' and ep==0 else 0)
                            wait_initial_work=work.copy()
                            if wait:
                                _,_,wait_trace=L.advance(mem,work,wait,config,record=trace_lane)
                            else:wait_trace=np.empty((0,82))
                            expected_work,wait_effort=work_restoration(wait_initial_work,wait)
                            assert np.max(np.abs(expected_work-work)) < 1e-12
                            after_wait=bound(mem,current_pair,config)
                            if policy in ('guard','fixed_once'):
                                assert after_wait['max_e'] <= theta*(1+1e-12)
                                assert after_wait['max_abs_s'] <= theta*(1+1e-12)
                                assert after_wait['tilt_bound'] < HCRIT
                                assert unchanged_cells(initial_mem,mem,cells)
                            lane_states['post_wait_mem'].append(mem.copy());lane_states['post_wait_work'].append(work.copy())
                            current=Q.query(mem,work,current_pair,4096,128,.01,config=config,record=trace_lane)
                            mem,work=current['final_mem'],current['final_work']
                            lane_states['post_query_mem'].append(mem.copy());lane_states['post_query_work'].append(work.copy())
                            before_write=bound(mem,current_pair,config)
                            feedback_initial_work=work.copy()
                            delta,_,delay_trace,write_trace=L.observe(mem,work,current['pred'],int(truth[current_pair]),
                                config,mode='zero_error' if policy=='zero_error' else 'normal',record=trace_lane)
                            assert np.max(np.abs(delta)) <= 1
                            expected_work,feedback_effort=work_restoration(feedback_initial_work,config['delay_steps']+config['write_steps'])
                            assert np.max(np.abs(expected_work-work)) < 1e-12
                            lane_states['post_write_mem'].append(mem.copy());lane_states['post_write_work'].append(work.copy())
                            probe=canonical_probes(mem,config)
                            protected=unchanged_cells(initial_mem,mem,cells)
                            untouched=unchanged_cells(initial_mem,mem,np.arange(4,8))
                            if policy in ('guard','fixed_once'):
                                assert before_write['tilt_bound'] < HCRIT and protected
                            entry=dict(episode=ep+1,wait_steps=wait,wait_effort=float(wait_effort),
                                query_effort=current['effort'],feedback_effort=float(feedback_effort),
                                query_steps=4096,feedback_steps=config['delay_steps']+config['write_steps'],
                                before_wait=before_wait,after_wait=after_wait,before_write=before_write,
                                actual_prediction=current['pred'],actual_counts=current['counts'].tolist(),
                                actual_first=current['first'].tolist(),outcome=int(truth[current_pair]),delta=delta.tolist(),
                                canonical_probe=probe,current_context_correct=probe['predictions'][current_pair]==truth[current_pair],
                                untouched_operation1_correct=all(probe['predictions'][p]==truth[p] for p in (2,3)),
                                untouched_operation1_bands_preserved=untouched,
                                all_noncurrent_bands_preserved=protected,
                                unobserved_operation0_prediction=probe['predictions'][1-current_pair],
                                unobserved_operation0_world_answer=int(truth[1-current_pair]))
                            lane_record['episodes'].append(entry)
                            if trace_lane:
                                name=f'lane{lane}_episode1.npz'
                                np.savez_compressed(OUT/'traces'/name,wait=wait_trace,query=current['trace'],
                                    delay=delay_trace,write=write_trace,noncurrent=cells,initial_bands=initial_bands)
                                all_trace=np.concatenate([wait_trace,current['trace'],delay_trace,write_trace])
                                ub=all_trace[:,:56].reshape(-1,8,7)[:,:,3]
                                observed_bands=np.where(ub<=Q.LOW,-1,np.where(ub>=Q.HIGH,1,0))
                                max_tilt=float(np.max(np.abs(all_trace[:,68:76][:,cells])))
                                preserved=bool((observed_bands[:,cells]==initial_bands[cells]).all())
                                if policy=='guard':assert max_tilt < HCRIT and preserved
                                trace_checks.append(dict(file=name,lane=lane,policy=policy,native_steps=len(all_trace),
                                    noncurrent_max_abs_tilt=max_tilt,noncurrent_bands_preserved_every_step=preserved))
                        records.append(lane_record)
                        state_records.append({k:np.asarray(v) for k,v in lane_states.items()})
        print(f'OTB19 seed={seed} lanes={len(records)}',flush=True)
    assert len(records)==256
    dump(OUT/'records.json',records)
    np.savez_compressed(OUT/'states.npz',**{k:np.stack([r[k] for r in state_records]) for k in state_records[0]})
    by_group={}
    for world in ('stable','reversed'):
        for policy in POLICIES:
            chosen=[r for r in records if r['world']==world and r['policy']==policy]
            summary=dict(lanes=len(chosen),episodes={})
            for ep in range(EPISODES):
                es=[r['episodes'][ep] for r in chosen]
                summary['episodes'][str(ep+1)]=dict(
                    current_context_correct=sum(x['current_context_correct'] for x in es),
                    untouched_operation1_correct=sum(x['untouched_operation1_correct'] for x in es),
                    untouched_operation1_bands_preserved=sum(x['untouched_operation1_bands_preserved'] for x in es),
                    all_noncurrent_bands_preserved=sum(x['all_noncurrent_bands_preserved'] for x in es),
                    wait_steps_total=sum(x['wait_steps'] for x in es),
                    wait_steps_mean=float(np.mean([x['wait_steps'] for x in es])),
                    max_noncurrent_tilt_bound_before_write=max(x['before_write']['tilt_bound'] for x in es))
            summary['total_wait_steps']=sum(e['wait_steps'] for r in chosen for e in r['episodes'])
            summary['total_preparation_current']=sum(e['wait_effort']+e['query_effort']+e['feedback_effort'] for r in chosen for e in r['episodes'])
            by_group[f'{world}/{policy}']=summary
    unchanged=all(sha(ROOT/p)==h for p,h in hashes.items())
    assert unchanged
    summary=dict(kind='exploratory_live_stream_guard',lanes=len(records),learning_episodes=len(records)*EPISODES,
        theta=theta,hcrit=float(HCRIT),conservative_fixed_wait_once=fixed_steps,
        source_hashes_unchanged=unchanged,by_group=by_group,selected_trace_checks=trace_checks,
        elapsed_seconds=time.perf_counter()-begin,
        limitations='Eight prelearned seeds and four context transitions in a supplied binary factorization. Guard is an external state comparator and wait controller. Fixed_once is a conservative analytic baseline, not an optimized fixed policy. Canonical diagnostic probes do not feed the learner. Continuous band invariance and selected numerical traces are distinct evidence.')
    dump(OUT/'summary.json',summary)
    print(json.dumps({k:dict(episode1=v['episodes']['1'],episode4=v['episodes']['4'],total_wait_steps=v['total_wait_steps']) for k,v in by_group.items()},indent=2,default=json_default),flush=True)


if __name__=='__main__':
    main()
