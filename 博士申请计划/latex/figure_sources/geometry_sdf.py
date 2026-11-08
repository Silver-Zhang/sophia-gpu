"""Redraw of Shriwise et al. (2017), DOI 10.1016/j.net.2017.08.008, Table 1.
Contract: same-study wall times reveal SDF query savings and residual CAD overhead.
Single-panel quantitative comparison. No timing-repeat uncertainty reported in source.
Source data: ../references/shriwise2017_table1.csv. All three implementations retained.
"""
from pathlib import Path
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({'font.family':'Arial','font.size':9,'axes.labelsize':9,'xtick.labelsize':9,'ytick.labelsize':9,'pdf.fonttype':42,'svg.fonttype':'none','savefig.dpi':300})
from figure_style import configure,finish
configure()
root=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((root/'references/shriwise2017_table1.csv').open()))
fig,ax=plt.subplots(figsize=(5.2,2.25))
fig.subplots_adjust(left=.32,right=.96,bottom=.26,top=.95)
values=[float(r['wall_time_min']) for r in rows]
ax.barh([0,1,2],values,height=.53,color=['#A0A4A8','#A0A4A8','#527D8E'])
ax.set_yticks([0,1,2],['MCNP5 (analytic CSG)','DAG-MCNP5','DAG-MCNP5 + SDF'])
ax.invert_yaxis();ax.set_xlim(0,30);ax.set_xticks([0,5,10,15,20,25,30]);ax.set_xlabel('Wall time (min)')
ax.spines[['top','right']].set_visible(False)
ax.tick_params(axis='y',length=0)
ax.text(25.13+.6,1,'25.13',va='center',fontsize=9)
ax.text(7.3+.6,2,'7.30',va='center',fontsize=9)
finish(fig,'geometry_sdf')
plt.close(fig)
