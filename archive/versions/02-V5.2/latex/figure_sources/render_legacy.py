"""Rebuild pre-existing vector diagrams from editable path/text scene data.
Geometry is preserved; every label is reset to the same final 9 pt YaHei font.
"""
from pathlib import Path
import json,re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from figure_style import configure,finish,WIDTH_MM
from matplotlib.textpath import TextToPath
from matplotlib.font_manager import FontProperties
font_path=configure()
font_prop=FontProperties(fname=str(font_path),size=9)
text_metrics=TextToPath()
SUBS=dict(zip('₀₁₂₃₄₅₆₇₈₉','0123456789'))
ROOT=Path(__file__).resolve().parents[1]
scenes=json.loads((ROOT/'figure_sources/legacy_scenes.json').read_text())['scenes']
for name,s in scenes.items():
    w,h=s['width_pt'],s['height_pt']
    fig=plt.figure(figsize=(WIDTH_MM/25.4,WIDTH_MM/25.4*h/w));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,w),ylim=(h,0));ax.axis('off')
    for d in s['paths']:
        verts=[];codes=[];current=None
        for item in d['items']:
            typ=item[0]
            if typ=='re':
                x0,y0,x1,y1=item[1];pts=[(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)]
                verts+=pts;codes +=[MPath.MOVETO,MPath.LINETO,MPath.LINETO,MPath.LINETO,MPath.CLOSEPOLY];current=None
            elif typ=='l':
                a,b=tuple(item[1]),tuple(item[2])
                if current!=a:verts.append(a);codes.append(MPath.MOVETO)
                verts.append(b);codes.append(MPath.LINETO);current=b
            elif typ=='c':
                a=tuple(item[1])
                if current!=a:verts.append(a);codes.append(MPath.MOVETO)
                verts += [tuple(x) for x in item[2:5]];codes += [MPath.CURVE4]*3;current=tuple(item[4])
            elif typ=='qu':
                ul,ur,ll,lr=item[1];verts +=[ul,ur,lr,ll,ul];codes +=[MPath.MOVETO,MPath.LINETO,MPath.LINETO,MPath.LINETO,MPath.CLOSEPOLY];current=None
            else:raise ValueError(typ)
        if not verts:continue
        if d.get('closePath') and codes[-1]!=MPath.CLOSEPOLY:verts.append(verts[0]);codes.append(MPath.CLOSEPOLY)
        stroke=d.get('color');fill=d.get('fill')
        patch=PathPatch(MPath(verts,codes),facecolor=fill if fill is not None else 'none',edgecolor=stroke if stroke is not None else 'none',linewidth=(d.get('width') or 0)*WIDTH_MM/25.4*72/w,
            alpha=min(d.get('fill_opacity') or 1,d.get('stroke_opacity') or 1))
        dash=re.search(r'\[([^]]+)\]',(d.get('dashes') or ''))
        if dash:
            seq=[float(x) for x in dash.group(1).split()]
            if seq:patch.set_linestyle((0,seq))
        ax.add_patch(patch)
    for label in s['labels']:
        x0,y0,x1,y1=label['bbox'];cx,cy=(x0+x1)/2,(y0+y1)/2
        if any(ch in SUBS for ch in label['text']):
            # YaHei has no Unicode subscript digits. Draw its ordinary digits
            # lower on the baseline, at the SAME 9 pt size and SAME font.
            chunks=[]
            for ch in label['text']:
                lowered=ch in SUBS; glyph=SUBS.get(ch,ch)
                if chunks and chunks[-1][1]==lowered:chunks[-1]=(chunks[-1][0]+glyph,lowered)
                else:chunks.append((glyph,lowered))
            widths=[text_metrics.get_text_width_height_descent(t,font_prop,False)[0] for t,_ in chunks]
            units_per_pt=w/(WIDTH_MM/25.4*72);x=cx-sum(widths)*units_per_pt/2
            for (txt,lowered),width in zip(chunks,widths):
                ax.text(x,cy+(2.8*units_per_pt if lowered else 0),txt,ha='left',va='center',color='#203445',fontsize=9)
                x+=width*units_per_pt
        else:ax.text(cx,cy,label['text'],ha='center',va='center',color='#203445',fontsize=9)
    finish(fig,name);plt.close(fig)
