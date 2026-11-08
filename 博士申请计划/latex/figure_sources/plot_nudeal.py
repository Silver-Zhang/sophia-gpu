"""Replot NuDEAL author manuscript arXiv:2607.01591v1, Table 6.
Question: how much memory is exchanged for sweep/MOC throughput?
64-angle full concurrency is OOM, not a zero-valued measurement.
Python backend; quantitative grid; 148 mm wide; editable PDF/SVG.
No uncertainty was reported in the source table; no error bars inferred.
"""
from pathlib import Path
import csv, sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
audit_dir = os.environ.get('NATURE_FIGURE_SCRIPTS')
if not audit_dir:
    audit_dir = str(Path.home()/'.codex/plugins/cache/nature-skills/nature-skills/0.1.0/skills/nature-figure/scripts')
sys.path.insert(0, audit_dir)
from audit_panel_alignment import require_matplotlib_panel_alignment
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','Helvetica','DejaVu Sans'],
    'font.size':8,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,
    'axes.spines.right':False,'axes.linewidth':0.7,'legend.frameon':False})
from figure_style import configure,finish
configure()
rows=list(csv.DictReader((ROOT/'references/nudeal_table6.csv').open()))
valid=[r for r in rows if r['sweep_s']]
x=list(range(len(valid))); labels=[r['angle_block_size'] for r in valid]
fig,axs=plt.subplots(1,2,figsize=(148/25.4,68/25.4))
fig.subplots_adjust(left=.10,right=.98,bottom=.23,top=.86,wspace=.56)
axs[0].plot(x,[float(r['memory_MB']) for r in valid],'-o',color='#315E84',lw=1.4,ms=4)
axs[0].set_ylabel('GPU memory (MB)');axs[0].set_ylim(0,8000);axs[0].set_yticks([0,2000,4000,6000,8000])
axs[1].plot(x,[float(r['moc_s']) for r in valid],'-o',color='#315E84',lw=1.4,ms=4,label='MOC step')
axs[1].plot(x,[float(r['sweep_s']) for r in valid],'-s',color='#AA7038',lw=1.4,ms=4,label='Transport sweep')
axs[1].set_ylabel('Time (s)');axs[1].set_ylim(0,12);axs[1].set_yticks([0,3,6,9,12])
axs[1].legend(loc='lower right',bbox_to_anchor=(1,.03),fontsize=7)
for ax,label in zip(axs,['a','b']):
    ax.set_xticks(x,labels);ax.set_xlabel('Angles per block')
    ax.text(-.17,1.12,label,transform=ax.transAxes,fontsize=9,fontweight='bold',va='bottom')
    ax.grid(False);ax.set_axisbelow(True)
finish(fig,'fig4_nudeal')
require_matplotlib_panel_alignment(fig,json_out=str(ROOT/'qa/fig4_nudeal.alignment.json'),
 tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True)
plt.close(fig)
