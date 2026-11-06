"""Archive every review record and synchronize text sources without writing a DOCX.

The source projection omits deleted material and includes inserted material. This
does not accept/reject revisions in the review Word, which remains byte-for-byte
unchanged. Formatting revisions are retained losslessly in the snapshot and XML.
"""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from difflib import SequenceMatcher
from lxml import etree as E
import argparse, csv, hashlib, io, json, re, subprocess

B = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=B, text=True).strip())
REL = B.relative_to(ROOT)
DOC = B / 'outputs/博士研究设想_导师讨论初稿.docx'
BASELINE = 'fefbfd3a7f00a85cf2721fd92b0764afc2b56032'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
NS = {'w': W[1:-1], 'm': M[1:-1]}
REV_TAGS = {'ins', 'del', 'moveFrom', 'moveTo', 'cellIns', 'cellDel', 'cellMerge'}

def sha(data): return hashlib.sha256(data).hexdigest()
def dump(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def old_file(relative):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + str(REL / relative)], cwd=ROOT)

def text(node, mode='after', math_markup=False):
    if mode == 'after' and node.tag in {W+'del', W+'moveFrom'}: return ''
    if mode == 'before' and node.tag in {W+'ins', W+'moveTo'}: return ''
    if E.QName(node).localname.endswith('PrChange'): return ''
    if mode == 'after' and node.tag == W+'tr' and node.find(W+'trPr/'+W+'del') is not None: return ''
    if mode == 'after' and node.tag == W+'tc' and node.find(W+'tcPr/'+W+'cellDel') is not None: return ''
    if node.tag == M+'oMath' and math_markup:
        value = text(node, mode)
        inline = {'SN': 'S_N', 'I-1': 'I^{-1}', 'I−1': 'I^{-1}',
                  'Ri': 'R_i', 'βi': r'\beta_i', 'q†': r'q^{\dagger}'}
        return '$' + inline.get(value, value) + '$'
    if node.tag in {W+'t', W+'delText', M+'t'}: return node.text or ''
    if node.tag == W+'tab': return '\t'
    if node.tag == W+'br': return '\n'
    return ''.join(text(c, mode, math_markup) for c in node)

def unpack(data):
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        parts = {n: z.read(n) for n in z.namelist()}
    roots = {n: E.fromstring(v) for n,v in parts.items() if n.startswith('word/') and n.endswith('.xml')}
    return parts, roots, list(roots['word/document.xml'].find(W+'body'))

def norm(t):
    return re.sub(r'\s+', '', t).replace('−', '-').replace('𝖳', 'T')

def citation_numbers(value):
    if not re.fullmatch(r'\d+(?:[–—-]\d+)?(?:,\d+(?:[–—-]\d+)?)*', value): return None
    out = []
    for part in value.split(','):
        pair = re.split('[–—-]', part)
        out.extend(range(int(pair[0]),int(pair[1])+1) if len(pair)==2 else [int(pair[0])])
    return out if out and max(out)<=47 and min(out)>=1 else None

def normalized_references(t):
    def sub(m):
        nums = citation_numbers(m.group(1))
        return '['+','.join(map(str,sorted(nums)))+']' if nums else m.group()
    return re.sub(r'\[([0-9,–—-]+)\]',sub,t)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--apply',action='store_true'); args=ap.parse_args()
    data=DOC.read_bytes(); digest=sha(data)
    state_path=B/'review_state.json'
    if args.apply and state_path.exists():
        previous=json.loads(state_path.read_text())
        changed=[name for name,digest0 in previous['source_sha256'].items() if sha((B/name).read_bytes())!=digest0]
        assert not changed,('现行源已有后续修改，禁止用旧Word覆盖；请先人工核对',changed)
    parts,roots,current=unpack(data)
    _,_,baseline=unpack(old_file('outputs/博士研究设想_导师讨论初稿.docx'))
    archive=B/'review_archive'/digest[:12]
    archive.mkdir(parents=True,exist_ok=True)
    snapshot=archive/'用户批注修订原件.docx'
    if snapshot.exists(): assert snapshot.read_bytes()==data
    else: snapshot.write_bytes(data)
    original_snapshot=archive/'初稿基线_只读.docx'
    if not original_snapshot.exists():original_snapshot.write_bytes(old_file('outputs/博士研究设想_导师讨论初稿.docx'))
    raw=archive/'ooxml';raw.mkdir(exist_ok=True)
    for name,value in parts.items():
        if name.endswith(('.xml','.rels')):
            target=raw/name; target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(value)
    # Preserve the old generating sources separately; deleted prose is audit-only.
    saved=archive/'生成源文件_同步前';saved.mkdir(exist_ok=True)
    for name in ['sources_ch%02d.md'%i for i in range(1,7)]+['outputs/manuscript.md','table_sources.md','assemble_manuscript.py','rebuild.py']:
        target=saved/name;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists(): target.write_bytes(old_file(name))

    comments=[];croot=roots.get('word/comments.xml')
    w14='{http://schemas.microsoft.com/office/word/2010/wordml}'
    w15='{http://schemas.microsoft.com/office/word/2012/wordml}'
    extended=roots.get('word/commentsExtended.xml')
    ex_by_para={n.get(w15+'paraId'):dict(n.attrib) for n in extended} if extended is not None else {}
    for c in croot.findall(W+'comment') if croot is not None else []:
        ident=c.get(W+'id'); starts=[];ends=[];refs=[]
        for i,block in enumerate(current):
            for tag,dest in [('commentRangeStart',starts),('commentRangeEnd',ends),('commentReference',refs)]:
                dest.extend(i for n in block.iter(W+tag) if n.get(W+'id')==ident)
        assert len(starts)==len(ends)==len(refs)==1,(ident,starts,ends,refs)
        lo,hi=starts[0],ends[0]
        last_para=c.findall(W+'p')[-1]
        ex=ex_by_para.get(last_para.get(w14+'paraId'),{})
        comments.append({'id':ident,'author':c.get(W+'author'),'date':c.get(W+'date'),
                         'text':text(c),'start_block':lo,'end_block':hi,'reference_block':refs[0],
                         'context_before':'\n'.join(text(x,'before') for x in current[lo:hi+1]),
                         'context_after':'\n'.join(text(x) for x in current[lo:hi+1]),
                         'original_resolved':ex.get(w15+'done')=='1','extended_metadata':ex,
                         'status':'保留原批注，待逐条处理；未按批注擅自改写',
                         'xml':E.tostring(c,encoding='unicode')})
    revisions=[]
    for part,root in roots.items():
        for node in root.iter():
            kind=E.QName(node).localname
            if kind in REV_TAGS or kind.endswith('PrChange'):
                block=next((i for i,b in enumerate(current) if node is b or b in node.iterancestors()),None) if part=='word/document.xml' else None
                revisions.append({'part':part,'xpath':node.getroottree().getpath(node),'type':kind,
                                  'id':node.get(W+'id'),'author':node.get(W+'author'),'date':node.get(W+'date'),
                                  'body_block':block,'text_all':''.join(node.xpath('.//w:t/text() | .//w:delText/text() | .//m:t/text()',namespaces=NS)),
                                  'context_before':text(current[block],'before') if block is not None else '',
                                  'context_after':text(current[block]) if block is not None else '',
                                  'xml':E.tostring(node,encoding='unicode')})
    dump(archive/'comments.json',comments);dump(archive/'revisions.json',revisions)
    with (archive/'批注处理清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['批注ID','作者','原始UTC时间','批注全文','原文块起点','原文块终点','修订前上下文','保留文本上下文','原始已解决状态','处理状态'])
        for c in comments:writer.writerow([c['id'],c['author'],c['date'],c['text'],c['start_block'],c['end_block'],c['context_before'],c['context_after'],c['original_resolved'],c['status']])
    # Comparing with the original delivered Word also catches untracked edits.
    old=[norm(text(x)) for x in baseline];before=[norm(text(x,'before')) for x in current]
    mapping={};direct=[];deleted_baseline=[]
    for tag,i,j,k,l in SequenceMatcher(None,old,before,autojunk=False).get_opcodes():
        if tag!='equal': direct.append({'operation':tag,'baseline_blocks':[i,j],'review_blocks':[k,l],
                                       'baseline':[text(x) for x in baseline[i:j]],
                                       'review_before_tracked_changes':[text(x,'before') for x in current[k:l]]})
        if tag=='equal' or (tag=='replace' and j-i==l-k):mapping.update({k+n:i+n for n in range(l-k)})
        elif tag=='delete':deleted_baseline.extend(range(i,j))
        elif tag=='replace':
            available=set(range(k,l))
            for bi in range(i,j):
                match=max(available,key=lambda ci:SequenceMatcher(None,old[bi],before[ci]).ratio())
                assert SequenceMatcher(None,old[bi],before[match]).ratio()>.80,(bi,match)
                mapping[match]=bi;available.remove(match)
    dump(archive/'untracked_and_structural_differences.json',direct)
    order=json.loads(old_file('bibliography/citation_order.json')); reverse={v:k for k,v in order.items()}
    equation_ids=re.findall(r'\{#(eq-[a-zA-Z]+)\}',old_file('outputs/manuscript.md').decode())
    eq_numbers={key:i+1 for i,key in enumerate(equation_ids)}
    def source_plain(s):
        s=re.sub(r'^#{1,3}\s+','',s)
        s=re.sub(r'^%%\s+\S+\s*','',s)
        def citations(m):return '['+','.join(str(n) for n in sorted(order[k] for k in re.findall(r'@(r\d+)',m.group())))+']'
        s=re.sub(r'\[@r\d+(?:;\s*@r\d+)*\]',citations,s)
        s=re.sub(r'@(eq-[a-zA-Z]+)',lambda m:'式（%d）'%eq_numbers[m.group(1)],s)
        s=s.replace('$S_N$','SN').replace('S_N','SN')
        s=s.replace(r'\mathcal L','L').replace(r'\dagger','†').replace(r'\beta','β')
        s=re.sub(r'\$([^$]+)\$',lambda m:re.sub(r'[{}_^]','',m.group(1)),s)
        return norm(normalized_references(s))
    def keys(t):
        def sub(m):
            nums=citation_numbers(m.group(1))
            return '['+'; '.join('@'+reverse[n] for n in nums)+']' if nums else m.group()
        return re.sub(r'\[([0-9,–—-]+)\]',sub,t)
    chunks=re.split(r'\n\s*\n',old_file('outputs/manuscript.md').decode().strip())
    src_map={};used=set();special={};tables=[];images=[];equations=[]
    for i,b in enumerate(baseline):
        if b.tag==W+'tbl':tables.append(i)
        elif b.find('.//'+W+'drawing') is not None:images.append(i)
        elif b.find('.//'+M+'oMathPara') is not None or (b.findall(M+'oMath') and re.search('（[1-8]）',text(b))):equations.append(i)
    # Exported numbered equations use oMath inside a tabbed paragraph.
    equations=[i for i,b in enumerate(baseline) if b.tag==W+'p' and b.find('.//'+M+'oMath') is not None and re.fullmatch('（[1-8]）',norm(''.join(b.xpath('.//w:t/text()',namespaces=NS))))]
    table_iter=iter(tables);image_iter=iter(images);equation_iter=iter(equations)
    missing=[]
    for chunk in chunks:
        if chunk.startswith('---\n') or chunk.startswith('{{<'):continue
        if chunk.startswith('|'):target=next(table_iter)
        elif chunk.startswith('!['):target=next(image_iter)
        elif chunk.startswith('$$'):target=next(equation_iter)
        else:
            candidate=source_plain(chunk)
            matches=[i for i,b in enumerate(baseline) if i not in used and b.tag==W+'p' and norm(normalized_references(text(b)))==candidate]
            if not matches:
                ranked=sorted(((SequenceMatcher(None,candidate,norm(normalized_references(text(b)))).ratio(),i) for i,b in enumerate(baseline) if i not in used and b.tag==W+'p' and text(b).strip()),reverse=True)
                if ranked and ranked[0][0]>.92:matches=[ranked[0][1]]
            if not matches:missing.append(chunk[:150]);continue
            target=matches[0]
        assert target not in used,target
        src_map[target]=chunk;used.add(target)
    assert not missing,missing
    chapter_starts=[i for i,b in enumerate(baseline) if re.match('第[一二三四五六]章 ',text(b))]
    assert len(chapter_starts)==6
    def chapter(bi):return sum(bi>=start for start in chapter_starts)
    ref_start=next(i for i,b in enumerate(baseline) if text(b)=='参考文献')
    units=[];changes=[];table_exports=[];unmapped=[]
    for ci,block in enumerate(current):
        bi=mapping.get(ci)
        value=text(block).strip()
        if bi is not None and bi>=ref_start:continue
        if bi is None:
            if not value:continue
            # The review inserts this exact plain paragraph before old chapter 6.
            following=next((mapping[j] for j in range(ci+1,len(current)) if j in mapping),ref_start)
            ch=chapter(following)
            if value=='6.候选方案':units.append((ch,keys(text(block,math_markup=True).strip()),ci,None));continue
            unmapped.append((ci,value));continue
        source=src_map.get(bi)
        if source is None:
            # TOC is a Word SDT; empty layout paragraphs and sectPr are not prose.
            if value and block.tag==W+'p':unmapped.append((ci,value))
            continue
        new_source=source
        if block.tag==W+'tbl':
            rows=[]
            for row in block.findall(W+'tr'):
                if row.find(W+'trPr/'+W+'del') is not None:continue
                cells=[keys(text(cell,math_markup=True).strip()).replace('|',r'\|').replace('\n','<br>') for cell in row.findall(W+'tc') if cell.find(W+'tcPr/'+W+'cellDel') is None]
                rows.append(cells)
            assert rows and len({len(r) for r in rows})==1
            new_source='\n'.join('| '+' | '.join(r)+' |' for r in rows[:1]+[[':---']*len(rows[0])]+rows[1:])
            table_exports.append((len(table_exports)+1,new_source,rows))
        elif source.startswith('!['):
            assert block.find('.//'+W+'drawing') is not None
        elif source.startswith('$$'):
            if '{#eq-moc}' in source:
                # Word directly changed the exponent length glyph from ell to l.
                current_math=''.join(block.xpath('.//m:t/text()',namespaces=NS))
                if 'Σtl' in current_math:new_source=source.replace(r'\ell','l')
        elif norm(text(baseline[bi]))!=norm(text(block)):
            if not value:new_source=''
            else:
                prefix=re.match(r'^(#{1,3} |%% \S+ )',source)
                new_source=(prefix.group() if prefix else '')+keys(text(block,math_markup=True).strip())
        if new_source!=source or norm(text(baseline[bi]))!=norm(text(block)):
            changes.append({'baseline_block':bi,'review_block':ci,'source_before':source,'source_after':new_source,
                            'word_before':text(baseline[bi]),'word_after':text(block),'chapter':chapter(bi)})
        if new_source:units.append((chapter(bi),new_source,ci,bi))
    assert not unmapped,unmapped
    assert len(table_exports)==6
    projection_mismatches=[]
    for ch,s,ci,bi in units:
        if s.startswith(('$$','![','|')):continue
        if source_plain(s)!=norm(normalized_references(text(current[ci]))):
            projection_mismatches.append({'block':ci,'source':s,'word':text(current[ci])})
    assert not projection_mismatches,projection_mismatches
    # Missing baseline blocks (front matter and fig1 note) are explicit deletions.
    for bi in deleted_baseline:
        if bi in src_map:changes.append({'baseline_block':bi,'review_block':None,'source_before':src_map[bi],'source_after':'','word_before':text(baseline[bi]),'word_after':'','chapter':chapter(bi),'untracked_deletion':True})
    dump(archive/'source_sync_changes.json',changes)
    front=chunks[0]+'\n\n'+'\n\n'.join(s for ch,s,_,_ in units if ch==0)+'\n\n{{< pagebreak >}}\n\n{{< toc 2 >}}\n\n{{< pagebreak >}}\n'
    chapters={i:'\n\n'.join(s for ch,s,_,_ in units if ch==i)+'\n' for i in range(1,7)}
    manuscript=front+'\n\n'+'\n\n'.join(chapters.values())+'\n\n# 参考文献\n'
    references=[]
    for ci,block in enumerate(current):
        if mapping.get(ci,-1)>ref_start and text(block).strip():references.append(text(block).strip())
    assert len(references)==47
    dump(archive/'source_projection_blocks.json',[{'chapter':ch,'review_block':ci,'baseline_block':bi,'markdown':s,'word_retained_text':text(current[ci]).strip()} for ch,s,ci,bi in units])
    counts={'comments':len(comments),'revision_markers':len(revisions),'revision_types':dict(Counter(r['type'] for r in revisions)),
            'untracked_or_structural_diff_groups':len(direct),'synchronized_source_blocks':len(changes),'tables':len(table_exports),
            'review_docx_sha256':digest,'baseline_commit':BASELINE,'word_unchanged':DOC.read_bytes()==data,
            'source_policy':'删除不进入现行生成源；插入进入源；全部批注保留待处理；不生成Word',
            'regeneration_approved':False}
    dump(archive/'verification.json',counts)
    lines=['# Word删改与批注完整提取核对','',f'原件SHA256：`{digest}`。原件及原始OOXML只归档，不接受或拒绝修订。','',
           f'共{len(comments)}条批注、{len(revisions)}个修订标记；另记录{len(direct)}组未跟踪或结构差异。修订元素数量不等于独立修改次数。','',
           '## 全部批注（保留待处理）','']
    for c in comments:
        lines.extend([f"### 批注 {c['id']} · 原文块 {c['start_block']}—{c['end_block']}",'',c['text'],'',
                      '**修订后所在段落/范围：**','',c['context_after'] or '（该范围文字已删除；修订前上下文完整保存在comments.json）',''])
    lines+=['## 全部插入与删除记录','']
    for r in revisions:
        if r['type'] in {'ins','del','moveFrom','moveTo'}:
            lines += [f"- `{r['type']}` id={r['id']}，原文块={r['body_block']}，{r['author']}，{r['date']}：{r['text_all'] or '（段落标记、行标记或空文本；详见原始XML）'}"]
    lines+=['','全部格式修订的属性、原始XML、作者、时间及上下文见`revisions.json`；未跟踪改动见`untracked_and_structural_differences.json`。完整源段落前后对照见`source_sync_changes.json`。','',
            '删除内容只保存在此审计归档和Git历史，不作为现行生成输入。批注要求的补充调研、合节、改写和流程图尚未执行。未经用户确认禁止重新生成Word。','']
    (archive/'删改与批注核对.md').write_text('\n'.join(line.rstrip() for line in lines))
    if args.apply:
        (B/'frontmatter.md').write_text(front)
        for i,s in chapters.items():(B/f'sources_ch{i:02d}.md').write_text(s)
        (B/'outputs/manuscript.md').write_text(manuscript)
        readable=re.sub(r'^---\n.*?\n---\n','',manuscript,flags=re.S)
        readable=re.sub(r'^\{\{<.*?>\}\}\s*','',readable,flags=re.M)
        readable=re.sub(r'^%%\s+\S+\s*','',readable,flags=re.M)
        def numeric(m):return '['+','.join(str(order[k]) for k in re.findall(r'@(r\d+)',m.group()))+']'
        readable=re.sub(r'\[@r\d+(?:;\s*@r\d+)*\]',numeric,readable)
        readable=re.sub(r'@(eq-[a-zA-Z]+)',lambda m:'式（%d）'%eq_numbers[m.group(1)],readable)
        (B/'outputs/博士研究设想_完整正文.md').write_text(readable.rstrip()+'\n\n'+'\n\n'.join(references)+'\n')
        (B/'bibliography/review_reference_list.md').write_text('\n\n'.join(references)+'\n')
        table_parts=[]
        for n,s,rows in table_exports:
            table_parts.append('{{TABLE%02d}}\n%s'%(n,s))
            (B/f'tables/table{n:02d}.md').write_text(s+'\n')
            with (B/f'tables/table{n:02d}.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f,lineterminator='\n').writerows(rows)
        (B/'table_sources.md').write_text('<!-- 派生快照；现行正文中的表格以sources_ch01—06.md为准。 -->\n\n'+'\n\n'.join(table_parts)+'\n')
        state={'schema_version':1,'review_docx_sha256':digest,'review_archive':str(archive.relative_to(B)),
               'baseline_commit':BASELINE,'regeneration_approved':False,'regeneration_policy':'须先获用户明确确认；禁止恢复已删除内容',
               'source_sha256':{str(p.relative_to(B)):sha(p.read_bytes()) for p in [B/'frontmatter.md']+[B/f'sources_ch{i:02d}.md' for i in range(1,7)]}}
        dump(B/'review_state.json',state)
    assert DOC.read_bytes()==data,'Review Word changed during read-only synchronization'
    print(json.dumps(counts,ensure_ascii=False,indent=2))
    print('Source synchronization applied.' if args.apply else 'Preflight only; no generating sources changed.')

if __name__=='__main__':main()
