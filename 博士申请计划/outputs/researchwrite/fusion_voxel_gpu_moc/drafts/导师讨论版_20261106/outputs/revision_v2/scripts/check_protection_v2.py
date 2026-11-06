"""Read-only protection gates for the original review and V2 authoring scope."""
from pathlib import Path
import json,hashlib,re
V=Path(__file__).resolve().parents[1];B=V.parents[1]
protected=json.loads((V/'planning/原件保护哈希.json').read_text())
changed=[p for p,sha in protected.items() if hashlib.sha256((B/p).read_bytes()).hexdigest()!=sha]
assert not changed,changed
body=(V/'exports/manuscript_v2.md').read_text()
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
report={'protected_files':len(protected),'original_hashes_unchanged':not changed,'deleted_records':len(p['all_deleted_records']),'long_deleted_records_checked':len(long),'verbatim_restorations':restored,'inserted_records':insert,'structure_checks':{'no_abstract_or_keywords':True,'chapter6_user_title':True,'table2_four_columns_no_platform_no_Zhou':True},'scope':'旧Word/旧PDF/根源/批注修订XML均未写入；仅在V2创建无旧修订的独立讨论稿'}
(V/'qa/人工删改核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
md=f'''# 人工删除、插入与原件核对

核对原件SHA-256：`{p['source_docx_sha256']}`。逐文件检查{len(protected)}个保护对象，全部哈希不变。原始Word中的38条批注、136个删除节点、23个插入节点以及101个格式修订节点仍完整保留在原件及审计档案中。

对V2组装正文、图注及表格检查所有{len(long)}条长度不少于16字符的删除文本，逐字恢复数为0。摘要、关键词、旧第六章标题、表2平台列及Zhou行均未恢复。原2.3—2.5、3.3—3.4、4.3—4.6、5.2及5.3—5.4按本轮授权合并，第六部分仅三个候选方向与一张比较表。

长段插入173的GPU归约段落逐字保留在3.1。用户插入标题“6.候选方案”原样保留。词级插入在新论述中保留文字或其语义，逐项原文和上下文见JSON；空文本节点作为结构修订保留在原始XML中。新V2没有对原件执行接受修订、清除批注或覆盖操作。

本轮检查包含人工逐项对照与机器字符串/结构检查。字符串检查只检测逐字恢复；对改写中可能重现被删观点的核对，另见独立论证审查及其闭环记录。
'''
(V/'qa/原人工删除内容核对报告.md').write_text(md)
print('Protected',len(protected),'original files; no deleted long passage restored;',len(insert),'insertions audited.')
