"""Independent OTB21 saved-data audit; no acquisition/kernel imports."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'results/otb21_readiness_history_validation/history_20261105'
LOW,HIGH = 2-1/math.sqrt(3),2+1/math.sqrt(3)


def read(p): return json.loads(p.read_text(encoding='utf-8'))


def load(p):
    with np.load(p,allow_pickle=False) as f: return dict(f)


def bands(m): return np.where(m[...,3]<=LOW,-1,np.where(m[...,3]>=HIGH,1,0))


def close(a,b):
    error = float(np.abs(np.asarray(a)-np.asarray(b)).max())
    assert np.allclose(a,b,rtol=2e-12,atol=2e-12),error
    return error


def compare(a,b):
    for k,v in b.items():
        if isinstance(v,(float,np.floating)): close(a[k],v)
        else: assert a[k]==v,(k,a[k],v)


def decode(c):
    hit = np.asarray(c)[...,1:]>0
    return np.where(hit.sum(-1)==1,hit.argmax(-1),-1)


def event_check(counts,first,budget):
    c,f = np.array(counts),np.array(first)
    assert np.array_equal(c==0,f==-1)
    assert ((f[f>=0]>=128)&(f[f>=0]<budget)).all()


def query_es(start,pair,steps,events,a,b):
    result = start[:,5]*a**steps
    if events: result[pair*2:pair*2+2] = a**(steps-1-events[-1])
    return result,start[:,6]*b**steps


def main():
    spec,rows,olds,summary = (read(OUT/p) for p in ('source_freeze.json','records.json','old_queries.json','summary.json'))
    z,oz,inputs = (load(OUT/p) for p in ('states.npz','old_states.npz','inputs.npz'))
    for p,h in spec['hashes'].items():
        assert hashlib.sha256((OUT/'source_snapshot'/p).read_bytes()).hexdigest()==h
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    prior19 = read(ROOT/'results/otb19_learning_readiness_guard/main/source_freeze.json')
    prior20 = read(ROOT/'results/otb20_bounded_error_amplification/main_20261105/manifest.json')
    cfg = spec['config']; assert cfg==prior19['config']==prior20['config']
    assert prior20['frozen_utc'] < spec['frozen_utc']
    for p in ('experiments/otb15_local_error_learning/model.py','experiments/otb17_learning_readiness/model.py','experiments/otb15_local_error_learning/MAIN_CONFIG.json'):
        assert spec['hashes'][p]==prior19['hashes'][p]==prior20['source_hashes'][p]
    assert spec['budgets']==[1536,2048,4096] and spec['policies']==['usual','fixed4096','guard']
    assert spec['phase_rng']==27501 and spec['fixed_wait']==4096
    phases = np.random.default_rng(27501).uniform(0,2*np.pi,(4,3))
    assert np.array_equal(inputs['phases'],phases)
    expected_work=np.zeros((4,3,4));expected_work[:,:,0]=-1.2;expected_work[:,:,1]=phases;expected_work[:,:,2]=512
    assert np.array_equal(inputs['work_states'],expected_work)
    assert np.array_equal(inputs['seeds'],np.arange(24001,24009))
    original = {s:read(ROOT/f'results/otb15_local_error_learning/main_runs/normal_{s}.json') for s in spec['seeds']}
    for si,s in enumerate(spec['seeds']):
        assert np.array_equal(inputs['memories'][si],original[s]['stage_states']['retained']['mem'])
    hc=2/(3*math.sqrt(3));theta=.95*(hc-cfg['hold_eta'])/cfg['alpha']
    close(hc,spec['hcrit']);close(theta,spec['theta']);close(theta,prior19['theta'])
    assert cfg['tau_s']>=1 and cfg['noise']==0
    a=math.exp(-1/cfg['tau_e']);b=1-1/cfg['tau_s']
    assert len(rows)==1152 and len(olds)==64
    assert all(len(x)==1152 and np.isfinite(x).all() for x in z.values())
    assert all(len(x)==64 and np.isfinite(x).all() for x in oz.values())
    for label,m in [(k,v) for k,v in z.items() if k.endswith('_mem')]+[('old_mem',oz['mem']),('input_mem',inputs['memories'])]:
        assert (m[...,3]>0).all() and (m[...,5]>=0).all() and (m[...,5]<=1+1e-12).all(),label
    max_es=0.;old_keys=set();seen=set();guard_waits=[];max_wait_bound=0.;encoded_current_correct=0
    for oid,o in enumerate(olds):
        assert o['old_id']==oid
        key=(o['seed'],o['phase_index'],o['old_pair']);assert key not in old_keys;old_keys.add(key)
        s,phase,pair=key;assert s in original and phase in range(4) and pair in (2,3)
        initial=inputs['memories'][s-24001]
        event_check(o['counts'],o['first'],4096)
        assert int(decode(o['counts']))==o['prediction']
        events=o['source_events'];assert events==sorted(set(events)) and all(0<=t<4096 for t in events)
        assert len([t for t in events if t>=128])==o['counts'][0]
        ee,ss=query_es(initial,pair,4096,events,a,b)
        max_es=max(max_es,close(ee,oz['mem'][oid,:,5]),close(ss,oz['mem'][oid,:,6]))
        assert np.array_equal(bands(initial),bands(oz['mem'][oid]))
        assert o['band_preserved'] is True
    for i,r in enumerate(rows):
        assert i==r['row'];s,phase,old,cur,budget,policy=(r[k] for k in ('seed','phase_index','old_pair','current_pair','budget','policy'))
        key=(s,phase,old,cur,budget,policy);assert key not in seen;seen.add(key)
        assert s in original and phase in range(4) and old in (2,3) and cur in (0,1) and budget in spec['budgets'] and policy in spec['policies']
        oid=r['old_id'];o=olds[oid];assert (o['seed'],o['phase_index'],o['old_pair'])==(s,phase,old)
        assert np.array_equal(z['post_old_mem'][i],oz['mem'][oid]) and np.array_equal(z['post_old_work'][i],oz['work'][oid])
        initial=inputs['memories'][s-24001];ib=bands(initial);cells=np.array([c for c in range(8) if c//2!=cur]);now=np.arange(cur*2,cur*2+2)
        truth=np.array([(p%2)^original[s]['initial_flips'][p//2]^(p//2==0) for p in range(4)],int)
        assert r['world_truth']==truth.tolist() and r['outcome']==truth[cur]
        pre,waited,queried,aw,post=(z[k][i] for k in ('post_old_mem','post_wait_mem','post_query_mem','at_write_mem','post_write_mem'))
        for label,m in [('prewait',pre),('postwait',waited),('atwrite',aw)]:
            em=float(m[cells,5].max());sm=float(np.abs(m[cells,6]).max())
            compare(r[label],dict(max_e=em,max_abs_s=sm,tilt_bound=cfg['hold_eta']+cfg['alpha']*max(em,sm)))
        em,sm=r['prewait']['max_e'],r['prewait']['max_abs_s']
        needed=max(math.ceil(cfg['tau_e']*math.log(em/theta)) if em>theta else 0,math.ceil(math.log(sm/theta)/(-math.log1p(-1/cfg['tau_s']))) if sm>theta else 0)
        wait=needed if policy=='guard' else 4096 if policy=='fixed4096' else 0
        assert r['wait_steps']==wait and r['total_live_steps']==4096+wait+budget+1000+8000
        max_es=max(max_es,close(waited[:,5],pre[:,5]*a**wait),close(waited[:,6],pre[:,6]*b**wait))
        if wait==0: assert np.array_equal(pre,waited) and r['wait_effort']==0
        assert r['wait_effort']>=0
        if policy=='guard':
            guard_waits.append(wait)
            # While waiting delta is zero: the initial accumulator alone bounds h.
            waiting_bound=cfg['hold_eta']+cfg['alpha']*sm;max_wait_bound=max(max_wait_bound,waiting_bound)
            assert waiting_bound<hc
            for label in ('postwait','atwrite'):
                assert r[label]['max_e']<=theta*(1+1e-12) and r[label]['max_abs_s']<=theta*(1+1e-12) and r[label]['tilt_bound']<hc
            for m in (waited,queried,aw,post): assert (bands(m)[cells]==ib[cells]).all()
        event_check(r['counts'],r['first'],budget);events=r['source_events']
        assert events==sorted(set(events)) and all(0<=t<budget for t in events)
        pre_events=[t for t in events if t<128];post_events=[t for t in events if t>=128]
        assert len(pre_events)==r['pre_counts'][0] and len(post_events)==r['counts'][0]
        assert r['source_tagged']==bool(post_events)
        assert r['first'][0]==(post_events[0] if post_events else -1)
        ee,ss=query_es(waited,cur,budget,events,a,b)
        max_es=max(max_es,close(queried[:,5],ee),close(queried[:,6],ss))
        max_es=max(max_es,close(aw[:,5],queried[:,5]*a**1000),close(aw[:,6],queried[:,6]*b**1000))
        pred=int(decode(r['counts']));assert r['actual_prediction']==pred
        prob=np.eye(2)[pred] if pred>=0 else np.array([.5,.5]);delta=np.eye(2)[truth[cur]]-prob
        assert np.array_equal(delta,r['delta'])
        close(r['e_current_at_write'],aw[now,5]);close(r['s_current_at_write'],aw[now,6])
        max_es=max(max_es,close(post[:,5],aw[:,5]*a**8000),close(post[:,6],aw[:,6]*b**8000+np.tile(delta,4)*aw[:,5]*a*(b**8000-a**8000)/(cfg['tau_s']*(b-a))))
        probe=r['canonical_probe'];pp=probe['predictions'];assert probe['bands']==bands(post).tolist()
        assert np.array_equal(decode(probe['counts']),pp);event_check(probe['counts'],probe['first'],4096)
        current_bands=tuple(bands(post)[now]);encoded=0 if current_bands==(1,-1) else 1 if current_bands==(-1,1) else -1
        encoded_current_correct+=int(encoded==truth[cur])
        compare(r,dict(current_context_correct=pp[cur]==truth[cur],untouched_operation1_correct=all(pp[p]==truth[p] for p in (2,3)),
            untouched_operation1_bands_preserved=bool((bands(post)[4:]==ib[4:]).all()),all_noncurrent_bands_preserved=bool((bands(post)[cells]==ib[cells]).all())))
        assert r['current_query_bands_preserved'] and np.array_equal(bands(waited),bands(queried))
    assert len(seen)==1152 and len(old_keys)==64
    groups={}
    for budget in spec['budgets']:
        for policy in spec['policies']:
            group=[r for r in rows if r['budget']==budget and r['policy']==policy]
            value=dict(trials=len(group),**{k:sum(r[k] for r in group) for k in ('current_context_correct','untouched_operation1_correct','untouched_operation1_bands_preserved','all_noncurrent_bands_preserved','source_tagged')},
                joint_adaptation_and_retention=sum(r['current_context_correct'] and r['untouched_operation1_correct'] for r in group),
                pending_before_feedback=sum(r['actual_prediction']<0 for r in group),mean_wait=float(np.mean([r['wait_steps'] for r in group])),
                wait_range=[min(r['wait_steps'] for r in group),max(r['wait_steps'] for r in group)],mean_total_live_steps=float(np.mean([r['total_live_steps'] for r in group])),
                max_noncurrent_tilt_bound_at_write=max(r['atwrite']['tilt_bound'] for r in group))
            assert value['trials']==128;key=f'{budget}/{policy}';compare(summary['groups'][key],value);groups[key]=value
    trace_results=[]
    for check in summary['selected_trace_checks']:
        tr=load(OUT/'traces'/check['file']);i=check['row'];r=rows[i];cells=tr['noncurrent'];initial=inputs['memories'][r['seed']-24001]
        segments=[('old',initial,oz['mem'][r['old_id']],r['old_pair']),('wait',z['post_old_mem'][i],z['post_wait_mem'][i],None),
            ('query',z['post_wait_mem'][i],z['post_query_mem'][i],r['current_pair']),('delay',z['post_query_mem'][i],z['at_write_mem'][i],None),('write',z['at_write_mem'][i],z['post_write_mem'][i],None)]
        radial_error=trace_es_error=0.
        for name,start,end,pair in segments:
            trace=tr[name];n=len(trace)
            if n==0: assert np.array_equal(start,end);continue
            mem=trace[:,:56].reshape(-1,8,7);assert np.array_equal(mem[-1],end)
            t=np.arange(n);ee=start[:,5][None]*a**(t[:,None]+1)
            if pair is not None:
                fired=trace[:,79]>0;last=np.maximum.accumulate(np.where(fired,t,-1));sel=last>=0
                ee[np.ix_(sel,[pair*2,pair*2+1])]=(a**(t[sel]-last[sel]))[:,None]
                assert np.flatnonzero(fired).tolist()==(olds[r['old_id']]['source_events'] if name=='old' else r['source_events'])
            d=np.tile(r['delta'],4) if name=='write' else np.zeros(8)
            ss=start[:,6][None]*b**(t[:,None]+1)+start[:,5][None]*d[None]*a*(b**(t[:,None]+1)-a**(t[:,None]+1))/(cfg['tau_s']*(b-a))
            trace_es_error=max(trace_es_error,close(ee,mem[:,:,5]),close(ss,mem[:,:,6]))
            prev=np.concatenate([start[None],mem[:-1]])
            h=cfg['hold_eta']*np.tanh((prev[:,:,0]+.43071203972028016)/.25)+cfg['alpha']*mem[:,:,6]
            close(h,trace[:,68:76]);u=prev[:,:,3]
            def derivative(v): return 2e-4*v*((v-2)-(v-2)**3+h)
            k1=derivative(u);k2=derivative(u+k1/2);k3=derivative(u+k2/2);k4=derivative(u+k3)
            radial_error=max(radial_error,close(u+(k1+2*k2+2*k3+k4)/6,mem[:,:,3]))
        full=np.concatenate([tr[k] for k in ('old','wait','query','delay','write')]);m=full[:,:56].reshape(-1,8,7)
        preserve=bool((bands(m)[:,cells]==bands(initial)[cells]).all());tilt=float(np.abs(full[:,68:76][:,cells]).max())
        compare(check,dict(native_steps=len(full),noncurrent_bands_preserved_every_step=preserve,noncurrent_max_abs_tilt=tilt))
        trace_results.append(dict(file=check['file'],steps=len(full),noncurrent_preserved=preserve,max_noncurrent_tilt=tilt,es_max_error=trace_es_error,radial_rk4_max_error=radial_error))
    result=dict(passed=True,trials=1152,old_queries=64,source_hashes_and_snapshots_checked=True,
        phase_rng_and_all_saved_memory_inputs_reconstructed=True,same_core_and_config_as_otb19_otb20=True,
        local_freeze_after_otb20_record=True,all_saved_es_boundaries_max_error=max_es,all_summary_groups_reconstructed=groups,
        current_context_encoded_correct=encoded_current_correct,
        guard_wait_unique=sorted(set(guard_waits)),waiting_delta_zero_s_only_max_tilt_bound=max_wait_bound,
        selected_trace_reconstruction=trace_results,
        scope='Independent saved-data/closed recurrence audit; no acquisition or dynamics modules imported.',
        limitations=['128 per group equals eight reused memories x four shared synthetic phase draws x two old x two current contexts, not independent semantic worlds.',
          'Local hashes and timestamps document fixed artifacts; they are not an external preregistration service.',
          'Protection at every native step is directly checked only on two retained traces; all trials have checked saved boundaries and continuous sufficient bounds.',
          'The trace audit independently reconstructs e/s, h, and radial RK4; full T7/work trajectories are not independently replayed.',
          'The 4096 wait was chosen from OTB20 before this acquisition. Guard robustness does not establish an advantage over an optimized longer fixed wait.',
          'Shorter query deadlines give old eligibility less time to decay before feedback; deadline and learning timing are jointly changed.',
          'source_tagged means at least one post-cue source event here; pre-cue source events were separately checked against saved event lists.',
          'No novel semantic family, fully oscillator-based controller, physical efficiency, or general scaling result is established.'])
    (OUT/'audit_independent.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('PASS: 1152 trials / 64 old queries; RNG, labels, e/s, guard, groups, two radial trace reconstructions.')


if __name__=='__main__':main()
