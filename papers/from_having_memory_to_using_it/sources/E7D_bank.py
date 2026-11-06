"""E7-D circuit components (exploratory). Three equal-size banks of K = 16 units run continuously through the whole chain (never reset):
EFF_T7  T7 units driven by an efference copy of P's input stream: a * gated M signal + b * B pulse during computation, the circuit's own
        preparation pulses during preparation, nothing while the ports are closed (exactly what P receives; known to the circuit).
OBS_T7  the same T7 units driven by the observed channels only (M0, M1, P spikes, R spikes, B) through fixed random weights.
OBS_LIF 16 MC-5C LIF relays on the observed channels (fixed random weights, time constants 16-1024), the "mixed memory" control.
T7 units: om2g core.step (P's refractory, BASE eps/beta), heterogeneous omega0 x kappa so that they fire spontaneously and their rhythm
encodes the integrated input. The readout (linear weights on the bank's spikes) is the only learned part."""
import numpy as np
import e7c
from e7c import Relay,advance
K=16;OMEGA=(.04,.08,.15,.3);KAPPA=(.002,.005,.01,.02)


class T7Bank:
    def __init__(s,n,refractory,in_weights=None):
        s.net=dict(omega0=np.repeat(OMEGA,4)[None,:].repeat(1,0)[0],kappa=np.tile(KAPPA,4),refractory=refractory);s.W=in_weights
        s.st=dict(memory=np.zeros((n,K)),phase=np.zeros((n,K)),cd=np.zeros((n,K),int),previous=np.zeros((n,K),bool));s.J=np.zeros((K,K))
    def run(s,drive):
        """drive (steps, n) scalar per row (EFF: same for every unit) or (steps, n, C) channels mixed by W; returns spikes (steps, n, K)."""
        out=np.zeros((len(drive),)+s.st['memory'].shape,bool)
        for t in range(len(drive)):
            d=drive[t][:,None]*np.ones(K) if s.W is None else drive[t]@s.W
            s.st=advance(s.st,d,s.net,s.J);out[t]=s.st['previous']
        return out


class LIFBank:
    def __init__(s,n,rng):
        taus=np.repeat((16.,64.,256.,1024.),4);s.relays=[Relay(dict(w=rng.normal(0,1,5),w0=0.,tau=t,setting=(1.,.005)),n) for t in taus]
    def run(s,pop):return np.stack([rl.run(pop)[0] for rl in s.relays],axis=-1).astype(bool)


def readout_features(spikes,end_window):
    """Per unit over the current computation + decision window: spike count, steps since the last spike at the window end (capped), and a
    leaky trace (tau 64) at the window end. spikes (steps, n, K) of the window."""
    T=len(spikes);t=np.arange(T)[:,None,None];cnt=spikes.sum(0);last=np.where(spikes.any(0),T-1-np.max(np.where(spikes,t,-1),axis=0),T)
    tr=(spikes*np.exp(-(T-1-t)/64.)).sum(0);return np.concatenate([cnt,np.minimum(last,T),tr],axis=1).astype(float)


class MemoryCopyBank:
    """EFF_MC: T7 units whose memory equals P's memory, each with its own clock. Self-coupling +beta cancels the unit's own spike-triggered
    memory drop one step later; the observed P spikes enter with -beta (one step later), so m_k follows P's m (same eps, same drive, same
    start), while omega0/kappa differ so that the units fire on their own and their rhythm encodes m. Spikes are the only output."""
    def __init__(s,n,refractory,m0):
        from om2d_composition import BASE
        s.beta=BASE['beta'];s.net=dict(omega0=np.repeat((.12,.16,.22,.3),4),kappa=np.tile((.002,.004,.008,.012),4),refractory=refractory)
        s.st=dict(memory=np.full((n,K),float(m0)),phase=np.zeros((n,K)),cd=np.zeros((n,K),int),previous=np.zeros((n,K),bool));s.J=s.beta*np.eye(K);s.prevP=np.zeros(n)
    def run(s,drive,p_events):
        out=np.zeros((len(drive),)+s.st['memory'].shape,bool)
        for t in range(len(drive)):
            d=(drive[t]-s.beta*s.prevP)[:,None]*np.ones(K);s.st=advance(s.st,d,s.net,s.J);out[t]=s.st['previous'];s.prevP=p_events[t].astype(float)
        return out


class KickBank:
    """Scaling probe (E7-D, axis 1). Memory-copy T7 units (memory = P's memory, as MemoryCopyBank) with their own refractory of 1 step.
    At computation step 128 (after the M->P gate closes, P's memory is constant up to its own spikes until the decision) every unit gets a
    reversible kick: +G_k for one step forces a spike (phase reset to 0), -(1-eps) G_k the next step restores the memory exactly. The
    latency of the next spike then depends only on m (s = omega0_k + kappa_k m, latency = ceil(2 pi / s)); units are tuned so that their
    'fired before the decision' thresholds tile the memory range (a thermometer code), refined by the latencies."""
    KICK_STEP=128
    def __init__(s,n,m0,lmax,size=64,kappas=(.003,.005,.008,.012),theta=(-11.,2.),thresholds=None,kappa_tuned=.02):
        from om2d_composition import BASE
        s.beta,s.eps=BASE['beta'],BASE['eps']
        if thresholds is None:per=size//len(kappas);th=np.linspace(*theta,per);ka=np.repeat(kappas,per);tt=np.tile(th,len(kappas))
        else:tt=np.asarray(thresholds,float);ka=np.full(tt.size,kappa_tuned);size=tt.size   # thresholds tuned to the experienced memory range
        om=2*np.pi/lmax-ka*tt;s.theta=tt;s.K=size;s.net=dict(omega0=om,kappa=ka,refractory=1);s.G=1.5*2*np.pi/ka
        s.st=dict(memory=np.full((n,size),float(m0)),phase=np.zeros((n,size)),cd=np.zeros((n,size),int),previous=np.zeros((n,size),bool));s.J=s.beta*np.eye(size);s.prevP=np.zeros(n)
        s.own_beta=0.                                   # v2: readout units are T7 units with beta = 0 (no spike-triggered memory drop)
    def step(s,d):
        """om2g core.step with this unit's beta (= 0): same phase / refractory rule, m = (1 - eps) m + drive."""
        st=s.st;pn=st['phase']+s.net['omega0']+s.net['kappa']*st['memory'];fired=(pn>=2*np.pi)&(st['cd']==0)
        s.st=dict(memory=(1-s.eps)*st['memory']+d-s.own_beta*fired,phase=np.where(fired,0.,pn%(2*np.pi)),cd=np.where(fired,s.net['refractory'],np.maximum(st['cd']-1,0)),previous=fired)
    def run(s,drive,p_events,kick_at=None):
        """v2 (beta = 0, no self-coupling): the v1 self-coupling compensated the own spike one step late; near-zero speeds then turned
        negative for one step, the phase wrapped to just below 2 pi and produced spurious spikes."""
        out=np.zeros((len(drive),)+s.st['memory'].shape,bool)
        for t in range(len(drive)):
            d=(drive[t]-s.beta*s.prevP)[:,None]*np.ones(s.K)
            if kick_at is not None and t==kick_at:d=d+s.G
            if kick_at is not None and t==kick_at+1:d=d-(1-s.eps)*s.G
            s.step(d);out[t]=s.st['previous'];s.prevP=p_events[t].astype(float)
        return out
    def run_rekick(s,drive,p_events,kick_at):
        """v3: kick at the gate closure (kick_at) and again one step after every observed P spike later in the window (P's spike lowers
        P's memory by beta; re-kicking restarts the latency on the new memory). Returns spikes and, per row, the step of the last kick."""
        n=s.st['memory'].shape[0];out=np.zeros((len(drive),n,s.K),bool);last=np.full(n,-1);kicked=np.zeros(n,bool)
        for t in range(len(drive)):
            d=(drive[t]-s.beta*s.prevP)[:,None]*np.ones(s.K);d=d-np.where(kicked,1.,0.)[:,None]*(1-s.eps)*s.G
            kick=np.full(n,t==kick_at) if t<=kick_at else s.prevP>0
            d=d+np.where(kick,1.,0.)[:,None]*s.G;last=np.where(kick,t,last);kicked=kick
            s.step(d);out[t]=s.st['previous'];s.prevP=p_events[t].astype(float)
        return out,last
    @staticmethod
    def rekick_features(spikes,last):
        """Per unit: latency from the reset spike of the last kick (step last+1) to the next spike, capped by the window end, whether it
        fired before the decision, and the time left after the last kick (shared, it sets the effective threshold)."""
        T,n,K=spikes.shape;t=np.arange(T)[:,None,None];after=spikes&(t>=(last+3)[None,:,None])
        first=np.where(after.any(0),np.argmax(after,axis=0)-(last+3)[:,None],T);left=(T-(last+3)).astype(float)
        return np.concatenate([first.astype(float),after.any(0).astype(float),left[:,None]],axis=1)
    def run_v1(s,drive,p_events,kick_at=None):
        out=np.zeros((len(drive),)+s.st['memory'].shape,bool)
        for t in range(len(drive)):
            d=(drive[t]-s.beta*s.prevP)[:,None]*np.ones(s.K)
            if kick_at is not None and t==kick_at:d=d+s.G
            if kick_at is not None and t==kick_at+1:d=d-(1-s.eps)*s.G
            s.st=advance(s.st,d,s.net,s.J);out[t]=s.st['previous'];s.prevP=p_events[t].astype(float)
        return out
    @staticmethod
    def latency_features(spikes,kick_at):
        """Steps from the kick's reset spike to the next spike, capped at the window end, and whether one occurred."""
        after=spikes[kick_at+3:];T=len(after);t=np.arange(T)[:,None,None];first=np.where(after.any(0),np.argmax(after,axis=0),T)
        return np.concatenate([first.astype(float),(first<T).astype(float)],axis=1)
