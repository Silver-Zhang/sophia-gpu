#!/usr/bin/env python3
"""Original schematic mechanisms, not measured or simulated research results.
Python/Matplotlib. All geometry and paths are pedagogical examples.
"""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import font_manager
ROOT=Path(__file__).resolve().parents[1]
from figure_style import configure,finish
configure()
BLUE='#24638d'; TEAL='#34877e'; INK='#203445'; LIGHT='#e2edf3'; GRAY='#a7b6c2'; WARM='#b76842'

def canvas(h):
    f,a=plt.subplots(figsize=(6.1,h));f.subplots_adjust(left=.015,right=.985,bottom=.025,top=.975);a.set(xlim=(0,100),ylim=(0,100));a.axis('off');return f,a

def text(a,x,y,s,size=9,**kw):a.text(x,y,s,ha=kw.pop('ha','center'),va='center',fontsize=size,color=INK,**kw)
def box(a,x,y,w,h,s,fc=LIGHT,size=9):
    a.add_patch(Rectangle((x,y),w,h,facecolor=fc,edgecolor=GRAY,lw=.8));text(a,x+w/2,y+h/2,s,size)
def arrow(a,x,y,u,v,c=BLUE,dash=False):
    a.add_patch(FancyArrowPatch((x,y),(u,v),arrowstyle='->',mutation_scale=10,color=c,lw=1,linestyle='--' if dash else '-'))
def save(f,name):
    finish(f,name)
    plt.close(f)

# Three horizontal rows with method names and essential geometric information only.
f,a=canvas(3.7)
text(a,2,96,'a  DDA',ha='left')
for i in range(6):
 for j in range(4):
    a.add_patch(Rectangle((2+i*4.3,71+j*5),4.3,5,
        fc=LIGHT if i<3 else '#e4efeb',ec=GRAY,lw=.6))
arrow(a,1,74,29,88)
for i in range(1,6):
 x=2+i*4.3;a.plot([x],[74+(x-1)/28*14],'.',color=WARM,ms=3)
text(a,34,85,'单元穿越',ha='left')
text(a,34,75,r'索引 $(i,j,k)$；区间 $[t_{\mathrm{in}},t_{\mathrm{out}}]$',ha='left')

text(a,2,64,'b  八叉树',ha='left')
for x,y,w,h in [(2,39,13,20),(15,49,13,10),(15,39,6.5,10),
                (21.5,39,6.5,5),(21.5,44,6.5,5)]:
 a.add_patch(Rectangle((x,y),w,h,fc=LIGHT,ec=GRAY,lw=.7))
arrow(a,1,42,29,56)
text(a,34,53,'叶单元定位',ha='left')
text(a,34,43,'编号、尺寸、材料',ha='left')

text(a,2,32,'c  BVH',ha='left')
for x,y,w,h in [(2,7,26,20),(4,10,10,14),(16,14,10,11)]:
 a.add_patch(Rectangle((x,y),w,h,fc='none',ec=GRAY,lw=.8))
a.plot([5,12,9,5],[12,14,22,12],color=TEAL,lw=1.2)
a.plot([18,25,22,18],[15,18,24,15],color=TEAL,lw=1.2)
arrow(a,1,10,29,24)
text(a,34,21,'候选面筛选与求交',ha='left')
text(a,34,11,'表面编号、交点参数',ha='left')
save(f,'dda_index')

# Causal links among numerical discretization, GPU execution and joint selection.
f,a=canvas(3.7)
box(a,1,77,28,18,r'RQ1 网格与离散 $\theta$'+'\n'+'材料界面 / 源区 / 求积')
box(a,36,77,28,18,'轨迹工作量\n访问数 / 段数 / 写入分布')
box(a,71,77,28,18,'RQ2 GPU参数 $s$\n缓存 / 分组 / 批次 / 求和')
arrow(a,29,86,35,86);arrow(a,65,86,70,86)
box(a,1,43,28,21,'CPU与参考解\n'+r'离散误差 $e_{\mathrm{disc}}$',fc='#e4efeb')
box(a,36,43,28,21,'同离散 CPU / GPU\n'+r'实现差异 $e_{\mathrm{impl}}$')
box(a,71,43,28,21,'执行成本\n'+r'$T$ / $M_{\mathrm{peak}}$')
for x in [15,50,85]:arrow(a,x,76,x,65)
arrow(a,29,53,35,53)
box(a,19,9,62,20,r'RQ3 联合选择 $(\theta,s)$'+'\n误差 / 显存约束')
for x in [15,50,85]:arrow(a,x,42,50 if x==50 else (30 if x<50 else 70),30)
save(f,'voxel_gpu_cost')
