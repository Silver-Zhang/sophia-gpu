"""Refresh publisher-deposited bibliographic metadata without paid full-text access."""
from pathlib import Path
import re,json,urllib.request,urllib.parse,concurrent.futures,time
BASE=Path(__file__).resolve().parent
OUT=BASE/'bibliography'; OUT.mkdir(exist_ok=True)
rows=[]
for line in (BASE/'02_文献证据与引用索引.md').read_text().splitlines():
    cells=[x.strip() for x in line.strip('|').split('|')]
    if cells and cells[0].isdigit():
        i,a,t,y,u,access=cells
        rows.append(dict(id=int(i),author_hint=a,title_hint=t,year_hint=y,identifier=u,AccessLevel=access))
def fetch(r):
    ident=r['identifier']
    if ident.startswith('10.') and 'arXiv' not in ident:
        url='https://api.crossref.org/works/'+urllib.parse.quote(ident,safe='')
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'ResearchProposalBibliography/1.0 (academic metadata verification)'})
            with urllib.request.urlopen(req,timeout=40) as f: data=json.load(f)
            r['crossref']=data['message'];r['metadata_status']='Crossref publisher-deposited record retrieved'
            (OUT/f"crossref_{r['id']:02d}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2))
        except Exception as e:r['metadata_status']=str(e)
    else:r['metadata_status']='official/index manual verification required'
    return r
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rows=list(ex.map(fetch,rows))
(OUT/'metadata_records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for r in rows:
    c=r.get('crossref',{})
    print(r['id'],c.get('title',[r['title_hint']])[0],c.get('published',{}).get('date-parts'),c.get('volume'),c.get('page'),r['metadata_status'])
