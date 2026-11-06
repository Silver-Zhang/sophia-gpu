"""Original conceptual figures, live SVG text, no simulated performance data."""
from pathlib import Path
from html import escape
import json,os
os.environ.setdefault('DYLD_FALLBACK_LIBRARY_PATH','/opt/homebrew/lib')
import cairosvg
P=Path(__file__).resolve().parent/'figures';P.mkdir(exist_ok=True)
W=450
def draw(num,title,height,nodes,edges,extra=''):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="450pt" height="{height}pt" viewBox="0 0 450 {height}">',
       '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="#425466" stroke-width="1"/></marker></defs>',
       '<rect width="450" height="'+str(height)+'" fill="white"/>',
       f'<text x="225" y="17" text-anchor="middle" font-family="PingFang SC, Noto Sans CJK SC, sans-serif" font-size="11" fill="#172B40">{escape(title)}</text>']
    for i,(x,y,w,h,lines,accent) in enumerate(nodes):
        s.append(f'<g id="node-{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="'+('#E7F0F8' if accent else '#F5F6F7')+'" stroke="#425466" stroke-width="0.8"/>')
        for j,line in enumerate(lines):
            yy=y+h/2-(len(lines)-1)*6.5+j*13+3.5
            s.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-family="PingFang SC, Noto Sans CJK SC, sans-serif" font-size="10" fill="#172B40">{escape(line)}</text>')
        s.append('</g>')
    for i,(points,dashed) in enumerate(edges):
        s.append(f'<polyline id="edge-{i}" points="{points}" fill="none" stroke="#425466" stroke-width="1"'+(' stroke-dasharray="4 3"' if dashed else '')+' marker-end="url(#arrow)"/>')
    s.append(extra);s.append('</svg>')
    svg='\n'.join(s);(P/f'fig{num:02}.svg').write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(P/f'fig{num:02}.png'),scale=4.1666667)
    cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(P/f'fig{num:02}.pdf'))
    return dict(figure=num,title=title,width_pt=W,height_pt=height,source='build_figures.py',kind='original conceptual diagram; no experimental data')
spec=[]
spec.append(draw(1,'方案评价包含建模、输运与更新反馈',213,[
 (10,38,126,48,['几何与材料设计','层厚／孔道／源'],False),(162,38,126,48,['模型转换与检查','空间分区／材料'],False),(314,38,126,48,['离散与数据准备','网格／截面／轨迹'],False),
 (314,128,126,48,['输运及统计计算','正／伴随、MC'],False),(162,128,126,48,['目标响应核验','精度／统计／成本'],True),(10,128,126,48,['设计更新','判定复用或重建'],False)],
 [('136,62 162,62',False),('288,62 314,62',False),('377,86 377,128',False),('314,152 288,152',False),('162,152 136,152',False),('73,128 73,86',True)],
 '<text x="225" y="202" text-anchor="middle" font-family="PingFang SC" font-size="9" fill="#172B40">虚线为设计反馈；重建开销按实际触发环节计入</text>'))
spec.append(draw(2,'四类空间对象及误差传播路径',244,[
 (10,37,126,46,['CAD／CSG材料模型','界面与连通性'],False),(162,37,126,46,['确定论空间离散','体素／规则块'],False),(314,37,126,46,['轨迹材料段序列','段长与光学厚度'],False),
 (10,127,126,48,['重要性场','目标贡献与方向'],False),(162,127,126,48,['权窗空间网格','采样权重控制'],False),(314,127,126,48,['响应与全过程成本','离散误差／资源'],True)],
 [('136,60 162,60',False),('288,60 314,60',False),('377,83 377,127',False),('225,83 225,103 73,103 73,127',False),('136,151 162,151',False),('288,151 314,151',False)],
 '<text x="225" y="205" text-anchor="middle" font-family="PingFang SC" font-size="10" fill="#172B40">界面位置、薄层和流道误差会改变传播路径</text><text x="225" y="224" text-anchor="middle" font-family="PingFang SC" font-size="10" fill="#172B40">求解网格与权窗网格可分别配置</text>'))
spec.append(draw(3,'GPU-MOC的轨迹组织与成本来源',258,[
 (10,36,126,44,['网格／材料／源','段数与访问分布'],False),(162,36,126,44,['轨迹存储选择','在线／全／部分缓存'],True),(314,36,126,44,['按工作量分组','轨迹／角度／能群'],False),
 (314,117,126,46,['沿轨迹扫描','段内积分及递推'],False),(162,117,126,46,['通量归约与源更新','原子／局部归约'],False),(10,117,126,46,['收敛及数据输出','全部迭代计时'],False),
 (10,207,430,32,['成本观测：追踪、访存、分歧、竞争、传输、峰值显存'],False)],
 [('136,58 162,58',False),('288,58 314,58',False),('377,80 377,117',False),('314,140 288,140',False),('162,140 136,140',False),('225,163 225,184 377,184 377,163',True)],
 '<text x="85" y="188" text-anchor="middle" font-family="PingFang SC" font-size="9" fill="#172B40">虚线为源迭代</text>'))
spec.append(draw(4,'CADIS与FW-CADIS的一致偏倚流程',270,[
 (10,34,126,44,['CADIS','单目标响应源'],False),(162,34,126,44,['伴随求解','目标重要性'],False),(314,34,126,44,['近似重要性 I','保留采样支持'],False),
 (10,111,126,44,['FW-CADIS','先求正向响应'],False),(162,111,126,44,['加权伴随源','按正向响应分配'],False),(314,111,126,44,['伴随求解得到 I','多目标重要性'],False),
 (55,210,158,44,['同一 I 生成','源偏倚＋一致权窗'],True),(257,210,158,44,['MC生产输运','响应与统计核验'],False)],
 [('136,56 162,56',False),('288,56 314,56',False),('136,133 162,133',False),('288,133 314,133',False),('440,56 447,56 447,180 134,180 134,210',False),('377,155 377,180',False),('213,232 257,232',False)]))
spec.append(draw(5,'重要性生成到蒙卡达标的全过程成本',239,[
 (10,36,126,44,['几何／材料检查','Tgeom'],False),(162,36,126,44,['多群核数据准备','TXS'],False),(314,36,126,44,['正向／伴随求解','TF ＋ TA'],False),
 (314,122,126,44,['映射／平滑／粗化','TWW'],False),(162,122,126,44,['MC生产输运','TMC'],False),(10,122,126,44,['输出与诊断','TIO'],False),
 (10,197,430,28,['合计时间各项不重复；更新时仅重计实际失效环节'],True)],
 [('136,58 162,58',False),('288,58 314,58',False),('377,80 377,122',False),('314,144 288,144',False),('162,144 136,144',False)]))
spec.append(draw(6,'候选方向可独立开展并按条件衔接',255,[
 (10,34,430,36,['共同目标：可靠屏蔽响应与可核验的资源收益'],False),
 (10,111,126,61,['方向一','空间离散与几何误差','需网格／伴随接口'],False),(162,111,126,61,['方向二','GPU正向—伴随','需源码／GPU资源'],False),(314,111,126,61,['方向三','自动耦合减方差','可先用成熟工具'],True),
 (10,214,430,28,['导师据应用、代码及实证问题选一个主方向'],False)],
 [('73,70 73,111',False),('225,70 225,111',False),('377,70 377,111',False),('73,172 73,214',False),('225,172 225,214',False),('377,172 377,214',False)],
 ''))
(P/'figure_manifest.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
print('Created',len(spec),'SVG/PNG/PDF conceptual figures')
