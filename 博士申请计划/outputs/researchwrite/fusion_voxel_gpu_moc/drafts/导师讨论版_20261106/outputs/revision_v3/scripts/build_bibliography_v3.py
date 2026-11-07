"""Compile the original corpus and independently checked additions for V3."""
from pathlib import Path
from collections import defaultdict
from html import unescape
import csv,json,re
V=Path(__file__).resolve().parents[1];B=V.parents[1];D=V/'bibliography'
from safety_v3 import require_v3_root
require_v3_root(V)
old=json.loads((D/'base_verified_records.json').read_text())
db={r['key']:dict(r) for r in old};evidence=defaultdict(list)
for filename in ['geometry_evidence.json','gpu_evidence.json','hybrid_evidence.json','application_evidence.json','gpu_context_evidence.json','opensn_evidence.json','v3_gpu_adjoint_followup.json']:
    data=json.loads((D/filename).read_text())
    for r in (data['records'] if 'records' in data else [data]) if isinstance(data,dict) else data:evidence[r['key']].append(dict(r,evidence_file=filename))
for h in json.loads((D/'v3_hardware_followup.json').read_text())['records']:
    evidence[h['key']].append({'key':h['key'],'evidence_file':'v3_hardware_followup.json','access_level':'2026-11-07限定补查：出版社元数据/摘要及作者单位原始资料；具体层级见attempts','primary_url':h['attempts'][0]['url'],'hardware':{'formal_gpu_model':h.get('formal_gpu_model'),'formal_cpu_model':h.get('formal_cpu_model')},'result':h.get('new_confirmed_facts',[]),'原文位置':h['attempts'],'unresolved':h.get('unresolved',[])})
def author(name):
    if isinstance(name,dict):return name
    if ',' in name:
        family,given=name.split(',',1);return {'family':family.strip(),'given':given.strip()}
    bits=name.split()
    return {'family':bits[-1],'given':' '.join(bits[:-1])} if len(bits)>1 else {'family':name}
for key,records in evidence.items():
    if key in db:continue
    r=records[0];venue=r.get('venue',{})
    db[key]={'key':key,'title':r['title'],'author':r.get('author') or [author(a) for a in r['authors']],
             'year':r['year'],'doi':r.get('doi') or '',
             'journal':venue.get('journal',r.get('journal','')) if isinstance(venue,dict) else venue,
             'volume':venue.get('volume','') if isinstance(venue,dict) else r.get('volume',''),
             'issue':venue.get('issue','') if isinstance(venue,dict) else r.get('issue',''),
             'pages':venue.get('pages','') if isinstance(venue,dict) else r.get('pages',''),
             'url':r['primary_url'],'kind':'article'}
    if key=='new_pryer_wavefront2026':db[key].update(kind='misc',journal='',eprint='2609.14496',url='https://arxiv.org/abs/2609.14496v1',note='arXiv预印本，v1；DOI登记状态见核验记录')
    if key=='new_shift_gpu_status2025':db[key].update(journal='EPJ Nuclear Sciences & Technologies',volume='11',pages='5')
    if key=='new_opensn2026':db[key].update(journal='Computer Physics Communications',volume='320',pages='110001')
    if key=='new_longhistory2013':db[key].update(kind='misc',journal='',eprint='1309.6166',note='M&C 2013作者稿；arXiv预印本')
    if key=='new_stream_kns2024':db[key].update(kind='inproceedings',note='Jeju, Korea, May 9–10, 2024')
fresh=json.loads((D/'crossref_verified_metadata.json').read_text()) if (D/'crossref_verified_metadata.json').exists() else {}
for key,r in db.items():
    c=fresh.get(key,{})
    if c:
        r['title']=unescape(c['title'][0])
        if c.get('author'):r['author']=c['author']
        if r['kind']=='article':
            for source,target in [('container-title','journal'),('volume','volume'),('issue','issue'),('page','pages')]:
                if c.get(source):r[target]=unescape(c[source][0]) if isinstance(c[source],list) else c[source]
            if not c.get('page') and c.get('article-number'):r['pages']=c['article-number']
    if key=='new_liu_balakovo2023':r['title']='Verification of multilevel octree grid algorithm of S_N transport calculation with the Balakovo-3 VVER-1000 neutron dosimetry benchmark'
    r['Boundary']='; '.join(dict.fromkeys(e['access_level'] for e in evidence[key]))
    r['evidence_records']=evidence[key]
    assert r['evidence_records'],key
    r['url']='https://doi.org/'+r['doi'] if r.get('doi') else r.get('url',r['evidence_records'][0]['primary_url'])
    if key=='new_pryer_wavefront2026':r['url']='https://arxiv.org/abs/2609.14496v1'
    if key=='r29':r['note']='在线指南13.5；访问日期2026-11-06'
    if key=='r45':r['url']='https://cms.oecd-nea.org/jcms/pl_32139/sinbad-shielding-integral-benchmark-archive-and-database'
    if key=='new_stream_kns2024':
        r['booktitle']='Transactions of the Korean Nuclear Society Spring Meeting'
        r['journal']=''
    r['AccessLevel']='; '.join(dict.fromkeys(e['access_level'] for e in evidence[key]))
    assert r.get('author') and r.get('title') and r.get('year'),key
def clean(s):return str(s).replace('&amp;','&').replace('{','').replace('}','')
def auth(a):
    family=a.get('family',a.get('name',''));given=a.get('given','')
    return family+', '+given if given else '{'+family+'}'
bib=[]
for key,r in db.items():
    fields={'author':' and '.join(auth(a) for a in r['author']),'title':'{'+clean(r['title'])+'}','year':str(r['year'])}
    for src,dest in [('journal','journal'),('booktitle','booktitle'),('volume','volume'),('issue','number'),('pages','pages'),('doi','doi'),('url','url'),('school','school'),('address','address'),('organization','organization'),('note','note'),('eprint','eprint')]:
        if r.get(src):fields[dest]=clean(r[src])
    if r['kind'] in ['online','manual','misc']:fields['urldate']='2026-11-06'
    if r.get('eprint'):fields['archivePrefix']='arXiv'
    bib.append('@'+r['kind']+'{'+key+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items())+'\n}')
(D/'references_v3.bib').write_text('\n\n'.join(bib)+'\n')
(D/'corpus_v3.json').write_text(json.dumps(list(db.values()),ensure_ascii=False,indent=2)+'\n')
cols=['key','authors','title','year','journal','volume','issue','pages','DOI','method','object','benchmark','hardware','baseline','results','insight','access_level','primary_urls','source_locations','unresolved']
def join_values(records,keys):
    values=[]
    for e in records:
        for k in keys:
            v=e.get(k)
            if v not in [None,'',[]]:values.append(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False))
    return ' | '.join(dict.fromkeys(values))
with (D/'文献核验清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');writer.writeheader()
    for key,r in db.items():
        es=evidence[key]
        writer.writerow(dict(key=key,authors='; '.join(auth(a) for a in r['author']),title=r['title'],year=r['year'],journal=r.get('journal',r.get('booktitle','')),volume=r.get('volume',''),issue=r.get('issue',''),pages=r.get('pages',''),DOI=r.get('doi',''),method=join_values(es,['method']),object=join_values(es,['object']),benchmark=join_values(es,['benchmark']),hardware=join_values(es,['hardware']),baseline=join_values(es,['baseline']),results=join_values(es,['quantitative_result','result']),insight=join_values(es,['insight']),access_level=r['AccessLevel'],primary_urls=join_values(es,['primary_url','additional_primary_urls','related_primary_urls','metadata_sources','documentation_url']),source_locations=join_values(es,['source_location','original_location','original_locations','原文位置','source_locations']),unresolved=join_values(es,['unresolved'])))
print('V3 corpus:',len(db),'identities;',sum(k.startswith('new_') for k in db),'new sources; all original 47 covered.')
