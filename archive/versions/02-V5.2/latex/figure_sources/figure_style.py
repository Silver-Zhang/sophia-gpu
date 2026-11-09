"""Shared final-print typography for every figure: Microsoft YaHei, 9 PDF pt.
The licensed font is read from the user's installation, never redistributed.
"""
from pathlib import Path
import os
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.text import Text
ROOT=Path(__file__).resolve().parents[1]
WIDTH_MM=148.2
FONT_PT=9.0

def configure():
    candidates=[os.environ.get('MICROSOFT_YAHEI_FONT',''),
        '/Applications/Microsoft Word.app/Contents/Resources/DFonts/msyh.ttc',
        '/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/msyh.ttc',
        str(Path.home()/'Library/Fonts/msyh.ttc'), 'C:/Windows/Fonts/msyh.ttc']
    path=next((Path(x) for x in candidates if x and Path(x).is_file()),None)
    if path is None:raise RuntimeError('Microsoft YaHei not found. Set MICROSOFT_YAHEI_FONT to a licensed font file.')
    font_manager.fontManager.addfont(str(path))
    name=font_manager.FontProperties(fname=str(path)).get_name()
    if name!='Microsoft YaHei':raise RuntimeError(f'Expected Microsoft YaHei, got {name}')
    mpl.rcParams.update({'font.family':'sans-serif','font.sans-serif':[name],
        'font.size':FONT_PT,'axes.labelsize':FONT_PT,'axes.titlesize':FONT_PT,
        'xtick.labelsize':FONT_PT,'ytick.labelsize':FONT_PT,'legend.fontsize':FONT_PT,
        'pdf.fonttype':42,'svg.fonttype':'none','axes.unicode_minus':False})
    return path

def finish(fig,name):
    height=fig.get_figheight()/fig.get_figwidth()*(WIDTH_MM/25.4)
    fig.set_size_inches(WIDTH_MM/25.4,height,forward=True)
    for text in fig.findobj(match=Text):
        text.set_fontfamily('Microsoft YaHei');text.set_fontsize(FONT_PT);text.set_fontweight('normal')
    fig.canvas.draw()
    fig.savefig(ROOT/'figures'/f'{name}.pdf')
    if os.environ.get('FIGURE_PREVIEWS') == '1':
        fig.savefig(ROOT/'figure_sources'/f'{name}.svg')
        fig.savefig(ROOT/'figure_sources'/f'{name}.png',dpi=300)
