"""Recompute figure values from the 1,152 preserved trial records."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT/'results/otb21_readiness_history_validation/history_20261105/records.json').read_text())
assert len(rows) == 1152
policies = ['usual', 'fixed4096', 'guard']
labels = ['Immediate update', 'Fixed wait (4,096)', 'State-based wait']
budgets = [1536, 2048, 4096]
fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout='constrained')
for i, (policy,label,color) in enumerate(zip(policies, labels, ['#8793a5','#df9a33','#267d80'])):
    groups = [[r for r in rows if r['policy']==policy and r['budget']==b] for b in budgets]
    assert all(len(g)==128 for g in groups)
    assert all(r['current_context_correct'] for g in groups for r in g)
    retained = [100*sum(r['untouched_operation1_correct'] for r in g)/len(g) for g in groups]
    cost = [np.mean([r['total_live_steps'] for r in g]) for g in groups]
    x = np.arange(3)+(i-1)*.24
    axes[0].bar(x,retained,width=.23,label=label,color=color)
    axes[1].bar(x,cost,width=.23,label=label,color=color)
    print(label, 'retention %:',retained,'mean total steps:',cost)
for ax in axes:
    ax.set_xticks(range(3), [f'{b:,}' for b in budgets]); ax.set_xlabel('Query duration (simulation steps)')
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Old relation retained (%)'); axes[0].set_ylim(0,115)
axes[1].set_ylabel('Total simulation steps'); axes[1].legend(fontsize=8)
fig.suptitle('New relation learned in every condition; retention costs time')
(ROOT/'figures').mkdir(exist_ok=True)
fig.savefig(ROOT/'figures/retention-cost.png',dpi=170)
fig.savefig(ROOT/'figures/retention-cost.svg')
