from pathlib import Path
import json,requests,concurrent.futures
B=Path(__file__).resolve().parent; S=B.parents[1]/'sources'
rows=json.loads((B/'bibliography/metadata_records.json').read_text())
cache={}
for name in ['参考文献_Crossref逐条核验.json','crossref_additional.json']:
 d=json.loads((S/name).read_text())
 if isinstance(d,dict):
  for k,v in d.items():
   if 'record' in v:cache[k.lower()]=v['record']
 else:
  for v in d:cache[v.get('DOI','').lower()]=v
for r in rows:
 if not r.get('crossref') and r['identifier'].lower() in cache:
  r['crossref']=cache[r['identifier'].lower()];r['metadata_status']='archived publisher Crossref record; key claim rechecked online 2026-11-06'
def f(r):
 if r.get('crossref') or not r['identifier'].startswith('10.') or 'arXiv' in r['identifier']:return r
 for api in ['https://api.crossref.org/works/','https://api.crossref.org/works/']:
  try:
   q=requests.get(api+r['identifier'],timeout=12,headers={'User-Agent':'AcademicBibliography/1.0'})
   if q.ok:
    d=q.json();r['crossref']=d['message'];r['metadata_status']='Crossref retrieved 2026-11-06'
    (B/f"bibliography/crossref_{r['id']:02d}.json").write_text(json.dumps(d,ensure_ascii=False,indent=2));break
  except Exception:pass
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(f,rows))
(B/'bibliography/metadata_records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Missing metadata:',[(r['id'],r['title_hint']) for r in rows if not r.get('crossref')])
