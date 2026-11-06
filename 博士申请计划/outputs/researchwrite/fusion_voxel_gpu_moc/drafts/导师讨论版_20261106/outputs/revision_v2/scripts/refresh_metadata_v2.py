"""Recheck publisher-deposited bibliographic fields through Crossref (no full-text claim)."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import requests,json,subprocess
V=Path(__file__).resolve().parents[1];D=V/'bibliography'
records=json.loads((D/'corpus_v2.json').read_text())
keep=['DOI','title','author','container-title','volume','issue','page','article-number','published-print','published-online','issued','publisher','type','URL']
def get(r):
    doi=r.get('doi')
    if not doi or 'arxiv.' in doi.lower():return r['key'],None,{'status':'no_Crossref_DOI; primary record retained'}
    url='https://api.crossref.org/works/'+quote(doi,safe='')
    try:
        response=requests.get(url,timeout=12,headers={'User-Agent':'DoctoralProposalLiteratureVerification/2.0'});response.raise_for_status();data=response.json()['message']
        return r['key'],{k:data[k] for k in keep if k in data},{'status':'publisher_deposit_rechecked','URL':url,'http':response.status_code}
    except Exception as e:return r['key'],None,{'status':'fresh_lookup_failed; independently read primary record retained','URL':url,'error':str(e)}
with ThreadPoolExecutor(max_workers=6) as ex:results=list(ex.map(get,records))
verified={k:v for k,v,_ in results if v}
(D/'crossref_verified_metadata.json').write_text(json.dumps(verified,ensure_ascii=False,indent=2)+'\n')
(D/'metadata_lookup_log.json').write_text(json.dumps({k:s for k,_,s in results},ensure_ascii=False,indent=2)+'\n')
print('Fresh Crossref records:',len(verified),'of',len(records),'corpus identities (non-DOI records use primary pages).')
