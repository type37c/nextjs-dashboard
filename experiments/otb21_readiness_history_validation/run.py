"""One-label learning under frozen preparations and new synthetic work phases."""
from pathlib import Path
import argparse
import importlib.util
import json
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('otb21_guard_reference',ROOT/'experiments/otb19_learning_readiness_guard/run.py')
B=importlib.util.module_from_spec(spec);sys.modules[spec.name]=B;spec.loader.exec_module(B)
SEEDS=tuple(range(24001,24009))
BUDGETS=(1536,2048,4096)
POLICIES=('usual','fixed4096','guard')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);args=ap.parse_args()
    if not args.name.replace('_','').isalnum():raise ValueError('Output name must be alphanumeric/underscore.')
    out=ROOT/'results/otb21_readiness_history_validation'/args.name
    if out.exists():raise FileExistsError(out)
    config=B.load(ROOT/'experiments/otb15_local_error_learning/MAIN_CONFIG.json')['base']
    prior=B.load(ROOT/'results/otb19_learning_readiness_guard/main/source_freeze.json')
    assert all(B.sha(ROOT/p)==h for p,h in prior['hashes'].items())
    theta=prior['theta'];hcrit=prior['hcrit']
    saved=[B.load(ROOT/f'results/otb15_local_error_learning/main_runs/normal_{seed}.json') for seed in SEEDS]
    memories=np.array([x['stage_states']['retained']['mem'] for x in saved])
    phases=np.random.default_rng(27501).uniform(0,2*np.pi,(4,3))
    works=np.zeros((4,3,4));works[:,:,0]=-1.2;works[:,:,1]=phases;works[:,:,2]=512
    out.mkdir(parents=True);(out/'traces').mkdir()
    np.savez_compressed(out/'inputs.npz',memories=memories,work_states=works,phases=phases,seeds=np.array(SEEDS))
    paths=[HERE/'DESIGN.md',HERE/'run.py',out/'inputs.npz',
        ROOT/'experiments/otb19_learning_readiness_guard/run.py',
        ROOT/'experiments/otb15_local_error_learning/model.py',ROOT/'experiments/otb15_local_error_learning/MAIN_CONFIG.json',
        ROOT/'experiments/otb17_learning_readiness/model.py',
        ROOT/'results/otb19_learning_readiness_guard/main/source_freeze.json',
        ROOT/'results/otb20_bounded_error_amplification/main_20261105/manifest.json',
        ROOT/'results/otb20_bounded_error_amplification/main_20261105/analysis.json']
    paths += [ROOT/f'results/otb15_local_error_learning/main_runs/normal_{seed}.json' for seed in SEEDS]
    hashes={p.relative_to(ROOT).as_posix():B.sha(p) for p in paths}
    for p in paths:
        dest=out/'source_snapshot'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
    B.dump(out/'source_freeze.json',dict(kind='fixed_policy_new_phase_and_deadline_boundary_evaluation',
        frozen_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),hashes=hashes,
        seeds=SEEDS,phase_rng=27501,phase_draws=4,old_pairs=[2,3],current_pairs=[0,1],
        budgets=BUDGETS,policies=POLICIES,fixed_wait=4096,theta=theta,hcrit=hcrit,config=config,
        expected_trials=1152,world_change='operation0_reversed_operation1_unchanged',
        total_time_includes_old_query_wait_current_query_delay_write=True,
        not_claimed='new semantic task family, new independent circuits, or general scaling'))
    rows=[];raw=[];old_rows=[];old_states=[];trace_checks=[];start=time.perf_counter()
    for si,seed in enumerate(SEEDS):
        mem0=memories[si];initial_bands=B.Q.memory_bands(mem0)
        assert np.all(initial_bands!=0)
        truth=np.array([(p%2)^saved[si]['initial_flips'][p//2]^(1 if p//2==0 else 0) for p in range(4)])
        for phase_index in range(4):
            for old_pair in (2,3):
                old=B.Q.query(mem0,works[phase_index],old_pair,4096,128,.01,config=config,record=True)
                old_id=len(old_rows)
                old_rows.append(dict(old_id=old_id,seed=seed,phase_index=phase_index,old_pair=old_pair,
                    prediction=old['pred'],counts=old['counts'].tolist(),first=old['first'].tolist(),
                    source_events=np.flatnonzero(old['trace'][:,79]).tolist(),
                    band_preserved=bool(old['band_preserved'].all())))
                old_states.append(dict(mem=old['final_mem'],work=old['final_work']))
                for current_pair in (0,1):
                    cells=B.noncurrent(current_pair);now=np.arange(2*current_pair,2*current_pair+2)
                    for budget in BUDGETS:
                        for policy in POLICIES:
                            selected=(seed==SEEDS[0] and phase_index==0 and old_pair==2 and current_pair==1
                                      and budget==1536 and policy in ('usual','guard'))
                            mem,work=old['final_mem'].copy(),old['final_work'].copy()
                            boundary=dict(post_old_mem=mem.copy(),post_old_work=work.copy())
                            prewait=B.bound(mem,current_pair,config)
                            wait=B.required_wait(mem,current_pair,theta,config) if policy=='guard' else 4096 if policy=='fixed4096' else 0
                            if wait:
                                expected,wait_effort=B.work_restoration(work,wait)
                                _,_,wait_trace=B.L.advance(mem,work,wait,config,record=selected)
                                assert np.array_equal(expected,work)
                            else:
                                wait_effort=0.;wait_trace=np.empty((0,82))
                            postwait=B.bound(mem,current_pair,config)
                            if policy=='guard':
                                assert postwait['tilt_bound']<hcrit
                                assert postwait['max_e']<=theta*(1+1e-12) and postwait['max_abs_s']<=theta*(1+1e-12)
                                assert B.unchanged_cells(mem0,mem,cells)
                            boundary['post_wait_mem']=mem.copy();boundary['post_wait_work']=work.copy()
                            current=B.Q.query(mem,work,current_pair,budget,128,.01,config=config,record=True)
                            mem,work=current['final_mem'],current['final_work']
                            boundary['post_query_mem']=mem.copy();boundary['post_query_work']=work.copy()
                            _,_,delay_trace=B.L.advance(mem,work,config['delay_steps'],config,record=selected)
                            boundary['at_write_mem']=mem.copy();boundary['at_write_work']=work.copy()
                            atwrite=B.bound(mem,current_pair,config)
                            delta=np.eye(2)[int(truth[current_pair])]-B.L.probability(current['pred'])
                            _,_,write_trace=B.L.advance(mem,work,config['write_steps'],config,delta=delta,record=selected)
                            boundary['post_write_mem']=mem.copy();boundary['post_write_work']=work.copy()
                            probe=B.canonical_probes(mem,config)
                            all_preserved=B.unchanged_cells(mem0,mem,cells)
                            if policy=='guard':assert atwrite['tilt_bound']<hcrit and all_preserved
                            aw=boundary['at_write_mem']
                            row=dict(row=len(rows),old_id=old_id,seed=seed,phase_index=phase_index,
                                old_pair=old_pair,current_pair=current_pair,budget=budget,policy=policy,
                                world_truth=truth.tolist(),wait_steps=wait,wait_effort=float(wait_effort),
                                total_live_steps=4096+wait+budget+config['delay_steps']+config['write_steps'],
                                prewait=prewait,postwait=postwait,atwrite=atwrite,
                                actual_prediction=current['pred'],counts=current['counts'].tolist(),first=current['first'].tolist(),
                                source_events=np.flatnonzero(current['trace'][:,79]).tolist(),
                                pre_counts=current['pre_counts'].tolist(),output_before_source=current['output_before_source'].tolist(),
                                source_tagged=bool(current['counts'][0]>0),delta=delta.tolist(),outcome=int(truth[current_pair]),
                                e_current_at_write=aw[now,5].tolist(),s_current_at_write=aw[now,6].tolist(),
                                canonical_probe=probe,current_context_correct=probe['predictions'][current_pair]==truth[current_pair],
                                untouched_operation1_correct=all(probe['predictions'][p]==truth[p] for p in (2,3)),
                                untouched_operation1_bands_preserved=B.unchanged_cells(mem0,mem,np.arange(4,8)),
                                all_noncurrent_bands_preserved=all_preserved,
                                current_query_bands_preserved=bool(current['band_preserved'].all()))
                            rows.append(row);raw.append(boundary)
                            if selected:
                                filename=f'row{row["row"]}.npz'
                                np.savez_compressed(out/'traces'/filename,old=old['trace'],wait=wait_trace,
                                    query=current['trace'],delay=delay_trace,write=write_trace,noncurrent=cells,
                                    initial_bands=initial_bands)
                                trace=np.concatenate([old['trace'],wait_trace,current['trace'],delay_trace,write_trace])
                                u=trace[:,:56].reshape(-1,8,7)[:,:,3]
                                bands=np.where(u<=B.Q.LOW,-1,np.where(u>=B.Q.HIGH,1,0))
                                kept=bool((bands[:,cells]==initial_bands[cells]).all())
                                maxtilt=float(np.max(np.abs(trace[:,68:76][:,cells])))
                                if policy=='guard':assert kept and maxtilt<hcrit
                                trace_checks.append(dict(file=filename,row=row['row'],policy=policy,native_steps=len(trace),
                                    noncurrent_bands_preserved_every_step=kept,noncurrent_max_abs_tilt=maxtilt))
        print(f'OTB21 seed={seed} trials={len(rows)}/1152',flush=True)
    assert len(rows)==1152 and len(old_rows)==64
    B.dump(out/'records.json',rows);B.dump(out/'old_queries.json',old_rows)
    np.savez_compressed(out/'states.npz',**{k:np.stack([r[k] for r in raw]) for k in raw[0]})
    np.savez_compressed(out/'old_states.npz',**{k:np.stack([r[k] for r in old_states]) for k in old_states[0]})
    groups={}
    for budget in BUDGETS:
        for policy in POLICIES:
            g=[r for r in rows if r['budget']==budget and r['policy']==policy]
            groups[f'{budget}/{policy}']=dict(trials=len(g),
                current_context_correct=sum(r['current_context_correct'] for r in g),
                untouched_operation1_correct=sum(r['untouched_operation1_correct'] for r in g),
                joint_adaptation_and_retention=sum(r['current_context_correct'] and r['untouched_operation1_correct'] for r in g),
                untouched_operation1_bands_preserved=sum(r['untouched_operation1_bands_preserved'] for r in g),
                all_noncurrent_bands_preserved=sum(r['all_noncurrent_bands_preserved'] for r in g),
                source_tagged=sum(r['source_tagged'] for r in g),
                pending_before_feedback=sum(r['actual_prediction']<0 for r in g),
                mean_wait=float(np.mean([r['wait_steps'] for r in g])),
                wait_range=[min(r['wait_steps'] for r in g),max(r['wait_steps'] for r in g)],
                mean_total_live_steps=float(np.mean([r['total_live_steps'] for r in g])),
                max_noncurrent_tilt_bound_at_write=max(r['atwrite']['tilt_bound'] for r in g))
    unchanged=all(B.sha(ROOT/p)==h for p,h in hashes.items());assert unchanged
    summary=dict(kind='fixed_policy_new_phase_and_deadline_boundary_evaluation',trials=len(rows),old_queries=len(old_rows),
        groups=groups,source_hashes_unchanged=unchanged,selected_trace_checks=trace_checks,
        elapsed_seconds=time.perf_counter()-start,
        scope='Four new shared work-phase draws, three query deadlines, eight existing learned seeds and supplied binary context routing. No parameter change after results and no novel semantic world confirmation.')
    B.dump(out/'summary.json',summary)
    print(json.dumps(groups,indent=2,default=B.json_default),flush=True)


if __name__=='__main__':main()
