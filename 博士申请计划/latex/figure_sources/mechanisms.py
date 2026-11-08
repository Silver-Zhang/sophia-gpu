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

# DDA: all three operations take a ray but return different geometric entities.
f,a=canvas(3.5)
for x,label in [(1,'a  均匀体素 / DDA'),(35,'b  层级叶单元'),(69,'c  BVH面元候选')]:text(a,x+14,94,label,10)
for i in range(6):
 for j in range(4):
    a.add_patch(Rectangle((2+i*5,51+j*8),5,8,fc=LIGHT if i<3 else '#e4efeb',ec=GRAY,lw=.6))
arrow(a,0,55,33,78)
for i in range(1,6):a.plot([2+i*5],[55+(2+i*5)/33*23],'.',color=WARM,ms=4)
text(a,16,43,'选取最近的网格面',9)
text(a,16,32,'更新单元索引与区间',9)
text(a,16,17,'单元索引 (i, j, k)，区间 [t入, t出]',8)
# quadtree slice as 3D octree pedagogical section
for x,y,w,h in [(36,51,15,32),(51,67,15,16),(51,51,7.5,16),(58.5,51,7.5,8),(58.5,59,7.5,8)]:
 a.add_patch(Rectangle((x,y),w,h,fc=LIGHT,ec=GRAY,lw=.7))
arrow(a,34,55,68,78)
text(a,51,43,'逐层找到穿过的叶单元',9)
text(a,51,32,'按单元尺寸计算下一交点',9)
text(a,51,17,'叶单元编号、尺寸与材料',8)
# BVH boxes/triangle faces ray
for x,y,w,h in [(70,51,28,32),(72,56,11,20),(85,62,11,17)]:a.add_patch(Rectangle((x,y),w,h,fc='none',ec=GRAY,lw=.8))
a.plot([74,80,77,74],[58,63,73,58],color=TEAL,lw=1.2)
a.plot([87,94,91,87],[64,67,77,64],color=TEAL,lw=1.2)
arrow(a,69,55,99,78)
text(a,84,43,'先筛包围盒，再求交',9)
text(a,84,32,'交点排序与内外判定',9)
text(a,84,17,'表面编号与交点参数',8)
text(a,50,3,'射线起点 r0 与方向 Ω',9)
save(f,'dda_index')

# Causal links among numerical discretization, GPU execution and joint selection.
f,a=canvas(3.7)
box(a,1,77,28,18,'RQ1 网格与离散 θ\n材料界面 / 源区 / 求积')
box(a,36,77,28,18,'轨迹工作量\n访问数 / 段数 / 写入分布')
box(a,71,77,28,18,'RQ2 GPU参数 s\n缓存 / 分组 / 批次 / 求和')
arrow(a,29,86,35,86);arrow(a,65,86,70,86)
box(a,1,43,28,21,'CPU参考响应\n材料路径与源近似\n离散误差 e_disc',fc='#e4efeb')
box(a,36,43,28,21,'GPU响应\n同离散 CPU / GPU\n实现差异 e_impl')
box(a,71,43,28,21,'时间与峰值显存\n扫描 / 访存 / 传输\n求和 / 源更新')
for x in [15,50,85]:arrow(a,x,76,x,65)
arrow(a,29,53,35,53)
box(a,19,9,62,20,'RQ3 网格与GPU参数联合选择\n离散精度、实现一致性与显存约束\n成本预测 / 参数搜索 / 独立几何检验')
for x in [15,50,85]:arrow(a,x,42,50 if x==50 else (30 if x<50 else 70),30)
save(f,'voxel_gpu_cost')
