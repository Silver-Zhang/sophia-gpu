"""Source-grounded geometry and response plates for section 4.2.
Run with NATURE_FIGURE_QA_SCRIPTS pointing to the nature-figure scripts directory.
Input values and image rights are recorded in benchmark_visuals/sources.json.
"""
from pathlib import Path
import os,sys,json,itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle
from matplotlib.text import Text
from figure_style import configure,finish,WIDTH_MM,FONT_PT
HERE=Path(__file__).resolve().parent;DATA=HERE/'benchmark_visuals'
QA=Path(os.environ['NATURE_FIGURE_QA_SCRIPTS']);sys.path.insert(0,str(QA))
from audit_panel_alignment import require_matplotlib_panel_alignment
configure()
plt.rcParams.update({'font.family':['Arial','Microsoft YaHei'],'font.size':9.03375,'svg.fonttype':'none','pdf.fonttype':42})
FACTS=json.loads((DATA/'geometry_parameters.json').read_text())
OUT=Path(os.environ.get('BENCHMARK_QA_OUT','/tmp/benchmark-figure-qa'));OUT.mkdir(exist_ok=True)

def check(fig,name,**kw):
    for text in fig.findobj(match=Text):
        text.set_fontfamily(['Arial','Microsoft YaHei']);text.set_fontsize(FONT_PT)
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig,json_out=OUT/(name+'.alignment.json'),strict=True,**kw)
    fig.savefig(HERE.parent/'figures'/(name+'.pdf'),backend='pgf')
    fig.savefig(HERE/(name+'.svg'))
    plt.close(fig)

def box(ax,limits,fill=False,hatch=None):
    x,y,z=limits
    v=np.array(list(itertools.product(x,y,z)),float)
    xy=np.c_[v[:,0]+.43*v[:,1],v[:,2]+.35*v[:,1]]
    if fill:
        for ids in [[0,1,3,2],[0,1,5,4],[1,3,7,5]]:
            ax.add_patch(Polygon(xy[ids],facecolor='white',edgecolor='black',linewidth=.65,hatch=hatch))
    else:
        for i,j in itertools.combinations(range(8),2):
            if sum(v[i]!=v[j])==1:ax.plot(*xy[[i,j]].T,color='black',lw=.6)
    return xy

def geometry_plate():
    fig=plt.figure(figsize=(WIDTH_MM/25.4,89/25.4))
    a=fig.add_axes([.015,.08,.465,.81],label='a');b=fig.add_axes([.52,.08,.465,.81],label='b')
    for ax in [a,b]:ax.set_axis_off()
    a.set_xlim(-9,119);a.set_ylim(-16,108)
    box(a,[[0,60],[0,100],[0,60]])
    # Four orthogonal void prisms, from OECD figures 5–8, retain the three bends.
    for limits in reversed(FACTS['Kobayashi']['void_boxes_cm']):box(a,limits,True)
    box(a,FACTS['Kobayashi']['source_box_cm'],True,'////')
    a.annotate('源区',xy=(6,7),xytext=(8,-10),ha='center',arrowprops={'arrowstyle':'-','lw':.6})
    a.annotate('近真空孔道',xy=(58,25),xytext=(85,4),ha='center',arrowprops={'arrowstyle':'-','lw':.6})
    a.text(60,101,'屏蔽区',ha='center',va='center')
    a.text(27,-6,'x',ha='center');a.text(110,30,'y',ha='center');a.text(-5,65,'z',ha='center')
    a.text(56,88,'60 cm',ha='center');a.text(113,67,'100 cm',rotation=90,ha='center',va='center',rotation_mode='anchor')
    image=plt.imread(DATA/'fng_streaming_fig3.png')
    w,h=fig.get_size_inches();ih=(.465*w/(.81*h))*(image.shape[0]/image.shape[1])
    b.imshow(image,extent=[0,1,.5-ih/2,.5+ih/2],aspect='auto',interpolation='none',resample=False)
    b.set_xlim(0,1);b.set_ylim(0,1)
    fig.text(.015,.955,'(a) Kobayashi折弯孔道',va='top',fontsize=FONT_PT)
    fig.text(.52,.955,'(b) FNG-ITER流束模型',va='top',fontsize=FONT_PT)
    check(fig,'benchmark_geometries',panel_ids={a:'a',b:'b'},row_groups=[['a','b']],column_groups=[])

def response_plate():
    fig=plt.figure(figsize=(WIDTH_MM/25.4,107/25.4))
    a=fig.add_axes([.015,.12,.44,.76],label='a');a.set_axis_off();a.set_xlim(-15,55);a.set_ylim(-37,37)
    a.add_patch(Rectangle((0,-23.425),49,46.85,facecolor='white',edgecolor='black',lw=.8))
    a.add_patch(Rectangle((0,-3.5),49,7,facecolor='white',edgecolor='black',lw=.65))
    a.plot([-5.3,49],[0,0],color='black',lw=.65,ls='--')
    a.plot(-5.3,0,'o',color='black',ms=3)
    a.annotate('D-T源',xy=(-5.3,0),xytext=(-7,11),ha='center',arrowprops={'arrowstyle':'-','lw':.6})
    a.text(24.5,15,'钨合金屏蔽体',ha='center')
    for x in [5,15,25,35]:
        a.plot([x,x],[-2.8,2.8],color='black',lw=1.5)
        a.plot([x,x],[-23.425,-25],color='black',lw=.6)
        a.text(x,-27,str(x),ha='center',va='top')
    a.annotate('活化箔',xy=(35,0),xytext=(27,-13),ha='center',arrowprops={'arrowstyle':'-','lw':.6})
    a.text(24.5,-34,'近似深度 / cm',ha='center')
    a.annotate('',xy=(0,29),xytext=(49,29),arrowprops={'arrowstyle':'|-|','lw':.65})
    a.text(24.5,31,'49 cm',ha='center')
    a.text(-9,-16,'源距\n5.3 cm',ha='center')
    # Spectrum and C/E values are recovered independently from the same published figure.
    s=fig.add_axes([.615,.49,.36,.35],label='spectrum');c=fig.add_axes([.615,.19,.36,.20],label='ce')
    exp=np.genfromtxt(DATA/'jeff_cu_experiment.csv',delimiter=',',names=True)
    calc=np.genfromtxt(DATA/'jeff_cu_mcnp.csv',delimiter=',',names=True)
    ce=np.genfromtxt(DATA/'jeff_cu_ce.csv',delimiter=',',names=True)
    assert np.all(exp['lower']<=exp['spectrum'])and np.all(exp['upper']>=exp['spectrum'])
    assert np.all(exp['energy_MeV']>0)and np.all(exp['spectrum']>0)and np.all(calc['spectrum']>0)
    s.errorbar(exp['energy_MeV'],exp['spectrum'],yerr=[exp['spectrum']-exp['lower'],exp['upper']-exp['spectrum']],fmt='o',ms=1.5,mfc='white',mec='black',mew=.4,ecolor='black',elinewidth=.4,capsize=0,label='Experiment')
    for i,r in enumerate(calc):s.plot([r['energy_low_MeV'],r['energy_high_MeV']],[r['spectrum']]*2,color='black',lw=.65,label='MCNP / JEFF-3.1'if i==0 else None)
    s.set_xscale('log');s.set_yscale('log');s.set_xlim(.1,20);s.set_ylim(.008,1.4)
    s.set_ylabel('Leakage / lethargy\n(cm$^{-2}$ source$^{-1}$)',fontsize=FONT_PT)
    s.legend(loc='upper left',bbox_to_anchor=(-.03,1.22),frameon=False,fontsize=FONT_PT,handlelength=1.4,labelspacing=.22,borderaxespad=0)
    s.tick_params(axis='x',labelbottom=False)
    unc=np.genfromtxt(DATA/'jeff_cu_benchmark_uncertainty.csv',delimiter=',',names=True)
    c.fill_between(unc['energy_MeV'],unc['lower_CE'],unc['upper_CE'],facecolor='.86',edgecolor='none',label='Experiment error')
    c.legend(loc='upper left',frameon=False,fontsize=FONT_PT,handlelength=1,borderaxespad=.15)
    c.errorbar(ce['energy_MeV'],ce['CE'],yerr=[ce['CE']-ce['lower'],ce['upper']-ce['CE']],fmt='+',ms=2,mew=.45,color='black',elinewidth=.4,capsize=0)
    c.axhline(1,color='black',lw=.6,ls='--');c.set_xscale('log');c.set_xlim(.1,20);c.set_ylim(0,2);c.set_yticks([0,1,2]);c.set_ylabel('C/E');c.set_xlabel('Energy / MeV')
    for ax in [s,c]:
        ax.spines[['top','right']].set_visible(False);ax.tick_params(direction='out',width=.6,length=2);ax.minorticks_off();ax.set_xticks([.1,1,10],['0.1','1','10'])
    fig.text(.015,.97,'(a) FNG钨合金中央剖面示意',va='top',fontsize=FONT_PT)
    fig.text(.53,.97,'(b) OKTAVIAN铜球泄漏谱',va='top',fontsize=FONT_PT)
    check(fig,'benchmark_responses',panel_ids={a:'a',s:'spectrum',c:'ce'},row_groups=[],column_groups=[['spectrum','ce']],exemptions=[{'panels':['a'],'checks':['all'],'reason':'Geometry panel spans the independent spectrum and C/E rows; no shared quantitative axis.'}])

if __name__=='__main__':geometry_plate();response_plate()
