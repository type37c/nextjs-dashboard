"""Exploratory history coupling pilot. No confirmatory claim. See DESIGN.md.

The processor/output integrator and copy bank have an independently written,
Numba-compiled implementation, checked against upstream and archived outcomes.
No fastmath; diagnostic candidate labels never enter observable policies.
"""
from pathlib import Path
import sys, json, pickle, time, hashlib, argparse, warnings
import numpy as np
from numba import njit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import InconsistentVersionWarning

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'experiments/e7d_confirm'))
with warnings.catch_warnings():
    warnings.simplefilter('ignore', InconsistentVersionWarning)
    import e7dcf as E
import bank as BK
import scaling_final as SF
from om2d_composition import BASE

HERE = Path(__file__).parent
OUT = ROOT/'results/history_coupling_pilot'
ARMS = ('B0','B1','B2_once','B2_repeat','B3')
HOLDS = (512,16384)
DEVICES = tuple(range(200,205))
TRAIN_GROUPS, EVAL_GROUPS = 8,16
BASES = {'train':9106100000,'eval':9106200000,'smoke':9106000000}

def dump(path, obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False,
        default=lambda x:x.tolist() if isinstance(x,np.ndarray) else x.item())+'\n')

def load_cal(seed):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', InconsistentVersionWarning)
        return pickle.load(open(ROOT/f'results/e7d_closed/cal_{seed}.pkl','rb'))

def score(model, features):
    """Explicit persisted StandardScaler + logistic linear score (no refit)."""
    sc,lr = model.steps[0][1],model.steps[1][1]
    return ((features-sc.mean_)/sc.scale_) @ lr.coef_[0] + lr.intercept_[0]

def pack(p,r):
    return np.column_stack([p['memory'][:,0],p['phase'][:,0],p['cd'][:,0],
        p['previous'][:,0],r['x'],r['phase'],r['cd'],np.zeros(len(r['x']))])

def unpack(st):
    return (dict(memory=st[:,0:1].copy(),phase=st[:,1:2].copy(),cd=st[:,2:3].astype(int),previous=st[:,3:4].astype(bool)),
            dict(x=st[:,4].copy(),phase=st[:,5].copy(),cd=st[:,6].astype(int)))

def parameters(X):
    pn,r=X['pn'],X['params']
    return np.array([pn['omega0'][0],pn['kappa'][0],pn['refractory'],BASE['eps'],BASE['beta'],*X['w'],r['leak'],r['gain'],r['theta']],float)

@njit(cache=True)
def integrate(st,drive,extra_r,gate,par,mode):
    """st columns: P m/phase/cd/previous, R x/phase/cd, removed-history h."""
    s=st.copy();T,n=drive.shape;pe=np.zeros((T,n),np.bool_);re=np.zeros((T,n),np.bool_)
    decay=1-par[3];two=2*np.pi
    for t in range(T):
        for i in range(n):
            m,ph,cd,prev,x,rph,rcd,h=s[i]
            kappa=0. if mode==1 else par[1]
            effective=m-h if mode==2 else m
            proposed=ph+par[0]+kappa*effective
            fire=proposed>=two and cd==0
            mn=decay*m+drive[t,i]-par[4]*fire
            if mode==3 and fire:mn=0.
            xn=par[8]*x+par[7]*(prev if gate[t,i] else 0.)+extra_r[t,i]
            rpn=rph+par[9]*max(xn-par[10],0.)
            rf=rpn>=two and rcd==0
            s[i,0]=mn;s[i,1]=0. if fire else proposed%two
            s[i,2]=par[2] if fire else max(cd-1,0.);s[i,3]=1. if fire else 0.
            s[i,4]=xn;s[i,5]=0. if rf else rpn%two;s[i,6]=32. if rf else max(rcd-1,0.)
            s[i,7]=decay*h
            pe[t,i]=fire;re[t,i]=rf
    return s,pe,re

@njit(cache=True)
def copy_bank_run(bs,shadow,pending,drive,events,bp,reset,kick):
    """Copy follows known input and observed P events; no true P m input.
    pending contains the previous observed spike's correction, preserving the
    upstream one-step delay. B3 correction is reconstructed from shadow history.
    """
    s=bs.copy();sh=shadow.copy();pd=pending.copy();T,n=drive.shape;K=bp.shape[0]
    spikes=np.zeros((T,n,K),np.bool_);a=1-BASE_EPS;two=2*np.pi
    for t in range(T):
        for i in range(n):
            pre=a*sh[i]+drive[t,i]
            correction=(-pre if reset else -BASE_BETA) if events[t,i] else 0.
            sn=pre+correction
            for j in range(K):
                m,ph,cd=s[i,j]
                proposed=ph+bp[j,0]+bp[j,1]*m
                fired=proposed>=two and cd==0
                d=drive[t,i]+pd[i]
                if t==kick:d+=bp[j,2]
                if t==kick+1 and kick>=0:d-=a*bp[j,2]
                s[i,j,0]=a*m+d
                s[i,j,1]=0. if fired else proposed%two
                s[i,j,2]=1. if fired else max(cd-1,0.)
                spikes[t,i,j]=fired
            sh[i]=sn;pd[i]=correction
    return s,sh,pd,spikes

BASE_EPS=float(BASE['eps']);BASE_BETA=float(BASE['beta'])

class Bank:
    def __init__(self,n,m0,D,thresholds):
        self.theta=np.asarray(thresholds);ka=np.full(len(thresholds),.02)
        self.bp=np.column_stack([2*np.pi/(98+D)-ka*self.theta,ka,1.5*2*np.pi/ka])
        self.st=np.zeros((n,len(ka),3));self.st[:,:,0]=m0
        self.shadow=np.full(n,m0);self.pending=np.zeros(n)
    def run(self,drive,events,mode,kick=-1):
        self.st,self.shadow,self.pending,sp=copy_bank_run(self.st,self.shadow,self.pending,drive,events,self.bp,mode==3,kick)
        return sp

def window(X,k,st,mode,idle=True):
    D=X['D'] if idle else 0;n=len(st);start=k*(484+X['D']);L=228+D
    me=X['me'][start:start+L];drive=np.zeros((L,n))
    drive[:128]=X['w'][0]*(me[:128,:,1].astype(float)-me[:128,:,0])
    drive[[0,2,4]]+=X['w'][1]*X['B'][:,k]*X['amp'][:,k]
    gate=np.zeros((L,n),bool);gate[:228]=True
    end,pe,re=integrate(st,drive,np.zeros_like(drive),gate,parameters(X),mode)
    return end,pe,re,drive

def prepare(X,k,st,mode,choice):
    gate,ep,er=E.candidate_inputs(choice,X['w']);g=np.broadcast_to(gate,(256,len(st))).copy()
    end,pe,re=integrate(st,ep,er,g,parameters(X),mode)
    return end,pe,re,ep

def pair_table(X,k,st,mode,A):
    """Only two allowed candidates, not old analytic margins. Diagnostics only.
    joint requires all four canonical probes; actual tests the actual next B.
    """
    T=[];actual=[];n=len(st);s=(k+1)*(484+X['D']);me=X['me'][s:s+228]
    for c in X['cfg']['pair']:
        ps,_,_,_=prepare(X,k,st,mode,np.full(n,c))
        ok=[]
        for bit,amp in E.PROBES:
            drive=X['w'][0]*(me[:,:,1].astype(float)-me[:,:,0])
            drive[128:]=0;drive[[0,2,4]]+=X['w'][1]*bit*amp
            _,_,re=integrate(ps,drive,np.zeros_like(drive),np.ones((228,n),bool),parameters(X),mode)
            ok.append(re.any(0)==(A&bool(bit)))
        T.append(np.all(ok,axis=0))
        _,_,re,_=window(X,k+1,ps,mode,idle=False)
        actual.append(re.any(0)==(A&X['B'][:,k+1].astype(bool)))
    return np.array(T),np.array(actual)

def form(st,sign):
    return np.column_stack([st[:,0],np.cos(st[:,1]),np.sin(st[:,1]),st[:,2],st[:,4],np.cos(st[:,5]),np.sin(st[:,5]),st[:,6],sign])

def run(data,X,arm,policy,cal,rng_seed=0,record_states=False):
    n=len(data['bits']);A=data['bits'].astype(bool);D=X['D'];pair=np.array(X['cfg']['pair'])
    st=pack(E.p_initial(n,X['pn'],X['config']['vref']),E.r_initial(n));bank=Bank(n,st[0,0],D,cal['thresholds'])
    mode=0;mref=float(np.median(cal['thresholds']));rng=np.random.default_rng(rng_seed)
    out={x:[] for x in ('correct','features','exact_features','T','actual_T','choice','copy_error','shadow_error','states','pre_states','mode','h','p_spikes','r_spikes','m_end')}
    for k in range(8):
        st,pe,re,drive=window(X,k,st,mode,idle=k<7)
        out['correct'].append(re[:228].any(0)==(A&X['B'][:,k].astype(bool)))
        out['p_spikes'].append(pe[:228].sum(0));out['r_spikes'].append(re[:228].sum(0));out['m_end'].append(st[:,0].copy())
        if k==7:break
        spikes=bank.run(drive,pe,mode,kick=128)
        # Identical observed-event forecast sign as upstream; no true A in policy.
        start=k*(484+D)
        _,sign,_=E.sync_estimate(X['me'][start:start+E.DECISION+1],X['mn'],X['w'][0],484+D,E.GATED,True,True,False)
        dd=dict(kick=BK.KickBank.latency_features(spikes,128),p_obs=BK.readout_features(pe[:,:,None],228+D),form=form(st,sign),theta=bank.theta)
        F=SF.features(dd,64,100+D);FE=SF.features(dd,64,100+D,exact=True)
        out['copy_error'].append(np.abs(bank.st[:,0,0]-st[:,0]));out['shadow_error'].append(np.abs(bank.shadow-st[:,0]))
        before=st.copy()
        if k==0:
            mode={'B0':0,'B1':1,'B2_once':2,'B2_repeat':2,'B3':3}[arm]
        if arm=='B2_repeat' or (arm=='B2_once' and k==0):st[:,7]=st[:,0]-mref
        T,AT=pair_table(X,k,st,mode,A)
        if isinstance(policy,str):
            if policy=='random':ix=rng.integers(0,2,n)
            elif policy=='oracle':ix=(T[1]&~T[0]).astype(int)
            elif policy=='frozen':ix=(score(cal['readouts'][64]['live'],F)>0).astype(int)
            elif policy=='fixed0':ix=np.zeros(n,int)
            elif policy=='fixed1':ix=np.ones(n,int)
            else:raise ValueError(policy)
        else:
            if 'constant' in policy:ix=np.full(n,policy['constant'],int)
            else:ix=(score(policy['model'],F)>0).astype(int)
        choice=pair[ix]
        for key,value in [('features',F),('exact_features',FE),('T',T),('actual_T',AT),('choice',ix),('states',st.copy()),('pre_states',before),('mode',mode),('h',st[:,7].copy())]:out[key].append(value)
        st,pe,re,drive=prepare(X,k,st,mode,choice);bank.run(drive,pe,mode)
    result={k:np.array(v) for k,v in out.items()}
    result.update(A=A,group=data['groups'],B=X['B'],amp=X['amp'],pair=pair,mref=np.array(mref))
    if not record_states:
        for k in ('states','pre_states'):result.pop(k)
    return result

def fit_readout(records):
    F=np.concatenate([r['features'].reshape(-1,r['features'].shape[-1]) for r in records])
    T=np.concatenate([r['T'].transpose(1,0,2).reshape(2,-1) for r in records],axis=1)
    sw=T[0]^T[1];y=(T[1]&~T[0]).astype(int)
    info=dict(rows=len(F),swap_rows=int(sw.sum()),swap_class_counts=np.bincount(y[sw],minlength=2).tolist(),candidate_success=T.mean(1).tolist())
    fixed=int(T[1].mean()>T[0].mean())
    if len(np.unique(y[sw]))<2:return dict(constant=fixed,info=info,fixed=fixed)
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=8000,C=3.,random_state=0)).fit(F[sw],y[sw])
    info['iterations']=int(model[-1].n_iter_[0])
    return dict(model=model,info=info,fixed=fixed)

def transplantation(data,X,base,cal):
    """Single-boundary diagnostics on B0 states. Same phase/cd/other state.
    Donors selected without outcome labels within A, current B, stage, device,
    hold; distinct group; same refractory; nearest circular phase.
    Exact thermometer score is privileged diagnostic, not live bank readout.
    """
    k=0;st=base['states'][k].copy();A=data['bits'].astype(bool);n=len(st);donor=np.full(n,-1,int)
    for i in range(n):
        mask=(A==A[i])&(X['B'][:,k]==X['B'][i,k])&(data['groups']!=data['groups'][i])&(st[:,2]==st[i,2])
        dist=np.abs(np.angle(np.exp(1j*(st[:,1]-st[i,1]))));mask&=dist<=.5
        candidates=np.flatnonzero(mask)
        if len(candidates):donor[i]=candidates[np.argmin(dist[candidates])]
    valid=donor>=0;ds=np.where(valid,donor,np.arange(n));tr=st.copy();tr[:,0]=st[ds,0]
    T0,AT0=pair_table(X,k,st,0,A);T1,AT1=pair_table(X,k,tr,0,A)
    # Exact features use only m thermometer + unchanged observed A/P timing gates.
    f0=base['exact_features'][k];f1=f0.copy();thresholds=cal['thresholds'][np.round(np.linspace(0,127,64)).astype(int)]
    thermo=tr[:,[0]]>=thresholds[None,:]
    for j in range(4):
        off=j*130
        f1[:,off:off+64]=thermo*f0[:,off+128:off+129]
        f1[:,off+64:off+128]=thermo*f0[:,off+129:off+130]
    exact=cal['readouts'][64]['exact'];c0=(score(exact,f0)>0).astype(int);c1=(score(exact,f1)>0).astype(int)
    o0=(T0[1]&~T0[0]).astype(int);o1=(T1[1]&~T1[0]).astype(int);ix=np.arange(n)
    return dict(valid=valid,donor=donor,group=data['groups'],A=A,original_m=st[:,0],donor_m=tr[:,0],phase_distance=np.abs(np.angle(np.exp(1j*(st[ds,1]-st[:,1])))),
        T0=T0,T1=T1,actual_T0=AT0,actual_T1=AT1,choice_original=c0,choice_informed=c1,
        original_correct=T0[c0,ix],misinformation_only=T0[c1,ix],transplant_stale=T1[c0,ix],transplant_informed=T1[c1,ix],
        oracle_stale=T1[o0,ix],oracle_informed=T1[o1,ix])

def job(seed):
    folder=OUT/f'device_{seed}';folder.mkdir(parents=True,exist_ok=False)
    cal=load_cal(seed);train=[];fit={}
    data=E.cohort(BASES['train']+seed,TRAIN_GROUPS)
    trainX={h:E.setup(seed,h,data,BASES['train']+10000+seed) for h in HOLDS}
    for arm in ARMS:
        rs=[]
        for h,X in trainX.items():
            r=run(data,X,arm,'random',cal,seed*100+h)
            np.savez_compressed(folder/f'train_{arm}_{h}.npz',**r);rs.append(r)
        fit[arm]=fit_readout(rs)
    pickle.dump(fit,open(folder/'refits.pkl','wb'));dump(folder/'fit_info.json',{a:{'fixed':v['fixed'],**v['info']} for a,v in fit.items()})
    data=E.cohort(BASES['eval']+seed,EVAL_GROUPS)
    for h in HOLDS:
        X=E.setup(seed,h,data,BASES['eval']+10000+seed)
        np.savez_compressed(folder/f'inputs_{h}.npz',**data,B=X['B'],amp=X['amp'])
        for arm in ARMS:
            for label,policy in [('frozen','frozen'),('refit',fit[arm]),('fixed','fixed'+str(fit[arm]['fixed'])),('oracle','oracle')]:
                r=run(data,X,arm,policy,cal,record_states=True)
                np.savez_compressed(folder/f'eval_{arm}_{label}_{h}.npz',**r)
                if arm=='B0' and label=='frozen':np.savez_compressed(folder/f'transplant_{h}.npz',**transplantation(data,X,r,cal))
        print(f'DONE device={seed} hold={h}',flush=True)
    return seed

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if args.run:
        if OUT.exists():raise RuntimeError('Output exists; refusing overwrite')
        OUT.mkdir(parents=True)
        dump(OUT/'protocol.json',dict(status='exploratory pilot, not preregistered confirmation',source_commit='01d84b5a41cc8d521724bbaa0127601b086b9936',
            arms=ARMS,holds=HOLDS,devices=DEVICES,train_groups=TRAIN_GROUPS,eval_groups=EVAL_GROUPS,bases=BASES,
            source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.suffix in ('.py','.md')},
            intervention_boundary='after decision window of computation 0; B2_repeat additionally at every later decision',
            mref='median of frozen training-derived E7-D memory thresholds',
            policy_information='observed A sign forecast, copy-bank spikes, observed P timing; no true state/labels to live policy',
            actual_future_labels='diagnostic only; choices and training use four canonical probes',
            donor_rule='same A/current B/P cd; different group; nearest circular phase within 0.5 rad; stage 0 only',
            python=sys.version,numpy=np.__version__))
        t=time.time()
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:list(pool.map(job,DEVICES))
        dump(OUT/'completion.json',dict(wall_seconds=time.time()-t,complete=True))
    else:parser.print_help()

if __name__=='__main__':main()
