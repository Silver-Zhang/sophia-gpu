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
text(a,16,43,'选最小下一面参数',9)
text(a,16,32,'更新单元索引与区间',9)
text(a,16,17,'输出：(i, j, k), [t入, t出]',8)
# quadtree slice as 3D octree pedagogical section
for x,y,w,h in [(36,51,15,32),(51,67,15,16),(51,51,7.5,16),(58.5,51,7.5,8),(58.5,59,7.5,8)]:
 a.add_patch(Rectangle((x,y),w,h,fc=LIGHT,ec=GRAY,lw=.7))
arrow(a,34,55,68,78)
text(a,51,43,'父子索引定位所交叶',9)
text(a,51,32,'按局部尺度推进区间',9)
text(a,51,17,'输出：叶号、尺度、材料',8)
# BVH boxes/triangle faces ray
for x,y,w,h in [(70,51,28,32),(72,56,11,20),(85,62,11,17)]:a.add_patch(Rectangle((x,y),w,h,fc='none',ec=GRAY,lw=.8))
a.plot([74,80,77,74],[58,63,73,58],color=TEAL,lw=1.2)
a.plot([87,94,91,87],[64,67,77,64],color=TEAL,lw=1.2)
arrow(a,69,55,99,78)
text(a,84,43,'先筛包围盒，再求交',9)
text(a,84,32,'交点排序与内外判定',9)
text(a,84,17,'输出：表面号、交点参数',8)
text(a,50,3,'共同输入：起点 r0、方向 Ω；真空区间也须保留传播与边界信息',9)
save(f,'dda_index')

# Cost relationship: geometric visits != source segments != accumulation operations.
f,a=canvas(3.3)
box(a,1,76,28,18,'空间配置 θ\n尺度 / 局部细化 / 源区')
box(a,36,76,28,18,'执行配置 s\n缓存 / 分组 / 归约')
box(a,71,76,28,18,'固定物理与射线\n核数据 / 群 / 方向')
box(a,1,43,28,20,'体素/树节点访问\nNv,k：定位与穿越')
box(a,36,43,28,20,'实际输运段\nNs,k：材料/源/计分')
box(a,71,43,28,20,'通量求和与热点\n通量写入 / 原子冲突')
for x in [15,50,85]:arrow(a,x,75,x,64,dash=True)
arrow(a,29,53,35,53,dash=True);arrow(a,64,53,70,53,dash=True)
box(a,1,11,28,18,'几何与响应误差\nΔτ / 连通性 / εR',fc='#e4efeb')
box(a,36,11,28,18,'峰值显存\n索引 + 场 + 缓存 + 工作区')
box(a,71,11,28,18,'完整求解时间\n生成 + 迭代 + 传输 + I/O')
for x in [15,50,85]:arrow(a,x,42,x,30,dash=True)
text(a,50,3,'待检验：局部细化的精度收益，是否伴随可解释的工作量与成本变化',9)
save(f,'voxel_gpu_cost')

# Experimental design with exact factorial levels and outputs rather than generic flow boxes.
f,a=canvas(3.8)
text(a,50,95,'同一物理模型：斜界面 / 薄层 / 直通与折弯孔道',10)
box(a,1,58,28,28,'参考链\n解析交点与光学厚度\n空间、角度与源迭代收敛\n同离散 CPU / GPU核对',size=9)
box(a,36,58,28,28,'空间变量 θ\n均匀 / 局部块 / 层级\n尺度与界面相位\n材料及源区配置',size=9)
box(a,71,58,28,28,'执行变量 s\n显式 / 在线 / 部分缓存\n原序 / 分桶 / 空间分组\n原子 / 局部归约',size=9)
arrow(a,30,71,35,71);arrow(a,70,71,65,71)
text(a,50,49,'交叉实验：θ × s；误差、显存与完整时间逐点实测',9)
box(a,1,18,28,22,'基线与四组对照\n均匀基线 / 仅空间 / 仅GPU\n独立组合 / 联合配置',size=8.5)
box(a,36,18,28,22,'机制与预测\n段数 / 带宽 / 工作分歧\n校准 → 留出几何检验',size=8.5)
box(a,71,18,28,22,'应用验证\nFNS及聚变子结构\n固定CADIS / FW-CADIS',size=8.5)
arrow(a,50,45,50,41);arrow(a,30,29,35,29);arrow(a,65,29,70,29)
text(a,50,6,'输出：误差约束下可行前沿、配置选择损失、完整达标时间',9)
save(f,'research_design')
