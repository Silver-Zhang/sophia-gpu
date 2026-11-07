"""Six original editable SVG physics/algorithm schematics, with no plotted data."""
from pathlib import Path
from html import escape
import os,json,math
V=Path(__file__).resolve().parents[1];B=V.parents[1];D=V/'figures'
from safety_v3 import require_v3_root
require_v3_root(V)
os.environ.setdefault('DYLD_FALLBACK_LIBRARY_PATH','/opt/homebrew/lib')
os.environ['FONTCONFIG_FILE']=str(V/'qa/fonts.conf')
import cairosvg
INK='#172B3A';BLUE='#2F6D96';TEAL='#3C8D81';PALE='#DCEAF2';GRAY='#EFF2F4';LINE='#8D9EAA'
FONT='PingFang SC, Noto Sans CJK SC, sans-serif'
class SVG:
    def __init__(self,n,h):
        self.n=n;self.h=h;self.i=0
        self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="450pt" height="{h}pt" viewBox="0 0 450 {h}">',
        '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="'+BLUE+'" stroke-width="1"/></marker></defs>',f'<rect x="0" y="0" width="450" height="{h}" fill="white"/>']
    def add(self,s):self.i+=1;self.s.append(f'<g id="component-{self.i}">{s}</g>')
    def rect(self,x,y,w,h,fill=GRAY,stroke=LINE):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="0.7"/>')
    def line(self,x1,y1,x2,y2,color=LINE,width=.7,dash=False,arrow=False):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="4 3"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def path(self,d,fill='none',stroke=BLUE,width=1,dash=False,arrow=False):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"'+(' stroke-dasharray="4 3"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def circle(self,x,y,r=4,fill=BLUE):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{BLUE}" stroke-width="0.7"/>')
    def text(self,x,y,label,size=10,anchor='start',bold=False,mathfont=False):
        lines=label.split('\n')
        family='STIX Two Math' if mathfont else FONT
        for i,line in enumerate(lines):self.add(f'<text x="{x}" y="{y+i*13}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" fill="{INK}"'+(' font-weight="bold"' if bold else '')+'>'+escape(line)+'</text>')
    def box(self,x,y,w,h,label,fill=GRAY):
        self.rect(x,y,w,h,fill);self.text(x+w/2,y+h/2-((len(label.split('\n'))-1)*6.5)+3.3,label,9.5,'middle')
    def grid(self,x,y,cols,rows,cw,ch):
        for i in range(cols+1):self.line(x+i*cw,y,x+i*cw,y+rows*ch)
        for j in range(rows+1):self.line(x,y+j*ch,x+cols*cw,y+j*ch)
    def save(self):
        self.s.append('</svg>');data='\n'.join(self.s).encode()
        (D/f'fig{self.n:02d}.svg').write_bytes(data)
        cairosvg.svg2png(bytestring=data,write_to=str(D/f'fig{self.n:02d}.png'),output_width=3000)
        cairosvg.svg2pdf(bytestring=data,write_to=str(D/f'fig{self.n:02d}.pdf'))
        return {'number':self.n,'width_pt':450,'height_pt':self.h,'png_width_px':3000,'effective_dpi':480,'live_SVG_text':True,'kind':'physics/algorithm schematic; no experimental curve','source':'scripts/build_figures_v3.py'}

def fig1():
    s=SVG(1,292)
    for x,y,label in [(12,18,'a 曲面与细通道'),(238,18,'b 粗网格材料投影'),(12,157,'c 界面附近局部离散'),(238,157,'d 特征线材料段')]:s.text(x,y,label,11,bold=True)
    s.rect(20,34,184,92,GRAY)
    s.path('M20,34 L91,34 C125,52 82,95 119,126 L20,126 Z',PALE,LINE)
    s.path('M20,78 L204,78',stroke='white',width=8)
    s.line(27,60,198,103,BLUE,1.4,arrow=True);s.text(36,54,'材料A');s.text(150,112,'材料B')
    s.text(34,141,'保留界面位置和通道连通性',9.5)
    x=246;y=34
    for i in range(8):
        for j in range(4):s.rect(x+22*i,y+23*j,22,23,PALE if i<4 else GRAY)
    s.rect(312,57,22,23,'#C5DADB');s.rect(334,80,22,23,'#C5DADB')
    s.line(252,58,418,104,BLUE,1.4,arrow=True);s.text(262,141,'界面单元以混合材料表示',9.5)
    s.rect(20,173,184,84,PALE)
    s.path('M95,173 C127,198 91,234 122,257 L204,257 L204,173 Z',GRAY,LINE)
    s.grid(20,173,4,3,46,28)
    for xx in [66,112]:
        for yy in [173,201,229]:s.grid(xx,yy,2,2,23,14)
    s.path('M20,210 L204,210',stroke='white',width=7)
    s.path('M95,173 C127,198 91,234 122,257',stroke=TEAL,width=1.5)
    s.line(26,190,197,242,BLUE,1.4,arrow=True)
    s.text(34,274,'细化改变交点及局部源区',9.5)
    s.rect(246,177,57,71,PALE);s.rect(303,177,67,71,'white');s.rect(370,177,58,71,GRAY)
    s.line(251,219,424,219,BLUE,1.5,arrow=True)
    for a,b,lab in [(251,303,'l₁, Σ₁'),(303,370,'l₂, Σ₂'),(370,423,'l₃, Σ₃')]:s.text((a+b)/2,203,lab,10,'middle',mathfont=True)
    s.text(338,270,'τ = Σ₁l₁ + Σ₂l₂ + Σ₃l₃',10,'middle',mathfont=True)
    return s.save()

def fig2():
    s=SVG(2,227);s.text(12,18,'受控几何与指定响应',11,bold=True);s.text(252,18,'局部候选配置',11,bold=True)
    s.rect(20,36,164,74,PALE);s.grid(20,36,4,3,41,24.6667)
    s.path('M20,82 L75,82 L75,58 L125,58 L125,82 L184,82',stroke='white',width=9)
    s.line(23,82,202,82,BLUE,1.4,arrow=True)
    s.circle(210,82,6,'white');s.text(196,104,'R',10)
    s.rect(270,36,155,74,GRAY);s.grid(270,36,5,3,31,24.6667)
    for xx,yy in [(301,60.6667),(332,60.6667),(363,60.6667)]:s.grid(xx,yy,2,2,15.5,12.3333)
    s.line(276,82,420,82,BLUE,1.2,arrow=True)
    s.line(222,73,257,73,BLUE,1.2,arrow=True)
    stages=['体积与弦长\n材料路径核对','固定材料模型\n离散收敛参考','正向与伴随\n目标误差指标','等预算比较\n局部分辨率']
    for i,label in enumerate(stages):
        x=10+110*i;s.box(x,145,100,47,label,PALE if i==3 else GRAY)
        if i<3:s.line(x+100,168,x+108,168,BLUE,1,arrow=True)
    s.line(75,115,75,136,BLUE,1,arrow=True);s.line(380,115,380,136,BLUE,1,arrow=True)
    s.text(225,216,'比较量：响应误差、材料段数、重建与求解时间',10,'middle')
    return s.save()

def fig3():
    s=SVG(3,304);s.text(10,18,'a 轨迹与材料段',11,bold=True);s.text(168,18,'b 线程批次中的沿程扫描',11,bold=True)
    s.rect(16,35,126,91,PALE);s.grid(16,35,3,3,42,30.3333)
    for y,dy in [(47,38),(65,20),(97,-39)]:s.line(20,y,137,y+dy,BLUE,1.2,arrow=True)
    s.text(27,143,'段长／材料／源区',9.5)
    for i,(count,width) in enumerate([(3,32),(6,31),(2,44),(4,38)]):
        y=38+i*24;s.text(166,y+11,'T'+str(i),9.5)
        for j in range(count):
            x=190+j*width;s.rect(x,y,width,16,PALE if j%2==0 else '#DDEDE8');s.text(x+width/2,y+11,str(j+1),9.5,'middle')
        s.line(190+count*width,y+8,min(437,199+count*width),y+8,BLUE,1,arrow=True)
    s.text(296,143,'一个任务：轨迹与能群',9.5,'middle')
    s.text(10,175,'c 在线生成与缓存',11,bold=True);s.text(226,175,'d 空间单元通量归约',11,bold=True)
    for i,label in enumerate(['段长','材料','源区']):s.box(16+i*57,192,57,25,label)
    s.text(96,241,'读取已缓存的段',10,'middle');s.text(96,256,'或在扫描时生成交点',10,'middle')
    s.line(150,184,150,155,BLUE,1,arrow=True)
    for x,label in [(242,'δ₁'),(298,'δ₂'),(354,'δ₃'),(410,'δ₄')]:s.circle(x,199,11,'white');s.text(x,202,label,9.5,'middle',mathfont=True)
    for x1,x2,x in [(242,298,270),(354,410,382)]:
        s.line(x1,211,x,229,BLUE,1,arrow=True);s.line(x2,211,x,229,BLUE,1,arrow=True);s.circle(x,240,11,PALE);s.text(x,243,'Σ',10,'middle',mathfont=True)
    s.line(270,252,315,272,BLUE,1,arrow=True);s.line(382,252,345,272,BLUE,1,arrow=True)
    s.box(296,276,70,21,'单元通量',PALE)
    s.path('M370,286 L440,286 L440,155 L220,155',width=1,dash=True,arrow=True);s.text(363,150,'源更新',9.5)
    return s.save()

def fig4():
    s=SVG(4,298);s.text(12,18,'局部响应与正向传播',11,bold=True)
    s.circle(37,68,12,PALE);s.text(37,71,'q',11,'middle')
    s.rect(95,39,239,62,GRAY)
    for x in [119,160,201,242,283]:s.line(x,39,x,101)
    s.circle(407,68,10,'white');s.text(407,71,'D',10,'middle')
    s.line(52,81,391,81,BLUE,1.3,arrow=True);s.text(224,115,'物理源到探测区的传播',10,'middle')
    s.line(392,48,53,48,BLUE,1.1,dash=True,arrow=True);s.text(221,35,'伴随信息由目标返回',9.5,'middle')
    s.text(10,153,'CADIS',10,bold=True)
    for x,label in [(89,'响应源 d'),(201,'伴随求解'),(313,'重要性 I')]:s.box(x,135,96,33,label,PALE if x==313 else GRAY)
    s.line(71,151,82,151,BLUE,1,arrow=True);s.line(185,151,195,151,BLUE,1,arrow=True);s.line(297,151,307,151,BLUE,1,arrow=True)
    s.text(10,211,'FW-CADIS',10,bold=True)
    for x,label in [(89,'正向响应估计'),(201,'加权响应源'),(313,'伴随重要性 I')]:s.box(x,193,96,33,label,PALE if x==313 else GRAY)
    s.line(78,209,83,209,BLUE,1,arrow=True);s.line(185,209,195,209,BLUE,1,arrow=True);s.line(297,209,307,209,BLUE,1,arrow=True)
    s.path('M412,151 L432,151 L432,270 L386,270',width=1,arrow=True)
    s.line(361,227,361,249,BLUE,1,arrow=True)
    s.box(89,254,297,34,'同一 I：源抽样 pI/C；目标权重 C/I',PALE)
    return s.save()

def fig5():
    s=SVG(5,292)
    for x,y,label in [(12,18,'a 固定物理输入与目标'),(240,18,'b 改变重要性近似'),(240,157,'c 权窗映射及执行'),(12,157,'d 独立源历史计分')]:s.text(x,y,label,11,bold=True)
    s.rect(20,36,163,77,PALE);s.path('M20,81 L72,81 L72,55 L126,55 L126,81 L183,81',stroke='white',width=9)
    s.line(24,81,204,81,BLUE,1.1,arrow=True);s.circle(211,81,6,'white');s.text(25,128,'几何、材料、源与响应集合',9.5)
    s.rect(246,45,55,55,GRAY);s.grid(246,45,3,3,18.3333,18.3333)
    s.circle(345,72,26,'white')
    for theta in range(0,360,45):
        a=math.radians(theta);s.line(345,72,345+23*math.cos(a),72+23*math.sin(a),BLUE,.8)
    for j in range(3):s.rect(391,45+19*j,34,16,PALE if j%2==0 else GRAY)
    s.text(335,128,'空间、角度与能群配置',9.5,'middle')
    s.line(221,74,234,74,BLUE,1.1,arrow=True);s.line(339,133,339,143,BLUE,1.1,arrow=True)
    for yy,label in [(179,'w上'),(199,'w目标'),(219,'w下')]:s.line(251,yy,303,yy,TEAL,2);s.text(310,yy+3,label,9.5)
    s.circle(365,200,9,PALE);s.text(365,203,'w',9.5,'middle')
    for yy in [178,222]:s.line(375,200,400,yy,BLUE,1,arrow=True);s.circle(412,yy,12,'white');s.text(412,yy+3,'w/2',9.5,'middle')
    s.text(333,251,'映射、平滑、粗化与分裂',9.5,'middle')
    for x,label in [(35,'H1'),(99,'H2'),(163,'H3')]:
        s.circle(x,179,5,PALE);s.text(x,170,label,9.5,'middle')
        for dx in [-10,10]:s.line(x,185,x+dx,211,BLUE,.8);s.circle(x+dx,216,3)
        s.line(x-10,221,x,236,BLUE,.8);s.line(x+10,221,x,236,BLUE,.8)
    s.box(20,241,178,24,'响应、RSD与完整时间',PALE)
    s.line(231,204,209,204,BLUE,1.1,arrow=True)
    s.text(225,282,'生产前固定参数；每个源历史内汇总后代贡献',9.5,'middle')
    return s.save()

def fig6():
    s=SVG(6,286)
    for x,y,label in [(12,18,'a 解析段与界面'),(240,18,'b 材料实验响应'),(12,157,'c 通道与转角散射'),(240,157,'d 聚变子结构响应')]:s.text(x,y,label,11,bold=True)
    s.rect(37,47,65,57,PALE);s.rect(102,47,66,57,'#DDEDE8');s.line(15,75,199,75,BLUE,1.3,arrow=True)
    s.text(69,40,'材料A',9.5,'middle');s.text(135,40,'材料B',9.5,'middle');s.circle(205,75,6,'white');s.text(31,126,'出射角通量、泄漏与段长',9.5)
    s.circle(258,76,6,PALE);s.text(241,46,'D-T源',9.5)
    s.rect(308,46,113,59,GRAY)
    for xx in [324,350,382]:s.line(264,76,xx,76,BLUE,1);s.circle(xx,76,4)
    s.text(318,39,'材料体及探测位置',9.5)
    s.text(337,124,'能谱、反应率',9.5,'middle');s.text(337,138,'加热与产氚',9.5,'middle')
    s.rect(20,177,183,74,GRAY)
    s.path('M20,218 L66,218 L66,192 L126,192 L126,230 L203,230',stroke='white',width=12)
    s.path('M15,218 L72,218 L61,186 L132,187 L121,236 L210,230',width=1.3,arrow=True)
    for x,y in [(72,218),(61,186),(132,187),(121,236)]:s.circle(x,y,2.5)
    s.text(31,272,'流束传播与壁面散射',9.5)
    s.add(f'<ellipse cx="333" cy="215" rx="68" ry="43" fill="{PALE}" stroke="{LINE}" stroke-width="0.8"/>')
    s.add('<ellipse cx="333" cy="215" rx="43" ry="26" fill="white" stroke="'+LINE+'" stroke-width="0.8"/>')
    s.rect(405,195,21,42,'#DDEDE8');s.text(416,187,'磁体',9.5,'middle')
    s.line(345,209,401,209,BLUE,1.1,arrow=True);s.line(346,231,424,258,BLUE,1.1,arrow=True)
    s.text(319,215,'源区',9.5);s.text(377,276,'维护区域',9.5)
    return s.save()

if __name__=='__main__':
    D.mkdir(exist_ok=True)
    result=[f() for f in [fig1,fig2,fig3,fig4,fig5,fig6]]
    (D/'figure_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Created 6 SVG/PNG/PDF schematic sets, 480 dpi PNG, live SVG text.')
