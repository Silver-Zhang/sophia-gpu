#!/usr/bin/env python3
"""Recheck baseline DOI metadata against Crossref; retain failures without invented fields."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv,json,re,urllib.request,urllib.parse,datetime,subprocess
ROOT=Path(__file__).resolve().parents[1]
def verify(item):
    entry=item['entry']; m=re.search(r'(10\.\d{4,9}/[A-Za-z0-9._;()/:%+\-]+)',entry)
    doi=m.group(1).rstrip('.,') if m else None
    out={'key':item['key'],'baseline_entry':entry,'doi':doi,'checked_date':'2026-11-08','source':'https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='') if doi else None}
    if not doi: return dict(out,status='no_doi_in_baseline')
    try:
        # System curl uses the OS trust store; Python installation lacks local CA certificates.
        result=subprocess.run(['curl','--fail','--silent','--show-error','--max-time','30',out['source']],capture_output=True,text=True)
        if result.returncode: raise RuntimeError(result.stderr.strip())
        msg=json.loads(result.stdout)['message']
        out.update(status='crossref_metadata_retrieved',title=msg.get('title'),authors=msg.get('author'),published=msg.get('published'),published_online=msg.get('published-online'),published_print=msg.get('published-print'),container_title=msg.get('container-title'),volume=msg.get('volume'),issue=msg.get('issue'),page=msg.get('page'),article_number=msg.get('article-number'),publisher=msg.get('publisher'),license=msg.get('license'),links=msg.get('link'))
    except Exception as exc: out.update(status='retrieval_failed',error=str(exc))
    return out
items=json.loads((ROOT/'references/baseline_inventory.json').read_text())['bibliography']
with ThreadPoolExecutor(max_workers=1) as pool: results=list(pool.map(verify,items))
(ROOT/'references/metadata_crossref.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'references/metadata_crossref.csv').open('w',newline='') as f:
    fields=['key','doi','status','title','container_title','volume','issue','page','article_number','error','source'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(results)
print({status:sum(x['status']==status for x in results) for status in sorted({x['status'] for x in results})})
