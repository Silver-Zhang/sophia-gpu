"""Offline reconstruction, scoped to the authorized V2 directory."""
from pathlib import Path
import subprocess,sys,os,json
V=Path(__file__).resolve().parents[1]
assert json.loads((V/'authorization.json').read_text())['approved'] is True
for name in ['build_bibliography_v2.py','write_tables_v2.py','build_figures_v2.py','export_v2.py','human_markdown_v2.py','verify_v2.py']:
 subprocess.run([sys.executable,str(V/'scripts'/name)],cwd=V,check=True)
print('Built V2 only. Reinspect every newly rendered page before delivery.')
