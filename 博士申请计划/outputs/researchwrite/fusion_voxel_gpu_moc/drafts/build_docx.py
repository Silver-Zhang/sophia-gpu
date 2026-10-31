from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'exports/博士科研计划书大纲.md'
OUTPUT = ROOT / 'exports/博士科研计划书大纲.docx'
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2.1), Cm(1.9)
sec.left_margin, sec.right_margin = Cm(2.1), Cm(2.1)
sec.header_distance, sec.footer_distance = Cm(0.9), Cm(0.9)

def font(style, size, bold=False, east='Noto Serif CJK SC'):
    style.font.name = 'Times New Roman'
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = RGBColor(0, 0, 0)
    rf = style.element.get_or_add_rPr().rFonts
    for attr in ['asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme']:
        rf.attrib.pop(qn('w:' + attr), None)
    rf.set(qn('w:eastAsia'), east)
    for border in style.element.xpath('./w:pPr/w:pBdr'):
        border.getparent().remove(border)

font(doc.styles['Normal'], 11)
normal = doc.styles['Normal'].paragraph_format
normal.line_spacing = 1.2
normal.space_after = Pt(5)
normal.widow_control = True
for name, size in [('Title', 20), ('Heading 1', 15), ('Heading 2', 12)]:
    st = doc.styles[name]
    font(st, size, True, 'Noto Sans CJK SC')
    st.paragraph_format.keep_with_next = True
    st.paragraph_format.space_before = Pt(12 if name != 'Title' else 0)
    st.paragraph_format.space_after = Pt(7)
    st.paragraph_format.line_spacing = 1.12
for name in ['List Bullet', 'List Number']:
    font(doc.styles[name], 11)
    st = doc.styles[name].paragraph_format
    st.space_after = Pt(4)
    st.line_spacing = 1.2

# The header stays deliberately quiet; no decorative lines or colored headings.
hp = sec.header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = hp.add_run('博士科研计划书 · 详细大纲')
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(90, 90, 90)
r.font.name = 'Noto Serif CJK SC'
r._r.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Noto Serif CJK SC')
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run()
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
r._r.addnext(field)

def hyperlink(p, url):
    rel = p.part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rel)
    r = OxmlElement('w:r')
    pr = OxmlElement('w:rPr')
    color = OxmlElement('w:color'); color.set(qn('w:val'), '000000'); pr.append(color)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '19'); pr.append(sz)
    r.append(pr)
    t = OxmlElement('w:t'); t.text = url; r.append(t)
    h.append(r); p._p.append(h)

def inline(p, text, size=None):
    for part in re.split(r'(\*\*.*?\*\*|https?://[^\s]+)', text):
        if not part: continue
        if part.startswith('http'):
            hyperlink(p, part)
        else:
            strong = part.startswith('**') and part.endswith('**')
            r = p.add_run(part[2:-2] if strong else part)
            if strong: r.bold = True
            if size: r.font.size = Pt(size)

def table(block):
    data = [[c.strip() for c in line.strip().strip('|').split('|')] for line in block]
    data = [row for row in data if not all(re.fullmatch(r':?-+:?', c) for c in row)]
    t = doc.add_table(rows=1, cols=len(data[0]))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    widths = [3.6, 6.4, 6.8]
    for col, width in zip(t.columns, widths): col.width = Cm(width)
    for rowi, values in enumerate(data):
        cells = t.rows[0].cells if rowi == 0 else t.add_row().cells
        trpr = t.rows[rowi]._tr.get_or_add_trPr()
        cant = OxmlElement('w:cantSplit'); trpr.append(cant)
        if rowi == 0:
            repeat = OxmlElement('w:tblHeader'); trpr.append(repeat)
        for col, value in enumerate(values):
            cell = cells[col]
            cell.width = Cm(widths[col])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.12
            inline(p, value, 10)
            if rowi == 0:
                for r in p.runs: r.bold = True
                shade = OxmlElement('w:shd'); shade.set(qn('w:fill'), 'F1F1F1')
                cell._tc.get_or_add_tcPr().append(shade)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

lines = SOURCE.read_text().splitlines()
i = 0
reference_section = False
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1; continue
    if line.startswith('|'):
        b = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            b.append(lines[i]); i += 1
        table(b); continue
    if line.startswith('# '):
        p = doc.add_paragraph(style='Title')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        inline(p, line[2:])
    elif line == '博士科研计划书大纲':
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(14)
        r = p.add_run('博士科研计划书大纲'); r.font.size = Pt(13)
    elif line.startswith('## '):
        if line.startswith('## 八'):
            reference_section = True
        p = doc.add_paragraph(line[3:], 'Heading 1')
        if reference_section: p.paragraph_format.page_break_before = True
    elif line.startswith('### '):
        doc.add_paragraph(line[4:], 'Heading 2')
    elif line.startswith('- '):
        p = doc.add_paragraph(style='List Bullet'); inline(p, line[2:])
    elif re.match(r'^\d+\. ', line):
        # Explicit labels preserve numbering restarts between outline subsections.
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.55)
        p.paragraph_format.first_line_indent = Cm(-0.55)
        inline(p, line)
    else:
        p = doc.add_paragraph()
        if reference_section and re.match(r'^\[\d+\]', line):
            p.paragraph_format.left_indent = Cm(0.7)
            p.paragraph_format.first_line_indent = Cm(-0.7)
            p.paragraph_format.space_after = Pt(7)
            p.paragraph_format.line_spacing = 1.08
            p.paragraph_format.keep_together = True
            inline(p, line, 9.5)
        else:
            inline(p, line)
    i += 1

doc.core_properties.title = '面向聚变堆复杂几何中子输运的体素化特征线方法与 GPU 并行研究'
doc.core_properties.subject = '博士申请科研计划书详细大纲'
doc.core_properties.author = ''
doc.core_properties.keywords = '聚变中子学; 体素; 特征线方法; GPU; FW-CADIS'
doc.save(OUTPUT)
print(OUTPUT)
