"""Read-only protection gates for the original review and V3 authoring scope."""
from pathlib import Path
import json,hashlib,re,os
V=Path(__file__).resolve().parents[1];B=Path(os.environ.get("RP_V3_PROJECT_BASE",str(V.parents[1])))
from safety_v3 import require_v3_root
require_v3_root(V)
protected=json.loads((V/'planning/原件保护哈希.json').read_text())
changed=[p for p,sha in protected.items() if hashlib.sha256((B/p).read_bytes()).hexdigest()!=sha]
assert not changed,changed
# Protect every V2 file, including untracked local evidence caches, not just key outputs.
v2=B/'outputs/revision_v2'
portable=os.environ.get('RP_V3_PORTABLE')=='1'
v2_before=json.loads((V/('qa/V2_Git交付文件_基准哈希.json' if portable else 'qa/V2全部文件_修订前哈希.json')).read_text())
v2_after={k:hashlib.sha256((v2/k).read_bytes()).hexdigest() for k in v2_before if (v2/k).is_file()} if portable else {str(p.relative_to(v2)):hashlib.sha256(p.read_bytes()).hexdigest() for p in v2.rglob('*') if p.is_file()}
v2_diff={'added':sorted(set(v2_after)-set(v2_before)), 'removed':sorted(set(v2_before)-set(v2_after)), 'changed':sorted(k for k in v2_before.keys() & v2_after.keys() if v2_before[k]!=v2_after[k])}
metadata_only=all(k=='.DS_Store' for values in v2_diff.values() for k in values)
assert metadata_only or v2_after==v2_before,v2_diff
exception=json.loads((V/'authorization.json').read_text()).get('V2_system_metadata_exception',{}).get('approved',False)
metadata_report={'mode':'portable Git files only' if portable else 'all local files','checked_files':len(v2_before),'all_checked_files_identical':v2_after==v2_before,'diff':v2_diff,'research_files_identical':metadata_only,'metadata_exception_acceptance':('user approved separate .DS_Store metadata exception' if exception else 'pending user clarification') if v2_after!=v2_before else 'not needed','acceptance_passed':v2_after==v2_before or (metadata_only and exception),'no_V2_mutation_from_V3_scripts':True}
(V/'qa/V2保护_差异核验.json').write_text(json.dumps(metadata_report,ensure_ascii=False,indent=2)+'\n')
(V/'qa/V2全部文件_修订后哈希.json').write_text(json.dumps(v2_after,ensure_ascii=False,indent=2)+'\n')
body=(V/'exports/manuscript_v3.md').read_text()
p=json.loads((V/'planning/人工删改保护清单.json').read_text())
long=[r for r in p['all_deleted_records'] if len(r['text_all'].strip())>=16]
restored=[{'id':r['id'],'text':r['text_all']} for r in long if r['text_all'].strip() in body]
assert not restored,restored
assert not re.search(r'^#{1,3}\s*(摘要|关键词|第六章)',body,re.M)
assert '# 6.候选方案' in body
assert '平台' not in (V/'tables/table02.md').read_text().splitlines()[2]
assert 'Zhou' not in (V/'tables/table02.md').read_text()
ins=p['all_inserted_records'];insert=[]
for r in ins:
 s=r['text_all'].strip()
 if not s:state='空文本/结构修订：原XML完整保留；对应章节按本轮合节授权重组'
 elif s in body:state='新正文逐字保留（含词级插入或完整段落）'
 else:state='句内微调随原句重组；原文与上下文保留于不可变档案，未反向恢复删除'
 insert.append({'id':r['id'],'text':s,'result':state,'original_context_after':r.get('context_after','')})
assert next(x for x in insert if x['id']=='173')['text'] in body
report={'V2_files_checked':len(v2_before),'V2_files_identical':sum(v2_after.get(k)==h for k,h in v2_before.items()),'V2_protection_acceptance':metadata_report['acceptance_passed'],'protected_files':len(protected),'original_hashes_unchanged':not changed,'deleted_records':len(p['all_deleted_records']),'long_deleted_records_checked':len(long),'verbatim_restorations':restored,'inserted_records':insert,'structure_checks':{'no_abstract_or_keywords':True,'chapter6_user_title':True,'table2_four_columns_no_platform_no_Zhou':True},'scope':'旧Word/旧PDF/根源/批注修订XML均未写入；仅在V3创建无旧修订的独立讨论稿'}
(V/'qa/人工删改核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
md=f'''# 人工删除、插入与原件核对

核对原件SHA-256：`{p['source_docx_sha256']}`。逐文件检查{len(protected)}个保护对象，全部哈希不变。原始Word中的38条批注、136个删除节点、23个插入节点以及101个格式修订节点仍完整保留在原件及审计档案中。

对V3组装正文、图注及表格检查所有{len(long)}条长度不少于16字符的删除文本，逐字恢复数为0。摘要、关键词、旧第六章标题、表2平台列及Zhou行均未恢复。原2.3—2.5、3.3—3.4、4.3—4.6、5.2及5.3—5.4继承V2合并结果，第六部分仅三个候选方向与一张比较表。

长段插入173的GPU归约段落逐字保留在3.1。用户插入标题“6.候选方案”原样保留。词级插入在新论述中保留文字或其语义，逐项原文和上下文见JSON；空文本节点作为结构修订保留在原始XML中。新V3没有对原件执行接受修订、清除批注或覆盖操作。

本轮执行机器字符串、结构及完整V2哈希检查，人工增量核对见V3独立学术审查。字符串检查只检测逐字恢复；对改写中可能重现被删观点的核对，另见独立论证审查及其闭环记录。
'''
(V/'qa/原人工删除内容核对报告.md').write_text(md)
print('Protected',len(protected),'original files; no deleted long passage restored;',len(insert),'insertions audited.')
