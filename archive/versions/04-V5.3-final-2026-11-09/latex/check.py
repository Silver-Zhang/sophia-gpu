#!/usr/bin/env python3
"""Check numeric citations and LaTeX references without requiring TeX packages."""
from pathlib import Path
import argparse,collections,json,re,sys
ap=argparse.ArgumentParser();ap.add_argument('--log',type=Path);ap.add_argument('--source',type=Path);args=ap.parse_args()
root=Path(__file__).resolve().parent;path=args.source or root/'main.tex'; raw=path.read_text();s=re.sub(r'(?m)(?<!\\)%.*$','',raw)
errors=[];warnings=[]
bibs=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',s)
for kind,vals in [('bibitem',bibs),('label',re.findall(r'\\label\{([^}]+)\}',s))]:
    errors += [f'duplicate {kind}: {k}' for k,n in collections.Counter(vals).items() if n>1]
keys=set(bibs);used=set(); labels=set(re.findall(r'\\label\{([^}]+)\}',s))
for citation in re.findall(r'\\upcite\{([^}]+)\}',s):
    if re.fullmatch(r'#\d',citation): continue
    if re.search(r'\d{4}-\d{2}-\d{2}',citation): errors.append('access date misused as citation: '+citation);continue
    for token in re.split(r'[,，]',citation):
        token=token.strip(); m=re.fullmatch(r'(\d+)\s*(?:--|–|—|-)\s*(\d+)',token)
        if m:
            lo,hi=map(int,m.groups())
            if lo>hi: errors.append('reversed citation range: '+token)
            used.update('ref'+str(n) for n in range(lo,hi+1))
        elif token.isdigit(): used.add('ref'+token)
        else: errors.append('invalid numeric citation: '+token)
for citation in re.findall(r'\\(?:cite|citep|citet)\{([^}]+)\}',s): used.update(citation.split(','))
errors += ['missing bibliography entry: '+k for k in sorted(used-keys)]
refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',s));errors += ['missing label: '+k for k in sorted(refs-labels)]
warnings += ['uncited bibliography entry: '+k for k in sorted(keys-used)]
baseline=json.loads((root/'references/baseline_inventory.json').read_text())
errors += ['baseline bibliography entry removed: '+x['key'] for x in baseline['bibliography'] if x['key'] not in keys]
errors += ['baseline equation label removed: '+x for x in baseline['equations'] if x not in labels]
for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',s):
    errors += [] if any((root/(name+suffix)).is_file() for suffix in ['', '.pdf', '.png']) else ['missing figure: '+name]
# Numbered bibliography follows first citation, including numeric ranges.
first=[]
for citation in re.findall(r'\\upcite\{([^}]+)\}',s.split('\\begin{thebibliography}',1)[0]):
    for token in citation.split(','):
        match=re.fullmatch(r'(\d+)--(\d+)',token)
        values=list(range(int(match[1]),int(match[2])+1)) if match else ([int(token)] if token.isdigit() else [])
        for value in values:
            if value not in first: first.append(value)
if first != list(range(1,len(bibs)+1)): errors.append('bibliography is not numbered by first citation')
if args.log:
    log=args.log.read_text(errors='replace')
    errors += [line for line in log.splitlines() if re.search(r'undefined|There were undefined references|Rerun to get cross-references right|Fatal error|^!',line,re.I)]
    warnings += [line for line in log.splitlines() if re.search(r'Overfull|Missing character',line)]
result={'source':str(path),'bibliography_count':len(bibs),'cited_entries':len(used),'equations':len(re.findall(r'\\begin\{equation\}',s)),'figures':len(re.findall(r'\\includegraphics',s)),'tables':len(re.findall(r'\\begin\{longtable\}',s)),'errors':errors,'warnings':warnings}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(errors or warnings))
