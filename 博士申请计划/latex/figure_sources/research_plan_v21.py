#!/usr/bin/env python3
"""Chapter-five information flow, not a transport-solver flowchart.

Contract: original editable vector, 148.2 x 108 mm, black on white, 9 PDF pt.
RQ1 supplies refinement regions and local response contributions. RQ2 supplies
trajectory work and time/memory estimates. RQ3 chooses trials and returns
refinement/execution settings; chapter 5.5 supplies independent tests.
Evidence: planned algorithms in chapter 5 only, no measured performance claims.
No comparable quantitative panels; panel-alignment gate is not applicable.
"""
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from figure_style import configure, finish, ROOT


def draw():
    configure()
    fig, ax = plt.subplots(figsize=(148.2/25.4, 108/25.4))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0,148.2), ylim=(0,116)); ax.axis('off')

    def box(y,h,text,gid):
        patch=Rectangle((12,y),126,h,fc='white',ec='black',lw=.8)
        patch.set_gid('node-'+gid);ax.add_patch(patch)
        ax.text(75,y+h/2,text,ha='center',va='center',linespacing=1.55,gid='text-'+gid)

    def arrow(x,y,u,v,gid):
        patch=FancyArrowPatch((x,y),(u,v),arrowstyle='->',mutation_scale=9,lw=.8,color='black')
        patch.set_gid('edge-'+gid);ax.add_patch(patch)

    box(101,11,'局部体素细化\n响应误差、轨迹工作量与GPU执行成本','scope')
    box(77,17,'RQ1 材料路径响应评价与细化（5.2）\n共同材料区间 → 局部贡献 → 候选细化区域','error')
    box(45,17,'RQ2 轨迹增量更新与缓存（5.3）\n受影响轨迹 → 局部重建 → GPU执行','gpu')
    box(13,17,'RQ3 有限预算配置选择（5.4）\n误差与显存筛选 → 试算 → 最终配置','selection')
    arrow(75,101,75,94,'scope-error')
    arrow(36,77,36,62,'error-gpu')
    ax.text(84,69.5,'候选细化区域\n受影响轨迹',ha='center',va='center',linespacing=1.4,gid='refinement-work')
    arrow(36,45,36,30,'gpu-selection')
    ax.text(84,37.5,'计算工作量、预计耗时\n峰值显存',ha='center',va='center',linespacing=1.4,gid='work-cost')
    ax.plot([138,145,145,141],[85.5,85.5,21.5,21.5],lw=.8,color='black',gid='error-cost-link')
    arrow(141,21.5,138,21.5,'error-selection')
    ax.text(141.5,54,'局部误差贡献',rotation=90,rotation_mode='anchor',ha='center',va='center',gid='error-feed')
    ax.plot([12,3,3,8],[21.5,21.5,85.5,85.5],lw=.8,color='black',gid='configuration-return')
    arrow(8,85.5,12,85.5,'selection-feedback')
    ax.text(7,54,'细化与执行配置更新',rotation=90,rotation_mode='anchor',ha='center',va='center',gid='feedback-text')
    arrow(75,13,75,8,'selection-validation')
    ax.text(75,3.5,'独立验证（5.5）：响应误差、全过程时间与峰值显存',ha='center',va='center',gid='validation')
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
