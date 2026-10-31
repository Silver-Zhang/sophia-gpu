"""Number only existing citations; preserve narrative, metadata provenance, and locators."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'exports/博士科研计划书_唯一审查底稿.md'
SOURCE=ROOT/'sources/参考文献编号前正文快照.md'
DATE='2026-10-20'
raw=TARGET.read_text()
if '\n## 参考文献\n' in raw:
    raw=SOURCE.read_text()
else:
    SOURCE.write_text(raw)
cr=json.loads((ROOT/'sources/参考文献_Crossref逐条核验.json').read_text())
def record(doi,key,other_sources,note=''):
    r=cr[doi]['record']
    return {'key':key,'authors':[{'given':a['given'],'family':a['family']} for a in r['author']],
      'title':r['title'][0],'year':(r.get('published-print') or r['published'])['date-parts'][0][0],
      'venue':r['container-title'][0],'volume':r.get('volume'),'issue':r.get('issue'),'pages':r.get('page'),
      'article_number':r.get('article-number'),'doi':doi,'type':'J','status':'正式发表',
      'online_date':r.get('published-online',{}).get('date-parts'),
      'sources':[cr[doi]['source']]+other_sources,'verification':'已核验','notes':note,'pending':[]}
refs=[]
refs.append(record('10.3389/fnuen.2024.1384788','moreno2024',[
 'https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1384788/pdf',
 'https://cnerg.github.io/community/people/cam/']))
refs.append(record('10.13182/FST91-A29687','liew1991',[
 'https://www.tandfonline.com/doi/abs/10.13182/FST91-A29687',
 'https://www.ans.org/pubs/journals/fst/volume-20/'],
 '按原刊卷年1991著录；2017-05-09为旧文数字化上线日期，不改作出版年。刊名按原刊Fusion Technology。'))
refs.append(record('10.1016/j.fusengdes.2007.06.038','tsige2007',[
 'https://www.sciencedirect.com/science/article/pii/S0920379607003407'],
 '作者按登记顺序H. Tsige-Tamirat、U. Fischer、A. Serikov、S. Stickel，保留官方已给出的首字母，不自行扩展名字。'))
z=json.loads((ROOT/'sources/zhou_datacite.json').read_text())['data']['attributes']
refs.append({'key':'zhou2025','authors':[{'given':x['givenName'],'family':x['familyName']} for x in z['creators']],
 'title':z['titles'][0]['title'],'year':2025,'venue':'arXiv:2503.17743v1','doi':'10.48550/arXiv.2503.17743',
 'type':'EB/OL','status':'预印本','date':'2025-03-22','sources':['https://arxiv.org/abs/2503.17743v1','https://api.datacite.org/dois/10.48550/arXiv.2503.17743','https://arxiv.org/html/2503.17743v1'],
 'verification':'已核验','notes':'按arXiv v1提交记录著录；12位作者逐名核对。当前arXiv记录注明已投同行评议期刊，未提供可核实的正式期刊出处；本稿继续引用预印本，不推断已正式发表。HTML自动渲染日期不作为发表年。','pending':[]})
kim=record('10.1080/00295639.2026.2652773','kim2026',[
 'https://www.tandfonline.com/doi/abs/10.1080/00295639.2026.2652773'],
 '出版社及Crossref均列2026-04-23在线发表；当前记录无卷期，页码1–25为在线版本页码，不补造卷期。')
kim['status']='已在线发表（online first），卷期待分配'
refs.append(kim)
a=json.loads((ROOT/'sources/amanatides_datacite.json').read_text())['data']['attributes']
refs.append({'key':'amanatides1987','authors':[{'given':x['givenName'],'family':x['familyName']} for x in a['creators']],
 'title':a['titles'][0]['title'],'year':1987,'venue':'EG 1987—Technical Papers','publisher':'Eurographics Association',
 'doi':'10.2312/egtp.19871000','type':'C','status':'会议论文正式发表',
 'sources':['https://api.datacite.org/dois/10.2312/egtp.19871000','https://diglib.eg.org/collections/ce7b470e-6b6a-472c-9702-afbe7ce326b1','https://www.cs.yorku.ca/~amana/research/grid.pdf'],
 'verification':'已核验','notes':'Crossref返回404，但DataCite登记可查且Eurographics官方BibTeX一致；不是无效DOI。官方登记未给出页码，本次不凭记忆补页码。','pending':[]})
refs.append(record('10.1177/10943420211022811','zhang2021',[
 'https://journals.sagepub.com/doi/10.1177/10943420211022811','https://amrex-codes.github.io/amrex/publications.html','https://arxiv.org/pdf/2009.12009'],
 '统一著录2021年正式期刊版35(6):508–526，不另编预印本条目。§5.2题为Regridding and load balancing，按正式排版稿核对。'))
refs.append(record('10.1080/00295450.2021.1871995','gaston2021',[
 'https://www.tandfonline.com/doi/pdf/10.1080/00295450.2021.1871995','https://inl.elsevierpure.com/en/publications/method-of-characteristics-for-3d-full-core-neutron-transport-on-u/']))
refs.append(record('10.1016/j.anucene.2013.12.012','boyd2014',[
 'https://www.sciencedirect.com/science/article/pii/S0306454913006634','https://dspace.mit.edu/server/api/core/bitstreams/c3c8d02f-80f0-4d84-9b8c-dc388917a03b/content'],
 '按正式卷年2014著录，DOI字符串中的2013不作为出版年。'))
refs.append({'key':'nvidia_guide','authors':[{'literal':'NVIDIA Corporation'}],
 'title':'CUDA C++ Best Practices Guide','year':2026,'version':'Release 13.4','date':'2026-10-12',
 'type':'EB/OL','status':'官方技术文档，已发布','doi':None,
 'url':'https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf',
 'sources':['https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf','https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html'],
 'verification':'已核验','notes':'作者、版本和日期据官方PDF封面。§9.1 Timing、§9.1.1 Using CPU Timers、§9.1.2 Using CUDA GPU Timers核对；网页未列DOI，不补造。HTML为滚动页面，以本次查阅的13.4版为准。','pending':[]})
refs.append({'key':'adinets2014','authors':[{'given':'Andy','family':'Adinets'}],
 'title':'CUDA Pro Tip: Optimized Filtering with Warp-Aggregated Atomics','year':2014,'date':'2014-10-01',
 'updated':'2017-11','venue':'NVIDIA Technical Blog','type':'EB/OL','status':'官方技术博客，已发布并更新','doi':None,
 'url':'https://developer.nvidia.com/blog/cuda-pro-tip-optimized-filtering-warp-aggregated-atomics/',
 'sources':['https://developer.nvidia.com/blog/cuda-pro-tip-optimized-filtering-warp-aggregated-atomics/'],
 'verification':'已核验','notes':'署名作者为Andy Adinets；网页注明2014-10-01发布、2017年11月更新。网页未列DOI，不补造。','pending':[]})
refs.append(record('10.1016/j.anucene.2012.11.029','baker2013',[
 'https://researchprofiles.herts.ac.uk/en/publications/goal-based-mesh-adaptivity-for-fixed-source-radiation-transport-c/',
 'https://www.sciencedirect.com/journal/annals-of-nuclear-energy/vol/55/suppl/C'],
 '按正式卷年2013著录，DOI字符串中的2012不作为出版年。保留全部7位作者。'))
refs.append(record('10.13182/NSE12-33','wagner2014',[
 'https://impact.ornl.gov/en/publications/fw-cadis-method-for-global-and-regional-variance-reduction-of-mon/',
 'https://web.ornl.gov/~peplowde/p068.pdf'],
 '原刊为2014年176(1):37–57；2017-03-22为旧文数字化上线日期。正文引用仅在第11节。'))
for i,r in enumerate(refs,1): r['number']=i;r['checked_date']=DATE
bykey={r['key']:r for r in refs}
def key_for_url(u):
    v=u.lower()
    if '2503.17743' in v:return 'zhou2025'
    if 'docs.nvidia.com/cuda/' in v:return 'nvidia_guide'
    if 'developer.nvidia.com/blog/' in v:return 'adinets2014'
    for r in refs:
        if r.get('doi') and r['doi'].lower() in v:return r['key']
    raise ValueError(u)
pattern=r'\[([^\]]+)\]\((https?://[^)]+)\)'
occ=[]
chapter=None
for lineno,line in enumerate(raw.splitlines(),1):
    cm=re.match(r'### (\d+\.\d+)',line)
    if cm:chapter=cm.group(1)
    for m in re.finditer(pattern,line):
        r=bykey[key_for_url(m.group(2))]
        occ.append({'number':r['number'],'key':r['key'],'section':chapter,'original_line':lineno,'original_label':m.group(1),'original_url':m.group(2)})
assert list(dict.fromkeys(o['number'] for o in occ))==list(range(1,14))
def replace_citation(m):
    label,u=m.groups();r=bykey[key_for_url(u)];n=r['number']
    loc=''
    if '图8' in label:loc='，图8'
    elif '表1、图6及第5节' in label:loc='，表1、图6及第5节'
    elif '§5.2' in label:loc='，§5.2'
    elif label.startswith('§9.1.1'):loc='，§9.1.1'
    elif label.startswith('§9.1.2'):loc='，§9.1.2'
    lead=label if r['key']=='wagner2014' else ''
    return lead+f'[{n}{loc}](#ref-{n})'
numbered=re.sub(pattern,replace_citation,raw)
# Exact narrative invariance: only citation labels/links and the appended list may change.
def before_normalized(s):
    return re.sub(pattern,lambda m:m.group(1) if key_for_url(m.group(2))=='wagner2014' else '',s)
def after_normalized(s):
    return re.sub(r'\[\d+(?:，[^\]]+)?\]\(#ref-\d+\)','',s)
assert before_normalized(raw)==after_normalized(numbered),'Non-citation narrative changed'

def short_author(a):
    if 'literal' in a:return a['literal']
    initials=' '.join(x[0].upper() for x in re.findall(r'[A-Za-z]+',a['given']))
    return a['family']+' '+initials

def entry(r):
    authors=', '.join(short_author(a) for a in r['authors'])
    line=f"{authors}. {r['title']}[{r['type']}]. "
    if r['key']=='zhou2025':
        line+=f"arXiv:2503.17743v1, 2025-03-22（预印本）[引用日期：{DATE}]. "
    elif r['type']=='J':
        line+=f"{r['venue']}, {r['year']}"
        if r.get('volume'):line+=', '+r['volume']
        if r.get('issue'):line+='('+r['issue']+')'
        if r.get('pages'):line+=': '+r['pages'].replace('-', '–')
        elif r.get('article_number'):line+=': '+r['article_number']
        if r['key']=='kim2026':line+='（已在线发表，online first；2026-04-23；卷期待分配）'
        line+='. '
    elif r['type']=='C':line+=f"{r['venue']}. {r['publisher']}, {r['year']}. "
    elif r['key']=='nvidia_guide':line+=f"Release 13.4, 2026-10-12[引用日期：{DATE}]. "
    else:line+=f"{r['venue']}, 2014-10-01（2017年11月更新）[引用日期：{DATE}]. "
    if r.get('doi'):line+=f"DOI: [{r['doi']}](https://doi.org/{r['doi']})."
    else:line+=f"[{r['url']}]({r['url']})（官方页面未列DOI）。"
    if r['pending']:line+=' [待核实：'+'；'.join(r['pending'])+']'
    return f"<a id=\"ref-{r['number']}\"></a>\n\n[{r['number']}] "+line
bibliography='\n\n## 参考文献\n\n'+'\n\n'.join(entry(r) for r in refs)+'\n'
TARGET.write_text(numbered.rstrip()+bibliography)
(ROOT/'sources/参考文献核验与编号记录.json').write_text(json.dumps({'checked_date':DATE,'references':refs,'citations':occ},ensure_ascii=False,indent=2))
# Audit table retains complete author spelling and detailed field evidence.
lines=['# 参考文献逐条核验与正文编号对应','',f'核验日期：{DATE}。仅整理既有13项来源，不增补研究文献，不调整正文论证。','',
'作者逐字段核验保留在JSON记录中；下表和文末条目列出全部作者，不以“等”省略。','',
'| 编号 | 作者（登记顺序） | 题名 | 年份／发表状态 | DOI | 正文位置 | 核验来源与结论 |','|---|---|---|---|---|---|---|']
for r in refs:
    au='; '.join(a.get('literal') or (a['given']+' '+a['family']) for a in r['authors'])
    sections='、'.join(dict.fromkeys(o['section'] for o in occ if o['number']==r['number']))
    sources='；'.join('[来源'+str(i)+']('+u+')' for i,u in enumerate(r['sources'],1))
    doi='['+r['doi']+'](https://doi.org/'+r['doi']+')' if r.get('doi') else '官方页面未列DOI；不补造'
    lines.append(f"| [{r['number']}] | {au} | {r['title']} | {r['year']}；{r['status']} | {doi} | {sections} | {r['verification']}；{sources} |")
lines+=['','## 日期、版本及核验说明','']
for r in refs:
    if r.get('notes'):lines.append(f"- [{r['number']}] {r['notes']}")
lines+=['','## 核验结论与边界','',
'13项来源的作者、题名、年份和引用版本均已核验；11项学术来源的DOI均可在Crossref或DataCite中匹配，2项NVIDIA官方网络资料未列DOI。',
'Kim文献尚无可核验卷期，明确标为online first及卷期待分配，不视为文献身份待核实；Amanatides–Woo条目不补未经本轮核实的页码。',
'本轮没有需要以“待核实”占位的作者、题名、年份或DOI字段；若后续新增字段而无证据，必须标注待核实，不从记忆补齐。',
'本次核验范围是书目信息、发表状态和引文对应关系，不将元数据匹配解释为已重新验证正文全部机制或性能结论。','']
(ROOT/'exports/参考文献核验表.md').write_text('\n'.join(lines))
# Number/source/locator scope checks.
final=TARGET.read_text();main=final.split('\n## 参考文献\n')[0]
nums=[int(x) for x in re.findall(r'\]\(#ref-(\d+)\)',main)]
assert len(nums)==len(occ) and set(nums)==set(range(1,14))
assert len(re.findall(r'^\[\d+\] ',final,re.M))==13
assert main.count('Wagner')==1
assert all(o['section'].startswith('11.') for o in occ if o['key']=='wagner2014')
assert not re.search(pattern,main),'Unexpected unnumbered external citation'
qa={'checked_date':DATE,'unique_references':13,'citation_occurrences':len(occ),
 'doi_verified':11,'official_web_sources_without_listed_doi':2,'core_fields_pending':0,
 'narrative_changed':False,'numbering':'first occurrence; shared number for repeated source',
 'locators_preserved':['图8','表1、图6及第5节','§5.2','§9.1.1','§9.1.2'],
 'wagner_only_body_section':'11.1','source_snapshot':str(SOURCE.relative_to(ROOT)),
 'final_sha256':hashlib.sha256(final.encode()).hexdigest(),
 'tests':['narrative invariant after removing citation markers','13 unique sources and contiguous numbering',f'{len(occ)} original citation occurrences mapped one-to-one','no unresolved external citation links','no orphan bibliography entries','Wagner confined to section 11 in body'],
 'note':'Literature scope unchanged. Known future volume/issue assignment not invented.'}
(ROOT/'qa_logs/参考文献编号核验记录.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
qpath=ROOT/'qa_logs/合并底稿核验记录.json'
q=json.loads(qpath.read_text());q['sha256']=qa['final_sha256'];q['characters']=len(final);q['references_added']=13;q['reference_check']=str((ROOT/'qa_logs/参考文献编号核验记录.json').relative_to(ROOT));q['next_action']='user review of verified references; no narrative rewriting'
qpath.write_text(json.dumps(q,ensure_ascii=False,indent=2))
p=ROOT/'state.json';state=json.loads(p.read_text());state['current_status']='references_verified_numbered_awaiting_user_review';state['next_step']='Review numbered reference list and verification report; no body revisions authorized in this round.';state['reference_verification_report']='exports/参考文献核验表.md';p.write_text(json.dumps(state,ensure_ascii=False,indent=2))
print(json.dumps(qa,ensure_ascii=False,indent=2))
