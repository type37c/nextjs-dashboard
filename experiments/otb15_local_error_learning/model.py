"""OTB15 fixed T7 + bistable companion, with explicitly auxiliary e/s states."""
from pathlib import Path
import sys
import math
import numpy as np

try:
    from numba import njit
except ImportError:
    fallback = Path(__file__).resolve().parents[2] / '.cache/oscillator-night-pydeps'
    if fallback.exists():
        sys.path.insert(0, str(fallback))
    from numba import njit

EPS=6.5e-5; BETA=.6; KAPPA=.025; OMEGA=2*np.pi/258; R=512
NU=1e-4; WC=2*np.pi/595; CHI=.001; SCALE=.25
MC=-.43071203972028016; G=.00015
LOW=2-1/np.sqrt(3); HIGH=2+1/np.sqrt(3)
BITS=np.array([[i>>2&1,i>>1&1,i&1] for i in range(8)], dtype=np.int64)
TRAIN=BITS[BITS.sum(1)%2==0]; TEST=BITS[BITS.sum(1)%2==1]
DEFAULT=dict(alpha=6.,tau_e=6000.,tau_s=1000.,query_steps=4096,
             cue_step=1024,write_steps=10000,delay_steps=1000,
             hold_eta=.1,noise=0.,gain=.3,competition=1.,
             epochs=3,reverse_epochs=3,retention_steps=80000)
CFG_KEYS=('alpha','tau_e','tau_s','cue_step','hold_eta','noise','gain','competition')
STATS_LOG=[]

def config_array(config):
    return np.array([config[k] for k in CFG_KEYS], dtype=np.float64)

def initial(seed):
    rng=np.random.default_rng(seed)
    mem=np.zeros((8,7),dtype=np.float64)
    mem[:,0]=MC;mem[:,1]=rng.uniform(0,2*np.pi,8);mem[:,2]=R
    mem[:,3]=1.;mem[:,4]=rng.uniform(0,2*np.pi,8)
    work=np.zeros((3,4),dtype=np.float64)
    work[:,0]=-1.2;work[:,1]=rng.uniform(0,2*np.pi,3);work[:,2]=R
    return mem,work

@njit(cache=True)
def radial(u,h):
    v=u-2.
    return 2.*NU*u*(v-v*v*v+h)

@njit(cache=True)
def _advance(mem,work,steps,query,pair,delta,cfg,wrong_tag,numeric,cut,seed,record):
    np.random.seed(seed)
    alpha,tau_e,tau_s,cue,hold_eta,noise,gain,competition=cfg
    decay=math.exp(-1./tau_e)
    counts=np.zeros(3,np.int64);first=np.full(3,-1,np.int64)
    # Trace columns: memory after (56), work after (12), total h (8), work drive (3), events (3).
    trace=np.empty((steps if record else 0,82),np.float64)
    stats=np.array([np.inf,-np.inf,np.inf,-np.inf,0.,0.])
    for t in range(steps):
        old_prev=work[0,3]
        coupling0=0.;coupling1=0.
        if query and not cut:
            u0=mem[2*pair,3];u1=mem[2*pair+1,3]
            coupling0=gain*max(u0-1.,0.)
            coupling1=gain*max(u1-1.,0.)
            if competition>0.:
                coupling0*=min(1.,max(0.,(3.-u1)/2.))
                coupling1*=min(1.,max(0.,(3.-u0)/2.))
        drives=np.empty(3,np.float64)
        fired=np.zeros(3,np.int64)
        for j in range(3):
            d=EPS*(-1.2)
            if (not query) or t<int(cue):d+=.01*(-1.2-work[j,0])
            if query and t==int(cue) and j==0:d+=.6
            if j==1:d+=old_prev*coupling0
            if j==2:d+=old_prev*coupling1
            drives[j]=d
            m=work[j,0];p=work[j,1];cd=work[j,2]
            pn=p+OMEGA+KAPPA*m
            f=pn>=2.*math.pi and cd==0.
            work[j,0]=(1.-EPS)*m+d-BETA*int(f)
            work[j,1]=0. if f else pn%(2.*math.pi)
            work[j,2]=R if f else max(cd-1.,0.)
            work[j,3]=1. if f else 0.;fired[j]=int(f)
            if query and t>=int(cue) and f:
                counts[j]+=1
                if first[j]<0:first[j]=t
        tagpair=(pair^1) if wrong_tag else pair
        hs=np.empty(8,np.float64)
        for c in range(8):
            m,p,cd,u,psi,e,s=mem[c]
            e*=decay
            if query and fired[0] and c//2==tagpair:e=1.
            s+=(e*delta[c%2]-s)/tau_s
            signal=0. if numeric else math.tanh((m-MC)/SCALE)
            h=hold_eta*signal+alpha*s
            if noise>0.:h+=noise*np.random.normal()
            hs[c]=h
            k1=radial(u,h);k2=radial(u+.5*k1,h)
            k3=radial(u+.5*k2,h);k4=radial(u+k3,h)
            un=u+(k1+2*k2+2*k3+k4)/6.
            if not numeric:
                pn=p+OMEGA+KAPPA*m
                f=pn>=2.*math.pi and cd==0.
                mem[c,0]=(1.-EPS)*m+.001+G*math.sqrt(max(u,0.))*math.cos(psi)-BETA*int(f)
                mem[c,1]=0. if f else pn%(2.*math.pi)
                mem[c,2]=R if f else max(cd-1.,0.)
                mem[c,4]=(psi+WC+CHI*signal)%(2.*math.pi)
            mem[c,3]=un;mem[c,5]=e;mem[c,6]=s
            stats[0]=min(stats[0],un);stats[1]=max(stats[1],un)
            stats[2]=min(stats[2],h);stats[3]=max(stats[3],h)
            stats[4]=max(stats[4],abs(e));stats[5]=max(stats[5],abs(s))
        if record:
            trace[t,:56]=mem.reshape(56)
            trace[t,56:68]=work.reshape(12)
            trace[t,68:76]=hs;trace[t,76:79]=drives;trace[t,79:82]=fired
    return counts,first,trace,stats

def advance(mem,work,steps,config,query=False,pair=0,delta=None,
            mode='normal',cut=False,seed=0,record=False):
    if delta is None:delta=np.zeros(2)
    counts,first,trace,stats=_advance(mem,work,int(steps),bool(query),int(pair),np.asarray(delta,dtype=float),
                    config_array(config),mode=='wrong_trace',mode=='numeric_memory',
                    bool(cut),int(seed),bool(record))
    assert np.isfinite(mem).all() and np.isfinite(work).all() and np.all(mem[:,3]>0)
    if steps>0:
        assert stats[0]>0 and np.isfinite(stats).all()
        STATS_LOG.append(stats.copy())
    return counts,first,trace

def decode(counts):
    hit=np.asarray(counts)[1:]>0
    return int(hit.argmax()) if hit.sum()==1 else -1

def predict(mem,work,features,action,config,mode='normal',cut=False,seed=0,record=False):
    pair=2*int(action)+int(features[action])
    counts,first,trace=advance(mem,work,config['query_steps'],config,True,pair,
                              mode=mode,cut=cut,seed=seed,record=record)
    pred=decode(counts)
    if mode=='numeric_memory':
        hit=mem[2*pair:2*pair+2,3]>=HIGH
        pred=int(hit.argmax()) if hit.sum()==1 else -1
        if cut:pred=-1
    return pred,counts,first,trace

def probability(pred):
    return np.array([.5,.5]) if pred<0 else np.eye(2)[pred].copy()

def observe(mem,work,pred,outcome,config,mode='normal',seed=0,record=False):
    # This is the only pathway through which a label reaches dynamics.
    before=(mem.copy(),work.copy())
    _,_,td=advance(mem,work,config['delay_steps'],config,mode=mode,seed=seed,record=record)
    delta=np.eye(2)[int(outcome)]-probability(pred)
    if mode=='zero_error':delta*=0
    if mode=='reverse_error':delta*=-1
    _,_,tw=advance(mem,work,config['write_steps'],config,delta=delta,
                   mode=mode,seed=seed+1,record=record)
    return delta,before,td,tw

def evaluate(mem,work,flips,config,mode='normal',cut=False,seed=0):
    rows=[]
    # Each held-out probe starts from the same copied dynamic boundary; probes
    # never update the learner or return labels to it.
    for q,x in enumerate(TEST):
        for a in range(2):
            mm,ww=mem.copy(),work.copy()
            pred,counts,first,_=predict(mm,ww,x,a,config,mode,cut,seed+2*q+a)
            truth=int(x[a])^int(flips[a])
            rows.append(dict(features=x.tolist(),action=a,truth=truth,pred=pred,
                             counts=counts.tolist(),first=first.tolist()))
    return rows

def score(rows,action=None):
    chosen=[r for r in rows if action is None or r['action']==action]
    return dict(correct=sum(r['pred']==r['truth'] for r in chosen),
                wrong=sum(r['pred']>=0 and r['pred']!=r['truth'] for r in chosen),
                pending=sum(r['pred']<0 for r in chosen),queries=len(chosen))
