"""Presentation only: read frozen summary; do not refit, simulate or reanalyse."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
s=json.loads((HERE.parent/'sources/HISTORY_COUPLING_CONFIRMATION_summary.json').read_text())
fig,ax=plt.subplots(2,2,figsize=(11,8),layout='constrained')
colors=['#125d56','#bd783a'];x=np.arange(2)
for i,(policy,label) in enumerate([('refit','Frozen learned readout'),('fixed','Fixed preparation')]):
 vals=[100*s['summary'][a][policy]['all7'] for a in ('B0','B2_once')]
 bars=ax[0,0].bar(x+(i-.5)*.35,vals,.34,label=label,color=colors[i]);ax[0,0].bar_label(bars,fmt='%.2f',padding=3,fontsize=9)
ax[0,0].set(xticks=x,xticklabels=['Normal T7','Past contribution\nremoved once'],ylim=(0,76),ylabel='Seven-step success (%)',title='a  Same substrates, different policies')
ax[0,0].legend(fontsize=9,frameon=False)
def contrasts(a,rows,title,xlim):
 for y,(label,d) in enumerate(rows):
  v=100*d['mean'];lo,hi=np.array(d['ci95'])*100
  a.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o',capsize=4,color=colors[0])
  a.annotate(f'{v:+.2f} [{lo:+.2f}, {hi:+.2f}]',(v,y),xytext=(0,12),textcoords='offset points',ha='center',fontsize=8)
 a.axvline(0,color='#aaaaaa',lw=1)
 a.set(yticks=range(len(rows)),yticklabels=[r[0] for r in rows],ylim=(len(rows)-.3,-.6),xlim=xlim,xlabel='Difference (percentage points)',title=title)
contrasts(ax[0,1],[('Primary',s['primary']),('Fixed',s['secondary']['fixed']),('Interaction',s['secondary']['interaction'])],'b  Primary criterion not met',(-20,25))
ax[0,1].axvline(3,color=colors[1],ls='--',lw=1)
ax[0,1].text(.97,.03,'Primary lower bound: +2.9883\nRequired: > +3 points',transform=ax[0,1].transAxes,ha='right',fontsize=8)
contrasts(ax[1,0],[('A = 0',s['secondary']['A0']),('A = 1',s['secondary']['A1'])],'c  Input-conditioned sign reversal',(-7,17))
y=np.arange(5);d=100*np.array(s['primary']['per_device'])
ax[1,1].barh(y,d,color=[colors[0] if v>=0 else colors[1] for v in d])
for i,v in enumerate(d):ax[1,1].text(v+(.15 if v>=0 else -.15),i,f'{v:+.2f}',va='center',ha='left' if v>=0 else 'right',fontsize=9)
ax[1,1].axvline(0,color='#aaaaaa',lw=1)
ax[1,1].set(yticks=y,yticklabels=[f'Circuit {i}' for i in range(200,205)],ylim=(4.6,-.6),xlim=(-4,10),xlabel='Difference (percentage points)',title='d  Circuit point estimates')
for a in ax.flat:a.spines[['top','right']].set_visible(False)
fig.suptitle('Retained history: conditional benefit, not uniform advantage',fontsize=15)
fig.supxlabel('Five fixed circuits; 128 history groups per circuit; two paired holds.\nPrimary analysis fixed before acquisition; no external preregistration. Secondary intervals are descriptive.',fontsize=9)
fig.savefig(HERE/'figure2_usable_memory.png',dpi=200);fig.savefig(HERE/'figure2_usable_memory.pdf')
