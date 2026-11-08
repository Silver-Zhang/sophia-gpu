"""Shared figure typography: YaHei Chinese, Arial labels, body-matched TeX math.
All ordinary labels use 9 PDF pt; math scripts follow native TeX sizing.
Installed fonts are embedded as subsets, never distributed as font files.
"""
from pathlib import Path
import os
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.text import Text
ROOT=Path(__file__).resolve().parents[1]
WIDTH_MM=148.2
FONT_PT=9.0*72.27/72.0  # PGF uses TeX points; the resulting PDF size is 9 bp.

def configure():
    candidates=[os.environ.get('MICROSOFT_YAHEI_FONT',''),
        '/Applications/Microsoft Word.app/Contents/Resources/DFonts/msyh.ttc',
        '/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/msyh.ttc',
        str(Path.home()/'Library/Fonts/msyh.ttc'), 'C:/Windows/Fonts/msyh.ttc']
    path=next((Path(x) for x in candidates if x and Path(x).is_file()),None)
    if path is None:raise RuntimeError('Microsoft YaHei not found. Set MICROSOFT_YAHEI_FONT to a licensed font file.')
    font_manager.fontManager.addfont(str(path))
    if font_manager.FontProperties(fname=str(path)).get_name()!='Microsoft YaHei':
        raise RuntimeError('Expected Microsoft YaHei font.')
    texbin=Path.home()/'texlive/2026/bin/universal-darwin'
    if texbin.is_dir():os.environ['PATH']=str(texbin)+os.pathsep+os.environ.get('PATH','')
    # Match main.tex's native CM math and Times New Roman upright math text.
    # Plain Latin labels remain Arial; xeCJK selects YaHei for Chinese.
    cjk_options='Path={'+path.parent.as_posix()+'/'+'}'
    if path.suffix.lower()=='.ttc':cjk_options+=',FontIndex=0'
    preamble=(r'\usepackage{fix-cm}\usepackage{fontspec}\usepackage{xeCJK}\usepackage{amsmath,amssymb}'
        r'\pagestyle{empty}\DeclareMathSizes{9.03375}{9.03375}{6.0225}{5.01875}'
        r'\setmainfont{Arial}\setsansfont{Arial}'
        r'\setmathrm{Times New Roman}\setmathsf{Helvetica}'
        +r'\setCJKmainfont['+cjk_options+']{'+path.name+'}'
        +r'\setCJKsansfont['+cjk_options+']{'+path.name+'}')
    mpl.rcParams.update({'font.family':['Arial','Microsoft YaHei'],
        'font.size':FONT_PT,'axes.labelsize':FONT_PT,'axes.titlesize':FONT_PT,
        'xtick.labelsize':FONT_PT,'ytick.labelsize':FONT_PT,'legend.fontsize':FONT_PT,
        'mathtext.fontset':'cm','pgf.texsystem':'xelatex','pgf.rcfonts':False,
        'pgf.preamble':preamble,'pdf.fonttype':42,'svg.fonttype':'none',
        'axes.unicode_minus':False})
    return path

def finish(fig,name):
    height=fig.get_figheight()/fig.get_figwidth()*(WIDTH_MM/25.4)
    fig.set_size_inches(WIDTH_MM/25.4,height,forward=True)
    for text in fig.findobj(match=Text):
        text.set_fontfamily(['Arial','Microsoft YaHei'])
        text.set_fontsize(FONT_PT);text.set_fontweight('normal')
    # PGF delegates all final text and formulas to XeLaTeX, as in main.tex.
    fig.savefig(ROOT/'figures'/f'{name}.pdf',backend='pgf')
    if os.environ.get('FIGURE_PREVIEWS') == '1':
        import fitz
        with fitz.open(ROOT/'figures'/f'{name}.pdf') as pdf:
            pdf[0].get_pixmap(matrix=fitz.Matrix(300/72,300/72)).save(
                ROOT/'figure_sources'/f'{name}.png')
