from pathlib import Path
import json,csv,hashlib,re,unicodedata,zipfile
from pypdf import PdfReader
r=Path(__file__).resolve().parents[1];out=r/'参考文献全文'
refs=json.loads((r/'sources/参考文献核验与编号记录.json').read_text())['references']
urls={1:'https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1384788/pdf',
4:'https://arxiv.org/pdf/2503.17743v1',5:'https://arxiv.org/pdf/2607.01591v1',
6:'https://www.cse.chalmers.se/edu/year/2012/course/_courses_2011/TDA361/grid.pdf',7:'https://arxiv.org/pdf/2009.12009',
9:'https://dspace.mit.edu/server/api/core/bitstreams/c3c8d02f-80f0-4d84-9b8c-dc388917a03b/content',
10:'https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf',11:'https://developer.nvidia.com/blog/cuda-pro-tip-optimized-filtering-warp-aggregated-atomics/',13:'https://web.ornl.gov/~peplowde/p068.pdf'}
versions={1:'期刊正式版',4:'arXiv预印本v1',5:'作者原始稿（arXiv）；不是25页期刊排版版',6:'公开作者版（教学网站镜像）',7:'19页期刊排版稿；首页有2021年35(6):508–526及正式DOI',9:'MIT机构仓储作者接受稿，含仓储封面',10:'官方PDF，Release 13.4',11:'官方博客全文HTML；文章内图片尽量内嵌供离线阅读',13:'作者机构公开的期刊版，21页'}
issues={2:'未查到可获取的公开全文；出版社全文需要访问权限；ANS旧站未返回可验证全文。用户确认无机构入口。',
3:'已查到作者在ResearchGate公开上传全文的记录，但当前PDF及全文页面访问返回403；未取得可验证文件。',
8:'文献为开放获取，但当前出版社及ResearchGate下载访问返回403；其他公开来源未取得可验证文件。',
12:'OpenAlex及Semantic Scholar未提供开放全文；出版社和机构页面仅有摘要或元数据。用户确认无机构入口。'}
si={1:'已检查期刊公开全文与PDF，未列独立SI下载附件；数据声明为可向作者获取，未自动联系作者。',
4:'已检查arXiv记录及全文，未列独立SI附件。',5:'已检查arXiv作者稿记录及全文，未列独立SI附件。',
6:'未发现独立SI；算法内容在正文中。',7:'已检查公开记录及19页全文，未列独立SI附件。',
9:'已检查MIT作者接受稿，未发现独立SI附件；软件仓库链接不视为SI文件，未下载整个仓库。',
10:'官方技术指南；未发现独立SI附件。',11:'官方技术博客；文内图作为HTML阅读资源保存，不计为SI。',
13:'已检查21页全文，未发现独立SI附件。'}
records=[]
norm=lambda s:''.join(re.findall('[a-z0-9]+',unicodedata.normalize('NFKC',s).lower()))
for ref in refs:
 n=ref['number'];files=list(out.glob(f'{n:02d}_*'))
 assert len(files)<=1,(n,files)
 row={'number':n,'title':ref['title'],'doi':ref.get('doi'),'status':'downloaded' if files else 'not_downloaded',
 'file':files[0].name if files else None,'source':urls.get(n),'version':versions.get(n),
 'si_requested':True,'si_files':[],'si_status':'no_separate_si_identified' if files else 'not_fully_verifiable_due_to_access',
 'si_note':si.get(n,'全文或出版社附件入口受限，不能核实是否存在独立SI；不将“未取得”写成“不存在”。'),
 'issue':issues.get(n),'checked_date':'2026-10-20'}
 if files:
  p=files[0];b=p.read_bytes();row['bytes']=len(b);row['sha256']=hashlib.sha256(b).hexdigest()
  if p.suffix=='.pdf':
   assert b.startswith(b'%PDF-');q=PdfReader(p);text=' '.join((p.extract_text() or '') for p in q.pages[:3]);assert norm(ref['title']) in norm(text),(n,'title mismatch');assert q.pages[-1].extract_text() is not None
   row['pages']=len(q.pages)
   if n==10:assert 'Release 13.4' in text
  else:
   assert 'Warp-Aggregated Atomics' in b.decode() and 'Conclusion' in b.decode();row['format']='HTML全文'
  row['validation']='文件类型、题名及PDF页数通过检查；未将摘要或验证页面当作全文。'
 else:row['validation']='未保存不完整PDF、空响应或访问验证页面。'
 records.append(row)
summary={'scope':'RP编号[1]–[13]；用户要求全文与可获取SI，未扩展书目','si_choice':'include_if_available','institutional_access':'用户明确无机构入口','total':13,'fulltexts_downloaded':sum(x['status']=='downloaded' for x in records),'pdfs':len(list(out.glob('*.pdf'))),'html_fulltexts':len(list(out.glob('*.html'))),'separate_si_files':0,'missing_numbers':[x['number'] for x in records if x['status']!='downloaded'],'records':records}
(out/'00_下载清单.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
with (out/'00_下载清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['编号','作者与题名','DOI','全文状态','文件名','版本','PDF页数','来源','补充材料检查','未取得原因'])
 for x in records:w.writerow([x['number'],x['title'],x['doi'] or '', '已下载' if x['status']=='downloaded' else '未取得全文',x['file'] or '',x['version'] or '',x.get('pages',''),x['source'] or ('https://doi.org/'+x['doi'] if x['doi'] else ''),x['si_note'],x['issue'] or ''])
lines=['# 参考文献全文下载清单','', '对应计划书参考文献[1]—[13]；核验日期：2026-10-20。','',
'**已保存9项全文：8份PDF、1篇官方HTML全文。尚有4项未取得全文，不是13项全部下载完成。**','',
'所有已取得全文均直接放在本文件夹，以编号开头命名。Kim为39页作者原始稿，OpenMOC为机构仓储作者接受稿，均已注明版本。','',
'## 全文与补充材料状态','', '| 编号 | 文献 | 全文状态与文件 | 补充材料 |','|---|---|---|---|']
for x in records:
 author=refs[x['number']-1]['authors'][0].get('family') or 'NVIDIA'
 label=f"{author} {refs[x['number']-1]['year']}"
 state=f"[{x['file']}]({x['file']})" if x['file'] else '**未取得全文**'
 lines.append(f"| [{x['number']}] | {label} | {state} | {x['si_note']} |")
lines+=['','## 未取得的4项','']
for x in records:
 if x['status']!='downloaded':
  lines.append(f"- [{x['number']}] **{x['title']}**。{x['issue']} [DOI与出版信息](https://doi.org/{x['doi']})。")
lines+=['','## 文件与版本说明','',
'- [4]、[5]、[9]复用了前期已下载的公开全文，并重新校验题名、文件类型及页数后集中复制；来源链接记录于CSV／JSON。',
'- [7]从arXiv取得的PDF本身是2021年期刊排版稿，首页含正式DOI；不因下载域名为arXiv而冒称另一篇论文。',
'- [11]原始来源是技术博客，保存为HTML全文，不将网页伪装成期刊PDF。',
'- 已逐项检查可访问页面与全文中的SI线索，目前未取得独立补充附件；“未发现公开附件”不等于证明不存在附件。受访问限制的条目明确保留未能核实状态。',
'- 文件完整性记录（页数、字节数、SHA-256）、来源及失败原因见00_下载清单.json；空文件、截断PDF及403验证页未纳入全文文件夹。',
'- 本批仅下载既定13项书目，未下载被它们引用的其他论文或整个软件仓库。','']
(out/'00_下载清单.md').write_text('\n'.join(lines))
# Convenient archive contains the same one-folder collection and no QA intermediates.
archive=r/'参考文献全文.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):
  if p.is_file():z.write(p,arcname='参考文献全文/'+p.name)
assert summary['fulltexts_downloaded']==9 and summary['missing_numbers']==[2,3,8,12]
(r/'qa_logs/参考文献下载最终核验.json').write_text(json.dumps({k:v for k,v in summary.items() if k!='records'},ensure_ascii=False,indent=2))
p=r/'state.json';j=json.loads(p.read_text());j['reference_download']={'status':'partial_no_institutional_access','directory':'参考文献全文','archive':'参考文献全文.zip','downloaded':9,'total':13,'missing_numbers':[2,3,8,12],'si_requested':True,'si_files_downloaded':0};p.write_text(json.dumps(j,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='records'},ensure_ascii=False,indent=2))
print('Folder:',out.resolve());print('Archive:',archive.resolve(),archive.stat().st_size)
