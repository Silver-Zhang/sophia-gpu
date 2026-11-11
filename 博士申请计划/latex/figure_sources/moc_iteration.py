#!/usr/bin/env python3
"""Fixed-source MOC source iteration: planned numerical baseline, no data.

Brief/contract: one panel, 148.2 mm, black lines and text on white, 9 PDF pt.
Fixed vacuum boundary, precomputed segments, group-Jacobi baseline. Geometry
is a fixed input, not an iteration task. Phi denotes retained angular moments;
S includes group/angle neutron transfer. Convergence uses new-solution physical
balance plus flux/response changes, never frozen-source sweep balance.
"""
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,FancyArrowPatch
from figure_style import configure,finish,ROOT

def draw():
 configure();plt.rcParams['svg.fonttype']='none'
 f,a=plt.subplots(figsize=(148.2/25.4,4.1));f.subplots_adjust(left=.01,right=.99,bottom=.01,top=.99)
 a.set(xlim=(0,100),ylim=(-6,101));a.axis('off')
 def box(x,y,w,h,t,gid):
  p=Rectangle((x,y),w,h,fc='white',ec='black',lw=.8);p.set_gid(gid);a.add_patch(p)
  a.text(x+w/2,y+h/2,t,ha='center',va='center',linespacing=1.7,gid=gid+'-text')
 def edge(x,y,u,v,gid):
  p=FancyArrowPatch((x,y),(u,v),arrowstyle='->',mutation_scale=9,lw=.8,color='black');p.set_gid(gid);a.add_patch(p)
 # A single top-to-bottom main path; fixed inputs left, feedback right.
 box(34,87,42,12,'初始化\n$\\Phi^{(0)}=0,\\ i=0$','initial-state')
 box(2,47,24,24,'预先构建\n材料段、源区\n权重与截面','fixed-discretization')
 box(34,71,42,12,'构造总角源\n$Q^{(i+1)}=q+\\mathcal{S}\\Phi^{(i)}$','source-update')
 box(34,53,42,12,'固定总源逐段扫描\n$\\psi_{\\rm out},\\ \\bar\\psi,\\ J_{\\rm out}$','track-sweep')
 box(34,35,42,12,'空间与角向求积\n$\\Phi^{(i+1)},\\ R^{(i+1)}$','volume-angle-tally')
 edge(55,87,55,83,'initial-to-source')
 edge(26,59,34,59,'fixed-to-sweep')
 edge(55,71,55,65,'source-to-sweep')
 edge(55,53,55,47,'sweep-to-tally')
 edge(55,35,55,29,'tally-to-test')
 diamond=Polygon([(37,20),(55,29),(73,20),(55,11)],closed=True,fc='white',ec='black',lw=.8)
 diamond.set_gid('convergence-test');a.add_patch(diamond)
 a.text(55,20,'通量/响应/平衡\n均满足阈值？',ha='center',va='center',linespacing=1.6,gid='convergence-text')
 box(82,46,16,12,'$i\\leftarrow i+1$','iteration-advance')
 box(34,-5,42,8,'输出收敛响应','converged-output')
 edge(55,11,55,3,'yes-to-output')
 a.text(60,7,'是',ha='center',va='center')
 # The no branch remains entirely outside the main sequence.
 a.plot([73,90,90],[20,20,40],color='black',lw=.8,gid='no-route')
 edge(90,40,90,46,'no-to-advance')
 a.text(79,23,'否',ha='center',va='center')
 a.plot([90,90,82],[58,77,77],color='black',lw=.8,gid='feedback-route')
 edge(82,77,76,77,'advance-to-source')
 finish(f,'v21_moc')
 v=ROOT/'figure_sources'/'v21_moc.svg';f.savefig(v)
 v.write_text(re.sub(r'(font-size: [0-9.]+)px',r'\1',re.sub(r' transform="rotate\(-?0 [^"]+\)"','',re.sub(r'<!DOCTYPE[^>]+>','',v.read_text()))))
 plt.close(f)

if __name__=='__main__':draw()
