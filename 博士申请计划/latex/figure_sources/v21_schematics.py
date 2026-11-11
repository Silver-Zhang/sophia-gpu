#!/usr/bin/env python3
"""V2.1 planned-method diagrams. No measured data; 148.2 mm, black/white,
9 pt YaHei/Arial. Components and edges follow outline and main.tex. Python
source and live-text SVG retained. Each diagram has one role: route choice,
numerical dependencies, multi-GPU reduction, RQ connections and validation.
"""
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
from figure_style import configure,finish,ROOT
configure();plt.rcParams['svg.fonttype']='none'
def canvas(h):
 f,a=plt.subplots(figsize=(148.2/25.4,h));f.subplots_adjust(left=.015,right=.985,bottom=.03,top=.97)
 a.set(xlim=(0,100),ylim=(0,100));a.axis('off');return f,a
def box(a,x,y,w,h,t):
 a.add_patch(Rectangle((x,y),w,h,fc='white',ec='black',lw=.8))
 a.text(x+w/2,y+h/2,t,ha='center',va='center',linespacing=1.65)
def arrow(a,x,y,u,v,d=False):
 a.add_patch(FancyArrowPatch((x,y),(u,v),arrowstyle='->',mutation_scale=9,lw=.8,color='black',linestyle='--' if d else '-'))
def save(f,n):
 finish(f,n);v=ROOT/'figure_sources'/f'{n}.svg';f.savefig(v);v.write_text(re.sub(r'(font-size: [0-9.]+)px', r'\1', re.sub(r' transform="rotate\(-?0 [^"]+\)"', '', re.sub(r'<!DOCTYPE[^>]+>', '', v.read_text()))));plt.close(f)
f,a=canvas(2.25)
box(a,2,66,96,28,'多层材料与复杂孔道：中子能谱、区域通量、反应率')
for x,t in [(2,'MOC\n沿程积分'),(36,'体素与局部细化\n材料路径'),(70,'CPU–多 GPU\n扫描与归约')]:
 box(a,x,19,28,29,t);arrow(a,x+14,66,x+14,48)
a.text(50,3,'精度控制 → 异构效率 → 精度–成本协调',ha='center',va='center');save(f,'v21_route')
from moc_iteration import draw as draw_moc_iteration
draw_moc_iteration()
f,a=canvas(3.0);box(a,2,78,96,18,'CPU：几何/版本管理、任务划分与调度')
for x,t in [(3,'GPU 1'),(37,'GPU 2'),(71,'GPU p')]:
 box(a,x,40,26,25,t+'\n完整轨迹扫描');arrow(a,x+13,78,x+13,65);arrow(a,x+13,40,x+13,29)
a.plot([16,84],[29,29],color='black',lw=.8);arrow(a,50,29,50,23)
box(a,2,2,96,21,'PCIe / 可用 NVLink：通量归约\n源更新 → 下一轮扫描')
save(f,'v21_multi')
f,a=canvas(3.0)
box(a,2,70,43,25,'RQ1：材料路径与响应误差\n几何保护、富集缺陷、细化')
box(a,55,70,43,25,'RQ2：多 GPU 协同\n轨迹更新、缓存、负载与通信')
arrow(a,23.5,70,23.5,57);arrow(a,76.5,70,76.5,57)
box(a,2,38,96,19,'RQ3：误差 / 时间 / 显存预测 → 有限预算选择');arrow(a,50,38,50,27)
box(a,2,7,96,20,'独立几何与 FNS 验证：达标可靠性、完整成本、适用范围');save(f,'v21_research')
