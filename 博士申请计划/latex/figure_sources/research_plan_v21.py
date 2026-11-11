#!/usr/bin/env python3
"""Planned algorithms and validation; no numerical results.

Contract: one research-process diagram, 148.2 x 116 mm, live text, 9 PDF pt,
black ink on white. Inputs feed common MOC, then error-control and GPU methods
feed constrained selection; selected parameters return to the calculation.
Independent validation is the output. The 5.2-5.5 manuscript is the evidence.
No comparable quantitative panels: panel-alignment gate is not applicable.
"""
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from figure_style import configure, finish, ROOT


def draw():
    configure()
    fig, ax = plt.subplots(figsize=(148.2/25.4, 116/25.4))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0,148.2), ylim=(0,116)); ax.axis('off')

    def box(x,y,w,h,text,gid):
        patch=Rectangle((x,y),w,h,fc='white',ec='black',lw=.8)
        patch.set_gid('node-'+gid); ax.add_patch(patch)
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',
                linespacing=1.55,gid='text-'+gid)

    def arrow(x,y,u,v,gid):
        patch=FancyArrowPatch((x,y),(u,v),arrowstyle='->',
                             mutation_scale=9,lw=.8,color='black')
        patch.set_gid('edge-'+gid);ax.add_patch(patch)

    box(8,102,134,10,'几何、材料、群常数与外源','inputs')
    box(8,82,134,15,'材料映射 → 特征线分段 → 多群扫描与源更新\n通量、反应率与轨迹工作量','moc')
    box(8,49,63,23,'误差控制（5.2）\n材料次序/段长 → 伴随加权\n独立加密求积 → 局部细化指标','error')
    box(79,49,63,23,'GPU异构并行（5.3）\n受影响轨迹 → 增量更新/缓存\n分组扫描/按目的地址求和','gpu')
    box(8,22,134,17,'协同选择（5.4）\n误差指标与时间/显存预测 → 筛选离散及执行参数','selection')
    box(8,2,134,13,'独立验证（5.5）\n解析、基准及实验 → 比较响应、总时间与显存','validation')
    arrow(75,102,75,97,'inputs-moc')
    # Fork with a shared horizontal line, no crossing data routes.
    ax.plot([39.5,39.5,110.5,110.5],[75,78,78,75],lw=.8,color='black',gid='fork')
    ax.plot([75,75],[82,78],lw=.8,color='black',gid='moc-fork')
    arrow(39.5,75,39.5,72,'moc-error');arrow(110.5,75,110.5,72,'moc-gpu')
    arrow(39.5,49,39.5,39,'error-selection');arrow(110.5,49,110.5,39,'gpu-selection')
    arrow(75,22,75,15,'selection-validation')
    ax.plot([8,1.5,1.5,4],[30.5,30.5,89.5,89.5],lw=.8,color='black',gid='parameter-feedback')
    arrow(4,89.5,8,89.5,'feedback-moc')
    ax.text(4.7,61,'参数更新',rotation=90,ha='center',va='center',gid='feedback-text')
    finish(fig,'research_plan_v21')
    svg=ROOT/'figure_sources/research_plan_v21.svg'
    fig.savefig(svg)
    raw=svg.read_text()
    raw=re.sub(r'<!DOCTYPE[^>]+>','',raw)
    raw=re.sub(r'(font-size: [0-9.]+)px',r'\1',raw)
    raw=re.sub(r' transform="rotate\(-?0 [^"]+\)"','',raw)
    svg.write_text('\n'.join(line.rstrip() for line in raw.splitlines())+'\n')
    plt.close(fig)

if __name__=='__main__':
    draw()
