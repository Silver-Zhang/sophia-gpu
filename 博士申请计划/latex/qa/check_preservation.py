#!/usr/bin/env python3
"""Compare V5 protected equation/table source blocks to the immutable V4.2 snapshot."""
from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[1]
s=(root/'main.tex').read_text()
b=json.loads((root/'references/baseline_inventory.json').read_text())
out={'baseline_commit':b['baseline_commit'],'checked_source_sha256':hashlib.sha256(s.encode()).hexdigest(),'equations':[],'tables':[]}
for key,env in [('equations','equation'),('tables','longtable')]:
    current={lab:(m.group(),s.count('\n',0,m.start())+1) for m in re.finditer(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}',s,re.S) for lab in re.findall(r'\\label\{([^}]+)\}',m.group())}
    for old in b['equation_sources' if env=='equation' else 'table_sources']:
        lab=old['labels'][0];a=current.get(lab);record={'label':lab,'exists':a is not None,'baseline_line':old['baseline_line']}
        if a:
            record.update(current_line=a[1],source_unchanged=a[0]==old['source'])
            if env=='longtable':
                # Width definitions may change to fix layout; compare rows and narrative too.
                normalize=lambda text: re.sub(r'\\(?:allowbreak|newline)', '', re.sub(r'\\begin\{longtable\}[^\n]*', '', text)).strip()
                record['content_unchanged_ignoring_column_definition']=normalize(a[0])==normalize(old['source'])
                record['content_unchanged_ignoring_columns_and_whitespace']=re.sub(r'\s+','',normalize(a[0]))==re.sub(r'\s+','',normalize(old['source']))
        out[key].append(record)
(root/'qa/source_preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
