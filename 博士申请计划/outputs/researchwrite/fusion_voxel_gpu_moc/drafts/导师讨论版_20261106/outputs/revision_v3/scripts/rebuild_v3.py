"""Offline reconstruction, scoped to the authorized V3 directory."""
from pathlib import Path
import subprocess,sys,os,json
V=Path(__file__).resolve().parents[1]
from safety_v3 import require_v3_root
require_v3_root(V)
if '--portable' in sys.argv:os.environ['RP_V3_PORTABLE']='1'
assert json.loads((V/'authorization.json').read_text())['approved'] is True
for name in ['build_bibliography_v3.py','write_tables_v3.py','build_figures_v3.py','export_v3.py','human_markdown_v3.py','close_comments_v3.py','verify_v3.py','concordance_v3.py']:
 subprocess.run([sys.executable,str(V/'scripts'/name)],cwd=V,check=True)
print('Built V3 only. Reinspect every newly rendered page before delivery.')
