from pathlib import Path
import re,json,hashlib
from copy import deepcopy
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'exports/博士科研计划书_唯一审查底稿.md'
MAIN=ROOT/'exports/博士科研计划书_审阅版.docx'
CHECK=ROOT/'exports/提交前仍需补充的信息清单.docx'
raw=SOURCE.read_text()
meta='> 唯一审查底稿：合并第1—11节已确认正文及本轮授权修订；逐节论证自检和修订出处保存在来源记录中，不计入RP正文。'
assert raw.count(meta)==1 or meta not in raw
clean=raw.replace(meta+'\n\n','')
assert raw.replace(meta+'\n\n','')==clean
# Existing LaTeX spans are converted to native editable OMML, never rewritten.
formula_re=r'\\{1,2}\((.*?)\\{1,2}\)'
formula_log=[]
expected=[]
bookmark_id=100

def font(st,size,bold=False,east='Songti SC'):
    st.font.name='Times New Roman';st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=RGBColor(0,0,0)
    rf=st.element.get_or_add_rPr().rFonts
    for k in list(rf.attrib):
        if 'Theme' in k:del rf.attrib[k]
    rf.set(qn('w:eastAsia'),east)
    for b in st.element.xpath('./w:pPr/w:pBdr'):b.getparent().remove(b)

def make_doc():
    d=Document();s=d.sections[0]
    s.page_width=Cm(21);s.page_height=Cm(29.7)
    s.top_margin=Cm(2.4);s.bottom_margin=Cm(2.3);s.left_margin=Cm(2.5);s.right_margin=Cm(2.5)
    s.footer_distance=Cm(1.1)
    font(d.styles['Normal'],12)
    pf=d.styles['Normal'].paragraph_format;pf.line_spacing=Pt(20);pf.space_after=Pt(4);pf.first_line_indent=Pt(24);pf.widow_control=True
    for name,size in [('Title',18),('Heading 1',15),('Heading 2',12.5)]:
        st=d.styles[name];font(st,size,True,'Heiti SC');pf=st.paragraph_format
        pf.first_line_indent=Pt(0);pf.keep_with_next=True;pf.keep_together=True;pf.line_spacing=1.2;pf.space_before=Pt(13 if name!='Title' else 0);pf.space_after=Pt(7)
    d.styles['Title'].paragraph_format.space_after=Pt(16)
    for n in ['List Bullet','List Number']:
        font(d.styles[n],12);pf=d.styles[n].paragraph_format;pf.line_spacing=Pt(20);pf.space_after=Pt(4);pf.first_line_indent=Pt(-12);pf.left_indent=Pt(15);pf.widow_control=True
    ref=d.styles.add_style('Reference Entry',1);font(ref,10.5);pf=ref.paragraph_format
    pf.line_spacing=Pt(14);pf.space_after=Pt(7);pf.left_indent=Pt(23);pf.first_line_indent=Pt(-23);pf.keep_together=True;pf.widow_control=True
    foot=s.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.CENTER;foot.paragraph_format.first_line_indent=Pt(0)
    f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');r=OxmlElement('w:r');t=OxmlElement('w:t');t.text='1';r.append(t);f.append(r);foot._p.append(f)
    settings=d.settings.element
    mp=OxmlElement('m:mathPr');mf=OxmlElement('m:mathFont');mf.set(qn('m:val'),'STIX Two Math');mp.append(mf);settings.append(mp)
    d.core_properties.title=clean.splitlines()[0].removeprefix('# ')
    d.core_properties.author='';d.core_properties.last_modified_by='';d.core_properties.subject='博士科研计划书';d.core_properties.comments=''
    return d

def mr(text,upright=False):
    r=OxmlElement('m:r');pr=OxmlElement('m:rPr');sty=OxmlElement('m:sty');sty.set(qn('m:val'),'p' if upright else 'i');pr.append(sty);r.append(pr)
    wp=OxmlElement('w:rPr');fo=OxmlElement('w:rFonts');fo.set(qn('w:ascii'),'STIX Two Math');fo.set(qn('w:hAnsi'),'STIX Two Math');fo.set(qn('w:eastAsia'),'Songti SC');wp.append(fo)
    sz=OxmlElement('w:sz');sz.set(qn('w:val'),'24');wp.append(sz);r.append(wp)
    t=OxmlElement('m:t');t.text=text;r.append(t);return r

def sub(base,index,upright_index=False):
    s=OxmlElement('m:sSub');e=OxmlElement('m:e');e.append(mr(base,base=='median'));b=OxmlElement('m:sub');b.append(mr(index,upright_index));s.extend([e,b]);return s

def math_nodes(tex):
    tex=tex.replace('\\\\','\\')
    if tex.startswith('|R-R_'):
        return [mr('|'),mr('R'),mr('−',True),sub('R','ref',True),mr('| ≤ ',True),sub('ε','abs',True),mr(' + ',True),sub('ε','rel',True),mr('|',True),sub('R','ref',True),mr('|',True)]
    if tex.startswith('d_{s,j}='):
        return [sub('d','s,j'),mr(' = ',True),sub('T','局部,s,j',True),mr(' − ',True),sub('T','均匀,s,j',True)]
    if tex.startswith('\\Delta T_s='):
        return [sub('ΔT','s'),mr(' = ',True),sub('median','j',True),mr('(',True),sub('d','s,j'),mr(')',True)]
    if tex=='\\Delta T_{\\mathrm{seq}}':return [sub('ΔT','seq',True)]
    if tex=='|\\Delta T_s|':return [mr('|',True),sub('ΔT','s'),mr('|',True)]
    raise ValueError(tex)

def math(p,tex):
    e=OxmlElement('m:oMath')
    for n in math_nodes(tex):e.append(n)
    p._p.append(e)
    flat=''.join(e.itertext()) # logged below using m:t only
    txt=''.join(n.text or '' for n in e.iter(qn('m:t')))
    formula_log.append({'latex':tex,'visible_tokens':txt})
    return txt

def hyperlink(p,label,target,internal=False):
    h=OxmlElement('w:hyperlink')
    if internal:h.set(qn('w:anchor'),target.replace('-','_'))
    else:h.set(qn('r:id'),p.part.relate_to(target,RT.HYPERLINK,is_external=True))
    h.set(qn('w:history'),'1')
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr');co=OxmlElement('w:color');co.set(qn('w:val'),'000000');pr.append(co)
    if internal:
        sz=OxmlElement('w:sz');sz.set(qn('w:val'),'19');pr.append(sz)
    r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)

# Preserve all prose and link labels; markdown-only syntax is removed.
token=re.compile(r'(\*\*.*?\*\*|\[[^\]]+\]\([^)]+\)|'+formula_re+r')')
def inline(p,text,bold=False):
    visible=''
    for piece in token.split(text):
        if piece is None or piece=='':continue
        # Capturing group from formula_re is avoided below by separate scanning.
    cursor=0
    pattern=re.compile(r'\*\*.*?\*\*|\[[^\]]+\]\([^)]+\)|'+formula_re)
    for m in pattern.finditer(text):
        if m.start()>cursor:
            v=text[cursor:m.start()];p.add_run(v).bold=bold;visible+=v
        v=m.group(0)
        if v.startswith('**'):
            visible+=inline(p,v[2:-2],True)
        elif v.startswith('['):
            lm=re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)',v);label,target=lm.groups()
            # Markdown numeric citation label becomes conventional [N], locator retained.
            label='['+label+']' if target.startswith('#ref-') else label
            hyperlink(p,label,target.lstrip('#'),target.startswith('#'));visible+=label
        else:
            fm=re.fullmatch(formula_re,v);visible+=math(p,fm.group(1))
        cursor=m.end()
    if cursor<len(text):v=text[cursor:];p.add_run(v).bold=bold;visible+=v
    return visible

def docx_text(p):
    return ''.join(p._p.xpath('.//w:t/text() | .//m:t/text()'))

d=make_doc();pending_bookmark=None
for line in clean.splitlines():
    if not line.strip():continue
    am=re.fullmatch(r'<a id="(ref-\d+)"></a>',line)
    if am:pending_bookmark=am.group(1).replace('-','_');continue
    if line.startswith('# '):
        p=d.add_paragraph(style='Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;text=line[2:]
    elif line.startswith('## '):
        p=d.add_paragraph(style='Heading 1');text=line[3:]
        if text=='参考文献':p.paragraph_format.page_break_before=True
    elif line.startswith('### '):p=d.add_paragraph(style='Heading 2');text=line[4:]
    elif line.startswith('- '):p=d.add_paragraph(style='List Bullet');text=line[2:]
    elif re.match(r'^\[\d+\] ',line):p=d.add_paragraph(style='Reference Entry');text=line
    else:
        p=d.add_paragraph();text=line
        if re.match(r'^\d+\. ',line):p.paragraph_format.first_line_indent=Pt(0)
    if pending_bookmark:
        bookmark_id+=1;b=OxmlElement('w:bookmarkStart');b.set(qn('w:id'),str(bookmark_id));b.set(qn('w:name'),pending_bookmark);p._p.append(b)
    exp=inline(p,text)
    if pending_bookmark:
        e=OxmlElement('w:bookmarkEnd');e.set(qn('w:id'),str(bookmark_id));p._p.append(e);pending_bookmark=None
    assert docx_text(p)==exp,(text[:50],docx_text(p),exp)
    expected.append(exp)
d.save(MAIN)
# Exact text check on saved OOXML includes text in hyperlinks and OMML.
loaded=Document(MAIN)
actual=[docx_text(p) for p in loaded.paragraphs if docx_text(p)]
assert actual==expected,'Saved text differs from the approved source rendering'
assert len(formula_log)==5
assert len(loaded.element.xpath('//m:oMath'))==5
assert len(loaded.element.xpath('//w:bookmarkStart'))==13
assert len(loaded.element.xpath('//w:hyperlink[@w:anchor]'))==22
assert '唯一审查底稿' not in ''.join(actual)
assert '尚不具备，需系统学习' in ''.join(actual)

# Separate checklist: no new commitments are inserted in the proposal.
items=[
('提交前需补充或确认的信息',[
('申请与提交信息','申请人姓名、报考院系与专业、导师姓名的正式写法、申请批次及提交截止时间；是否要求匿名审阅。'),
('院系格式与学制','院系指定模板、篇幅和参考文献格式要求，以及实际学制。正文目前为“暂按四年规划；学制待确认”，未默认四年培养。'),
('组内网格与求解器条件','补充已有块结构网格框架的名称、版本及可使用范围；确认MOC求解器本体是否可访问、可修改，GPU化程度和网格、轨迹、截面、通量接口状态。'),
('GPU与性能分析条件','确认GPU型号、显存容量、使用权限与可用时段；确认性能分析工具的安装、版本兼容性与性能计数器权限。未落实前，正文继续保留“待确认”。'),
('专项学习安排','补充GPU编程与MOC实现的具体学习安排、拟完成的代码实践及验收方式。已有编程和输运建模基础不替代专项实现能力，不预设已完成培训。'),
('申请人材料佐证','准备课程成绩、项目参与说明和可提供的代码或报告；硕士课题仍标为在研，提交时按实际进展更新，不将预期结果写为已完成。')]),
('实施前需冻结的参数',[
('物理输入与精度约束','明确拟使用算例与数据访问条件、目标响应、角能离散、参考解生成条件及绝对与相对组合容限。若提交前未落实，保留待定状态及确定方式。'),
('资源与公平比较预算','明确显存预算档位、对等调参预算、候选参数范围与独立测试场景划分；这些数值须由实际代码和设备条件支持。'),
('预登记与验收参数','按正文约定，在正式测量前冻结配置集与独立配置点数、模型复杂度、重复次数、计时重构阈值、噪声判据及留出检验验收要求。它们不是本次格式整理已确定的事实。')])]
c=make_doc();c.core_properties.title='提交前仍需补充的信息清单';c.core_properties.subject='博士科研计划书提交信息'
p=c.add_paragraph('提交前仍需补充的信息清单',style='Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
for heading,rows in items:
    c.add_paragraph(heading,style='Heading 1')
    for title,body in rows:
        p=c.add_paragraph(style='List Bullet');p.add_run(title+'：').bold=True;p.add_run(body)
c.save(CHECK)
(ROOT/'exports/提交前仍需补充的信息清单.md').write_text('# 提交前仍需补充的信息清单\n\n'+'\n\n'.join('## '+heading+'\n\n'+'\n'.join('- **'+t+'：**'+b for t,b in rows) for heading,rows in items)+'\n')
SOURCE.write_text(clean)
qa={'status':'created_pending_render_review','main_docx':str(MAIN.relative_to(ROOT)),'checklist_docx':str(CHECK.relative_to(ROOT)),
    'source_sha256':hashlib.sha256(clean.encode()).hexdigest(),'paragraphs_checked':len(actual),'formulas':formula_log,
    'internal_citations':22,'reference_bookmarks':13,'body_prose_rewritten':False,'draft_metadata_removed':True,
    'page':'A4; margins top 2.4 / bottom 2.3 / left-right 2.5 cm',
    'styles':'Title; Heading 1; Heading 2; 12pt body exact 20pt spacing; 10.5pt hanging references; editable OMML',
    'resources':'All pending solver/GPU/tool states retained; GPU/MOC skill not yet acquired retained.'}
(ROOT/'qa_logs/Word排版核验记录.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in qa.items() if k!='formulas'},ensure_ascii=False,indent=2))
