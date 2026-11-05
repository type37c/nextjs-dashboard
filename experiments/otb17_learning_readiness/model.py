"""OTB17 query dynamics: OTB15 core with explicitly selectable preparation.

Queries have no label input. Supplied memories and working states are copied;
counterfactual candidate trials therefore cannot update a live learner. The T7
recurrence, bistable polynomial, residual e/s dynamics and readout coupling are
the OTB15 equations. Preparation changes only an external current into work T7s.
"""
from pathlib import Path
import math
import sys
import numpy as np

try:
    from numba import njit
except ImportError:
    fallback = Path(__file__).resolve().parents[2] / '.cache/oscillator-night-pydeps'
    if fallback.exists():
        sys.path.insert(0, str(fallback))
    from numba import njit

EPS = 6.5e-5
BETA = .6
KAPPA = .025
OMEGA = 2*np.pi/258
R = 512
NU = 1e-4
WC = 2*np.pi/595
CHI = .001
SCALE = .25
MC = -.43071203972028016
G = .00015
LOW = 2-1/np.sqrt(3)
HIGH = 2+1/np.sqrt(3)
DEFAULT = dict(alpha=6., tau_e=6000., tau_s=1000., hold_eta=.1,
               gain=.3, competition=1., noise=0.)
CFG_KEYS = ('alpha', 'tau_e', 'tau_s', 'hold_eta', 'gain', 'competition')
STAT_NAMES = ('min_u', 'max_u', 'min_tilt', 'max_tilt',
              'max_eligibility', 'max_abs_accumulator', 'max_abs_work_m')


def config_array(config=None):
    value = dict(DEFAULT)
    if config is not None:
        value.update(config)
    if value.get('noise', 0.) != 0.:
        raise ValueError('This deterministic query engine does not implement noise.')
    cfg = np.asarray([value[k] for k in CFG_KEYS], dtype=np.float64)
    if not np.isfinite(cfg).all() or cfg[1] <= 0 or cfg[2] <= 0:
        raise ValueError('Finite coefficients and positive trace time constants required.')
    return cfg


@njit(cache=True)
def radial(u, h):
    v = u-2.
    return 2.*NU*u*(v-v*v*v+h)


@njit(cache=True)
def band(u):
    if u <= LOW:
        return -1
    if u >= HIGH:
        return 1
    return 0


def memory_bands(mem):
    u = np.asarray(mem)[..., 3]
    return np.where(u <= LOW, -1, np.where(u >= HIGH, 1, 0)).astype(np.int8)


def decode(counts):
    hit = np.asarray(counts)[..., 1:] > 0
    return np.where(hit.sum(axis=-1) == 1, hit.argmax(axis=-1), -1)


@njit(cache=True)
def _query(mem, work, pair, steps, cue, prep_strength, prep_mask, cut, cfg, record, cue_impulse):
    alpha, tau_e, tau_s, hold_eta, gain, competition = cfg
    decay = math.exp(-1./tau_e)
    counts = np.zeros(3, np.int64)
    pre_counts = np.zeros(3, np.int64)
    output_before_source = np.zeros(2, np.int64)
    source_has_fired_after_cue = False
    first = np.full(3, -1, np.int64)
    # Compatible with the original OTB15 record columns: states, h, drives, events.
    trace = np.empty((steps if record else 0, 82), np.float64)
    stats = np.array([np.inf, -np.inf, np.inf, -np.inf, 0., 0., 0.])
    initial_bands = np.empty(8, np.int8)
    final_bands = np.empty(8, np.int8)
    band_preserved = np.ones(8, np.bool_)
    for c in range(8):
        initial_bands[c] = band(mem[c, 3])
    effort = 0.
    all_finite = True
    positive_u = True
    for t in range(steps):
        old_prev = work[0, 3]
        coupling0 = 0.
        coupling1 = 0.
        if not cut:
            u0 = mem[2*pair, 3]
            u1 = mem[2*pair+1, 3]
            coupling0 = gain*max(u0-1., 0.)
            coupling1 = gain*max(u1-1., 0.)
            if competition > 0.:
                coupling0 *= min(1., max(0., (3.-u1)/2.))
                coupling1 *= min(1., max(0., (3.-u0)/2.))
        drives = np.empty(3, np.float64)
        fired = np.zeros(3, np.int64)
        for j in range(3):
            d = EPS*(-1.2)
            if t < cue and prep_mask[j]:
                prep = prep_strength*(-1.2-work[j, 0])
                d += prep
                effort += abs(prep)
            if t == cue and j == 0:
                d += cue_impulse
            if j == 1:
                d += old_prev*coupling0
            if j == 2:
                d += old_prev*coupling1
            drives[j] = d
            m, p, cd = work[j, :3]
            pn = p+OMEGA+KAPPA*m
            f = pn >= 2.*math.pi and cd == 0.
            work[j, 0] = (1.-EPS)*m+d-BETA*int(f)
            work[j, 1] = 0. if f else pn % (2.*math.pi)
            work[j, 2] = R if f else max(cd-1., 0.)
            work[j, 3] = 1. if f else 0.
            fired[j] = int(f)
            if f:
                if t >= cue:
                    counts[j] += 1
                    if first[j] < 0:
                        first[j] = t
                    if j > 0 and not source_has_fired_after_cue:
                        output_before_source[j-1] += 1
                else:
                    pre_counts[j] += 1
            stats[6] = max(stats[6], abs(work[j, 0]))
            for k in range(4):
                all_finite = all_finite and math.isfinite(work[j, k])
        if t >= cue and fired[0]:
            source_has_fired_after_cue = True
        hs = np.empty(8, np.float64)
        for c in range(8):
            m, p, cd, u, psi, e, s = mem[c]
            e *= decay
            if fired[0] and c//2 == pair:
                e = 1.
            # delta = 0 during a query: residual accumulator still relaxes.
            s += (e*0.-s)/tau_s
            signal = math.tanh((m-MC)/SCALE)
            h = hold_eta*signal+alpha*s
            hs[c] = h
            k1 = radial(u, h)
            k2 = radial(u+.5*k1, h)
            k3 = radial(u+.5*k2, h)
            k4 = radial(u+k3, h)
            un = u+(k1+2*k2+2*k3+k4)/6.
            pn = p+OMEGA+KAPPA*m
            f = pn >= 2.*math.pi and cd == 0.
            mem[c, 0] = (1.-EPS)*m+.001+G*math.sqrt(max(u, 0.))*math.cos(psi)-BETA*int(f)
            mem[c, 1] = 0. if f else pn % (2.*math.pi)
            mem[c, 2] = R if f else max(cd-1., 0.)
            mem[c, 3] = un
            mem[c, 4] = (psi+WC+CHI*signal) % (2.*math.pi)
            mem[c, 5] = e
            mem[c, 6] = s
            stats[0] = min(stats[0], un)
            stats[1] = max(stats[1], un)
            stats[2] = min(stats[2], h)
            stats[3] = max(stats[3], h)
            stats[4] = max(stats[4], abs(e))
            stats[5] = max(stats[5], abs(s))
            positive_u = positive_u and un > 0.
            band_preserved[c] = band_preserved[c] and band(un) == initial_bands[c]
            for k in range(7):
                all_finite = all_finite and math.isfinite(mem[c, k])
        if record:
            trace[t, :56] = mem.reshape(56)
            trace[t, 56:68] = work.reshape(12)
            trace[t, 68:76] = hs
            trace[t, 76:79] = drives
            trace[t, 79:82] = fired
    for c in range(8):
        final_bands[c] = band(mem[c, 3])
    return (counts, first, pre_counts, effort, initial_bands, final_bands,
            band_preserved, stats, all_finite, positive_u, trace, output_before_source)


def _inputs(mem, work):
    mm = np.asarray(mem, dtype=np.float64).copy()
    ww = np.asarray(work, dtype=np.float64).copy()
    if mm.shape != (8, 7) or ww.shape != (3, 4):
        raise ValueError('Expected memory (8,7) and work state (3,4).')
    if not np.isfinite(mm).all() or not np.isfinite(ww).all() or np.any(mm[:, 3] <= 0):
        raise ValueError('States must be finite with positive companion amplitudes.')
    if np.any(mm[:, 2] < 0) or np.any(ww[:, 2] < 0):
        raise ValueError('Refractory states must be nonnegative.')
    return mm, ww


def query(mem, work, pair, steps, cue_step=1024, prep_strength=.01,
          prep_mask=(True, True, True), memory_cut=False, config=None, record=False,
          cue_impulse=.6):
    """One diagnostic query, with total budget including preparation.

    `first` uses query-start coordinates, so it includes preparation latency.
    `effort` is summed absolute added preparation current, not physical energy.
    `band_preserved` checks the initial three-way band at every native step;
    a band crossing during residual s relaxation can therefore fail preservation.
    `output_before_source` counts post-cue output events without a strictly earlier
    post-cue source event (including output simultaneous with the first source).
    Setting `cue_impulse=0` is an explicit source-cue-cut diagnostic.
    """
    mm, ww = _inputs(mem, work)
    steps, cue, pair = int(steps), int(cue_step), int(pair)
    mask = np.asarray(prep_mask, dtype=np.bool_)
    if steps <= 0 or not 0 <= cue < steps or not 0 <= pair < 4:
        raise ValueError('Require steps>0, 0<=cue<steps, 0<=pair<4.')
    if mask.shape != (3,) or not math.isfinite(prep_strength) or prep_strength < 0:
        raise ValueError('Require 3-node mask and nonnegative finite prep strength.')
    if not math.isfinite(cue_impulse) or cue_impulse < 0:
        raise ValueError('Require a nonnegative finite cue impulse.')
    r = _query(mm, ww, pair, steps, cue, float(prep_strength), mask,
               bool(memory_cut), config_array(config), bool(record), float(cue_impulse))
    counts, first, pre_counts, effort, before, after, preserved, stats, finite, positive, trace, early = r
    if not finite or not positive:
        raise FloatingPointError('Non-finite state or nonpositive amplitude during query.')
    return dict(counts=counts, first=first, pre_counts=pre_counts,
                output_before_source=early,
                pred=int(decode(counts)), final_mem=mm, final_work=ww,
                effort=float(effort), band_before=before, band_after=after,
                band_preserved=preserved, stats=dict(zip(STAT_NAMES, stats.tolist())),
                all_finite=bool(finite), positive_u=bool(positive), trace=trace)


@njit(cache=True)
def _batch(mems, works, pairs, steps, cues, strengths, masks, cuts, cfg, cue_impulses):
    n = len(pairs)
    counts = np.empty((n, 3), np.int64)
    first = np.empty((n, 3), np.int64)
    pre_counts = np.empty((n, 3), np.int64)
    output_before_source = np.empty((n, 2), np.int64)
    efforts = np.empty(n)
    before = np.empty((n, 8), np.int8)
    after = np.empty((n, 8), np.int8)
    preserved = np.empty((n, 8), np.bool_)
    stats = np.empty((n, 7))
    finite = np.empty(n, np.bool_)
    positive = np.empty(n, np.bool_)
    for i in range(n):
        r = _query(mems[i], works[i], pairs[i], steps, cues[i], strengths[i],
                   masks[i], cuts[i], cfg, False, cue_impulses[i])
        counts[i], first[i], pre_counts[i] = r[0], r[1], r[2]
        efforts[i], before[i], after[i], preserved[i] = r[3], r[4], r[5], r[6]
        stats[i], finite[i], positive[i] = r[7], r[8], r[9]
        output_before_source[i] = r[11]
    return counts, first, pre_counts, efforts, before, after, preserved, stats, finite, positive, output_before_source


def query_batch(mems, works, pairs, steps, cues, prep_strengths,
                prep_masks, cuts=None, config=None, cue_impulses=None):
    """Independent candidate queries from input copies, with one total budget.

    All arrays carry a leading trial axis. The caller explicitly expands a saved
    boundary over candidates; this function never returns labels or selects a
    winning preparation. Raw diagnostics are returned for offline scoring.
    """
    mm = np.asarray(mems, dtype=np.float64).copy()
    ww = np.asarray(works, dtype=np.float64).copy()
    pp = np.asarray(pairs, dtype=np.int64)
    cc = np.asarray(cues, dtype=np.int64)
    ss = np.asarray(prep_strengths, dtype=np.float64)
    masks = np.asarray(prep_masks, dtype=np.bool_)
    n, steps = len(pp), int(steps)
    cuts = np.zeros(n, dtype=np.bool_) if cuts is None else np.asarray(cuts, dtype=np.bool_)
    impulses = np.full(n, .6) if cue_impulses is None else np.asarray(cue_impulses, dtype=np.float64)
    if (mm.shape != (n, 8, 7) or ww.shape != (n, 3, 4) or
            pp.shape != (n,) or cc.shape != (n,) or ss.shape != (n,) or
            masks.shape != (n, 3) or cuts.shape != (n,) or impulses.shape != (n,)):
        raise ValueError('Incompatible batch dimensions.')
    if n == 0 or steps <= 0 or np.any((pp < 0) | (pp >= 4)) or np.any((cc < 0) | (cc >= steps)):
        raise ValueError('Empty batch or invalid pair/cue/step value.')
    if (not np.isfinite(mm).all() or not np.isfinite(ww).all() or
            not np.isfinite(ss).all() or np.any(ss < 0) or np.any(mm[:, :, 3] <= 0)):
        raise ValueError('Non-finite input, negative preparation or nonpositive amplitude.')
    if np.any(mm[:, :, 2] < 0) or np.any(ww[:, :, 2] < 0):
        raise ValueError('Refractory states must be nonnegative.')
    if not np.isfinite(impulses).all() or np.any(impulses < 0):
        raise ValueError('Require nonnegative finite cue impulses.')
    r = _batch(mm, ww, pp, steps, cc, ss, masks, cuts, config_array(config), impulses)
    counts, first, pre_counts, effort, before, after, preserved, stats, finite, positive, early = r
    if not finite.all() or not positive.all():
        raise FloatingPointError('Non-finite state or nonpositive amplitude in batch.')
    return dict(counts=counts, first=first, pre_counts=pre_counts, pred=decode(counts),
                output_before_source=early,
                final_mem=mm, final_work=ww, effort=effort, band_before=before,
                band_after=after, band_preserved=preserved, stats=stats,
                stat_names=STAT_NAMES, all_finite=finite, positive_u=positive)
