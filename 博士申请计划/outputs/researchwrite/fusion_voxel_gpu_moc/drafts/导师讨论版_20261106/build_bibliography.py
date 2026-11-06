"""Build verified BibTeX and an explicit claim/access matrix. No full-text inference."""
from pathlib import Path
from html import unescape
import json,csv,re
B=Path(__file__).resolve().parent; O=B/'bibliography'
records=json.loads((O/'metadata_records.json').read_text()); manual={r['id']:r for r in json.loads((O/'manual_metadata.json').read_text())}
def author(*names):return [{'family':n.split('|')[0],'given':n.split('|')[1] if '|' in n else ''} for n in names]
extra={
4:dict(author=author('Ebiwonjumi|Bamidele','Segantin|Stefano','Peterson|Ethan'),journal='Fusion Science and Technology',year=2025,volume='81',issue='1',pages='18-31'),
5:dict(author=author('车锐','刘仕倡','田卓','陈义学'),journal='核技术',year=2024,volume='47',issue='5',pages='050008'),
19:dict(author=author('宋佩涛'),year=2021,school='哈尔滨工程大学',address='哈尔滨',kind='phdthesis'),
20:dict(author=author('宋佩涛','张志俭','梁亮','张乾','赵强'),journal='原子能科学技术',year=2019,volume='53',issue='11',pages='2209-2217'),
22:dict(author=author('汪岸'),year=2025,school='北京科技大学',address='北京',kind='phdthesis'),
24:dict(author=author('Zhou|Faguo','Li|Shunde','Xue|Rong','Bu|Lingkun','Nie|Ningming','Shi|Peng','Wang|Jue','Hu|Yun','Wang|Zongguo','Wang|Yangang','Yang|Qinmeng','Yu|Miao'),year=2025,kind='misc',eprint='2503.17743',note='arXiv预印本',url='https://arxiv.org/abs/2503.17743'),
28:dict(author=author('Adinets|Andrey'),year=2014,kind='online',note='NVIDIA Technical Blog，2017年更新'),
29:dict(author=author('NVIDIA Corporation'),year=2026,kind='manual',organization='NVIDIA',note='Release 13.4，2026-10-12'),
37:dict(author=author('郑华庆','李斌','宋婧','郝丽娟','龙鹏程','胡丽琴','吴宜灿'),journal='核技术',year=2016,volume='39',issue='9',pages='090502'),
40:dict(author=author('Oak Ridge National Laboratory'),year=2026,kind='manual',organization='ORNL',note='SCALE 6.3.1手册'),
41:dict(author=author('OpenMC development team'),year=2026,kind='online',note='稳定版在线手册，访问日期2026-11-06'),
44:dict(author=author('Munk|Madicken','Slaybaugh|R. N.','Pandya|Tara M.','Johnson|Seth R.','Evans|T. M.'),title='FW/CADIS-Ω: An angle-informed hybrid method for deep-penetration radiation transport',year=2016,kind='misc',eprint='1612.00793',note='arXiv预印本；相关会议稿PHYSOR 2016',doi='10.48550/arXiv.1612.00793',url='https://arxiv.org/abs/1612.00793'),
45:dict(author=author('OECD Nuclear Energy Agency'),title='SINBAD — Shielding Integral Benchmark Archive and Database',year=2026,kind='online',url='https://harbor.oecd-nea.org/jcms/pl_32139/sinbad-shielding-integral-benchmark-archive-and-database',note='官方数据库说明，访问日期2026-11-06'),
46:dict(doi='10.1016/j.fusengdes.2019.111243',**{k:v for k,v in manual[46].items() if k not in ['id','source']}),
47:dict(author=author('Zhang|Xian','Liu|Shichang','Li|Shu','Chen|Yixue'),title='Development of multilevel mesh adaptivity for global variance reduction in Monte Carlo code cosRMC',journal='Fusion Engineering and Design',year=2024,volume='202',pages='114372',doi='10.1016/j.fusengdes.2024.114372',url='https://doi.org/10.1016/j.fusengdes.2024.114372')}
access={1:'publisher_abstract_and_supplied_prose',2:'publisher_abstract',3:'archived_publisher_abstract',4:'publisher_fulltext_selected_sections',5:'official_abstract_and_PDF_excerpt',6:'archived_fulltext_and_supplied_extract',7:'publisher_fulltext_selected_sections',8:'official_PDF_abstract_and_method_excerpt',9:'publisher_abstract_and_introduction',10:'publisher_abstract_and_introduction',11:'publisher_metadata_and_supplied_summary',12:'author_manuscript_abstract',13:'official_abstract',14:'publisher_abstract',15:'publisher_detailed_abstract',16:'publisher_abstract',17:'archived_fulltext_and_abstract',18:'official_abstract',19:'doctoral_catalogue_abstract_no_fulltext',20:'official_abstract',21:'official_SC23_abstract',22:'doctoral_catalogue_detailed_abstract_no_fulltext',23:'publisher_abstract',24:'author_manuscript_selected_sections',25:'publisher_abstract_and_conclusion_excerpt',26:'publisher_abstract',27:'author_manuscript_selected_methods',28:'archived_official_HTML_selected_sections',29:'official_13.4_manual_selected_sections',44:'original_preprint',45:'official_database_page',46:'publisher_abstract_and_institution_bibliography',47:'publisher_abstract_and_selected_sections'}
hybrid={r['candidate']:r for r in json.loads((O/'hybrid_sources.json').read_text())['records']}
claims={
1:'参数化几何与屏蔽/增殖设计迭代',2:'CIT屏蔽厚度与混凝土重复计算',3:'CAD到ITER输运模型转换及核验',4:'FNS钨钒铍多响应实验比较',5:'FNS-Duct/FNS-W cosRMC验证',6:'MOC实现与段积分、并行框架',7:'一般非结构三维MOC及资源代价',8:'MCAM几何与二维MOC、菱形差分',9:'CAD到S_N及体积加权材料',10:'固定源探测器目标导向自适应',11:'本征值目标导向误差估计',12:'浸没体材料投影与自适应',13:'八叉树非匹配笛卡儿与角通量映射',14:'空间矩比、多层扫描及原算例60%—80%成本节省',15:'DWR固定源/临界及原算例>70%节省',16:'IGA、DWR、h(p)与DSA',17:'块结构网格并行管理',18:'GPU自适应笛卡儿网格组织与构建成本',19:'ALPHA及CPU/GPU、MOC-EX研究路线',20:'二维MOC通信与扫描重叠，原五节点总体改善约8%',21:'ANT-MOC存储/通信模型、多级负载；原16000GPU扩展',22:'直接三维ANT-MOC、循环轨迹与V&V',23:'循环轨迹长度与负载模型',24:'轴向OTF与显式/分组；不采用冲突倍率',25:'直接三维、在线轴向/批处理；组件速度对单线程CPU',26:'轴向MOC/DD、异步与8/16GPU对128核CPU',27:'MOC/HFEM、DGMOC挤出限制与DFEM-S_N一般几何',28:'warp聚合原子减少冲突的一般机制',29:'合并访存、驻留、同步及性能剖析原则',44:'正伴随角信息构造替代标量重要性',45:'SINBAD类别、版本管理与许可访问',46:'CFETR线圈核响应，MAGIC加密度降低',47:'cosRMC八叉树与响应矩阵权窗及CFETR扇区'}
db=[]
for i in range(1,48):
 r=next((r for r in records if r['id']==i),{})
 c=r.get('crossref',{});m=manual.get(i,{})
 d=dict(id=i,key=f'r{i}',title=unescape(c.get('title',[r.get('title_hint','')])[0]),author=c.get('author',[]),year=int(r.get('year_hint',2026)),journal=unescape(c.get('container-title',[''])[0]),volume=c.get('volume',''),issue=c.get('issue',''),pages=c.get('page',c.get('article-number','')),kind='article')
 # Formal issue year takes priority over earlier online deposition date.
 if m:
  for k,v in m.items():
   if k not in ['id','source','author']:d[k]=v
 if not d['author'] and m:d['author']=m['author']
 ident=r.get('identifier','')
 d['doi']=ident if ident.startswith('10.') else ''
 d['url']='https://doi.org/'+d['doi'] if d['doi'] else ident
 if i in extra:d.update(extra[i])
 if i==18:d.update(title='基于GPU的并行自适应笛卡儿网格建模方法与仿真应用研究综述',author=author('任丽欣','刘树森','郭煜中','何小伟','吴恩华'),journal='计算机辅助设计与图形学学报')
 if i==21:d['kind']='inproceedings'
 if i==27:d['note']='在线发表，2026-04-23；核对作者稿方法细节'
 if i==42:d.update(year=2026,issue='sup1',pages='S485-S502')
 if i==43:d.update(year=2026,issue='2',pages='444-470')
 assert d['author'] and d['title'],i
 d['AccessLevel']=hybrid.get(i,{}).get('access_level',access.get(i,'publisher_abstract'))
 d['EvidenceSource']=hybrid.get(i,{}).get('url',d['url'])
 d['SupportedClaim']=hybrid.get(i,{}).get('supported_claim',claims.get(i,''))
 d['Boundary']=hybrid.get(i,{}).get('boundary','仅支持已读摘要/节选范围；不外推本计划速度、精度或普适优越性')
 d['MetadataSource']=('publisher-deposited Crossref JSON' if c else m.get('source','official publication/catalogue page'))
 d['LookupStatus']=r.get('metadata_status','official/manual record verified')
 if 'archived' in d['LookupStatus']:d['LookupStatus']='archived publisher Crossref record reused; fresh DOI lookup attempted'
 db.append(d)
def esc(s):return str(s).replace('\\','').replace('&amp;','&').replace('{','').replace('}','')
bibs=[]
for d in db:
 def fmt_author(a):
  fam=a.get('family',a.get('name',''));given=a.get('given','')
  if fam=='others':return 'others'
  return fam+', '+given if given else '{'+fam+'}'
 fields={'author':' and '.join(fmt_author(a) for a in d['author']),'title':'{'+esc(d['title'])+'}','year':d['year']}
 for source,target in [('journal','booktitle' if d['kind']=='inproceedings' else 'journal'),('volume','volume'),('issue','number'),('pages','pages'),('doi','doi'),('url','url'),('school','school'),('address','address'),('organization','organization'),('note','note'),('eprint','eprint')]:
  if d.get(source):fields[target]=esc(d[source])
 if d['kind'] in ['online','manual','misc']:fields['urldate']='2026-11-06'
 if d['kind']=='misc':fields['archivePrefix']='arXiv'
 if d['kind']=='inproceedings':fields['publisher']='Association for Computing Machinery';fields['address']='New York'
 bibs.append('@'+d['kind']+'{'+d['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items())+'\n}')
(O/'references.bib').write_text('\n\n'.join(bibs)+'\n')
(O/'verified_records.json').write_text(json.dumps(db,ensure_ascii=False,indent=2))
order=json.loads((O/'citation_order.json').read_text())
cols=['FinalNumber','CandidateID','Key','Title','Authors','Year','Journal','Volume','Issue','Pages','DOI','EvidenceSource','AccessLevel','SupportedClaim','Boundary','MetadataSource','LookupStatus','VerifiedDate']
with (O/'evidence_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(cols)
 for d in sorted(db,key=lambda d:order[d['key']]):
  w.writerow([order[d['key']],d['id'],d['key'],d['title'],'; '.join(a.get('family','')+' '+a.get('given','') for a in d['author']),d['year'],d.get('journal',''),d.get('volume',''),d.get('issue',''),d.get('pages',''),d.get('doi',''),d['EvidenceSource'],d['AccessLevel'],d['SupportedClaim'],d['Boundary'],d['MetadataSource'],d['LookupStatus'],'2026-11-06'])
print('Built',len(db),'references and claim/access matrix')
