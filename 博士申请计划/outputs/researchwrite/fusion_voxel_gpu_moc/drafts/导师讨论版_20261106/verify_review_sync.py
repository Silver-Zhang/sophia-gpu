"""Read-only independent checks of review preservation and source projection."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from collections import Counter
import hashlib,json,re,subprocess
B=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
state=json.loads((B/'review_state.json').read_text());archive=B/state['review_archive']
word=B/'outputs/博士研究设想_导师讨论初稿.docx';raw=word.read_bytes()
assert sha(raw)==state['review_docx_sha256']
assert raw==(archive/'用户批注修订原件.docx').read_bytes()
with ZipFile(word) as z:
    assert z.testzip() is None
    for n in z.namelist():
        if n.endswith(('.xml','.rels')):assert z.read(n)==(archive/'ooxml'/n).read_bytes(),n
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    comments=E.fromstring(z.read('word/comments.xml'));doc=E.fromstring(z.read('word/document.xml'))
    ids=[n.get(w+'id') for n in comments.iter(w+'comment')]
    assert len(ids)==len(set(ids))==38
    saved_comments=json.loads((archive/'comments.json').read_text())
    assert [(n.get(w+'id'),E.tostring(n,encoding='unicode')) for n in comments.iter(w+'comment')]==[(c['id'],c['xml']) for c in saved_comments]
    for tag in ['commentRangeStart','commentRangeEnd','commentReference']:
        assert sorted(n.get(w+'id') for n in doc.iter(w+tag))==sorted(ids)
    actual=[];actual_xml=[]
    for n in z.namelist():
        if not(n.startswith('word/') and n.endswith('.xml')):continue
        root=E.fromstring(z.read(n))
        for el in root.iter():
            kind=E.QName(el).localname
            if kind in {'ins','del','moveFrom','moveTo','cellIns','cellDel','cellMerge'} or kind.endswith('PrChange'):
                actual.append((n,el.getroottree().getpath(el),kind,el.get(w+'id')))
                actual_xml.append(E.tostring(el,encoding='unicode'))
    records=json.loads((archive/'revisions.json').read_text())
    assert actual==[(r['part'],r['xpath'],r['type'],r['id']) for r in records]
    assert actual_xml==[r['xml'] for r in records]
    assert len(records)==260
units=json.loads((archive/'source_projection_blocks.json').read_text())
for i in range(1,7):
    expected='\n\n'.join(u['markdown'] for u in units if u['chapter']==i)+'\n'
    assert (B/f'sources_ch{i:02d}.md').read_text()==expected,i
for name,digest in state['source_sha256'].items():assert sha((B/name).read_bytes())==digest,name
source=(B/'frontmatter.md').read_text()+'\n\n'+'\n\n'.join((B/f'sources_ch{i:02d}.md').read_text() for i in range(1,7))+'\n\n# 参考文献\n'
assert (B/'outputs/manuscript.md').read_text()==source
assembler=(B/'assemble_manuscript.py').read_text()
for token in ['captions={',"00_确认大纲与现有正文材料.md",'%% 摘要 聚变屏蔽计算']:
    assert token not in assembler,token
assert not state['regeneration_approved']
pdf=B/'outputs/博士研究设想_导师讨论初稿.pdf'
root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=B,text=True).strip())
old_pdf=subprocess.check_output(['git','show',state['baseline_commit']+':'+str(pdf.relative_to(root))],cwd=root)
assert pdf.read_bytes()==old_pdf
report={'status':'passed','comments_with_complete_anchors':len(ids),'all_revision_markers_preserved':len(records),
        'revision_types':dict(Counter(r['type'] for r in records)),
        'word_sha256_unchanged':sha(raw),'pdf_unchanged':True,'all_OOXML_parts_preserved':True,
        'six_chapter_sources_match_retained_Word_projection':True,
        'source_blocks_with_before_after_mapping':len(json.loads((archive/'source_sync_changes.json').read_text())),
        'untracked_or_structural_diff_groups':len(json.loads((archive/'untracked_and_structural_differences.json').read_text())),
        'retained_markdown_headings':len(re.findall(r'^#{1,3} ',source,re.M))-1,
        'regeneration_approved':False,'no_Word_regeneration_performed':True}
print(json.dumps(report,ensure_ascii=False,indent=2))
