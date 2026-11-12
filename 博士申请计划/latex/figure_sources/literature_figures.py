#!/usr/bin/env python3
"""Licensed literature image assembly.
Reproduction details and immutable asset hashes: references/figure_sources.md.
"""
from pathlib import Path
import os, sys, tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams.update({"font.family": ["Arial", "Microsoft YaHei"], "font.size": 9.03375,
    "svg.fonttype": "none", "pdf.fonttype": 42})
import matplotlib.image as mpimg
import fitz
from figure_style import configure, finish, WIDTH_MM
configure()
ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(__file__).resolve().parent/'literature'
qa_scripts = os.environ.get('NATURE_FIGURE_QA_SCRIPTS')
if not qa_scripts:
    raise RuntimeError('Set NATURE_FIGURE_QA_SCRIPTS to the nature-figure scripts directory.')
sys.path.insert(0, qa_scripts)
from audit_panel_alignment import require_matplotlib_panel_alignment
QA = Path(os.environ.get('FIGURE_QA_DIR', tempfile.gettempdir()))

def axes_pair(height):
    f, aa = plt.subplots(1, 2, figsize=(WIDTH_MM/25.4, height/25.4))
    f.subplots_adjust(left=.005, right=.995, bottom=.01, top=.99, wspace=.07)
    for a in aa:
        a.set(xlim=(0,1), ylim=(0,1));a.axis('off')
    return f, aa

def image_contained(a, arr, ytop=1):
    # Preserve image aspect ratio within equal physical panel rectangles.
    b=a.get_window_extent(); ratio=(arr.shape[1]/arr.shape[0])/(b.width/b.height)
    w=min(1, ratio*ytop); h=w/ratio
    # PGF can embed native image pixels; interpolation='none' prevents export downsampling.
    a.figure._native_image_sizes = getattr(a.figure, '_native_image_sizes', []) + [(arr.shape[1], arr.shape[0])]
    a.imshow(arr, extent=((1-w)/2,(1+w)/2,(ytop-h)/2,(ytop+h)/2), aspect='auto', interpolation='none', resample=False)

def save(f, name):
    f.canvas.draw()
    require_matplotlib_panel_alignment(f, json_out=QA/(name+'.alignment.json'))
    finish(f,name)  # Export figures/<name>.pdf using shared PGF/XeLaTeX settings.
    with fitz.open(ROOT/'figures'/f'{name}.pdf') as pdf:
        actual = sorted((im[2],im[3]) for im in pdf[0].get_images())
    if actual != sorted(f._native_image_sizes):
        raise RuntimeError(f'{name}: embedded image pixels changed: {actual}')
    if os.environ.get('FIGURE_QA_EXPORTS') == '1':
        f.savefig(QA/(name+'.svg'))
        f.savefig(QA/(name+'.png'), dpi=600)
    plt.close(f)

# Engineering geometry: unchanged complete official images, only scaled/assembled.
f, aa=axes_pair(65)
f.canvas.draw()
for a, name, label in zip(aa,['ars-9610-powercore04.jpg','ars-9611-blanket03.jpg'],['a','b']):
    image_contained(a,mpimg.imread(ASSETS/name),ytop=.93)
    a.text(0, .98, label, va='top', color='black')
save(f,'aries_rs')

# Same-sized original panels b,d: no recolouring, retouching or result images.
im=mpimg.imread(ASSETS/'yang_fig1.webp')
f, aa=axes_pair(78)
f.canvas.draw()
for a, crop in zip(aa,[im[:504,468:,:],im[504:,468:,:]]):
    image_contained(a,crop)
save(f,'yang_mesh')
