#!/usr/bin/env python3
"""Join identity metadata, source-limited core evidence and manuscript claim contexts.
A manuscript context is not evidence of an independently verified paper result.
"""
from pathlib import Path
import json,re,csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'main.tex').read_text();body=s.split('\\begin{thebibliography}',1)[0]
meta={x['key']:x for x in json.loads((ROOT/'references/metadata_crossref.json').read_text())}
if (ROOT/'references/metadata_new_geometry.json').exists():
    meta.update({x['key']:x for x in json.loads((ROOT/'references/metadata_new_geometry.json').read_text())})
data={x['key']:x for x in json.loads((ROOT/'references/metadata_datacite.json').read_text())}
gpu={f"ref{re.match(r'\d+',x['identity'])[0]}":x for x in json.loads((ROOT/'references/gpu_evidence.json').read_text())['records']}
geo={}
for line in (ROOT/'references/geometry_evidence.md').read_text().splitlines():
    cells=line.strip('|').split('|')
    if re.match(r'^\d+\s',cells[0]): geo['ref'+re.match(r'^\d+',cells[0])[0]]=cells
app={}
for line in (ROOT/'references/application_evidence.md').read_text().splitlines():
    cells=line.strip('|').split('|')
    if re.match(r'^ref\d+\s',cells[0]): app[re.match(r'^ref\d+',cells[0])[0]]=cells
contexts={}
for block in re.split(r'\n\s*\n',body):
    nums=set()
    for c in re.findall(r'\\upcite\{([^}]+)\}',block):
        for t in c.split(','):
            rr=re.fullmatch(r'(\d+)--(\d+)',t)
            if rr:nums.update(range(int(rr[1]),int(rr[2])+1))
            elif t.isdigit():nums.add(int(t))
    for n in nums:contexts.setdefault(f'ref{n}',[]).append({'latex_context':block.strip(),'evidence_status':'manuscript_claim_context_only'})
unknown='本轮未独立取得；正文沿用内容不得视为已完成原文核验'
records=[]
for key,entry in re.findall(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})',s,re.S):
    m=meta.get(key,{});d=data.get(key,{})
    doi=(m.get('doi') or (re.search(r'(10\.\d{4,9}/[A-Za-z0-9._;()/:%+\-]+)',entry).group(1).rstrip('.') if re.search(r'(10\.\d{4,9}/[A-Za-z0-9._;()/:%+\-]+)',entry) else None))
    ident={'reference_key':key,'manuscript_entry':entry.strip(),'doi':doi,'authors_metadata':m.get('authors') or d.get('creators'),'full_title_metadata':m.get('title') or d.get('titles'),'published_metadata':m.get('published') or d.get('publication_year'),'published_online':m.get('published_online'),'published_print':m.get('published_print'),'identity_verification_status':m.get('status') or 'new_entry_not_crossref_retrieved','datacite_status':d.get('status'),'identity_source':m.get('source'),'datacite_source':d.get('source')}
    out={'identity':ident,'provenance':'V4.2保留条目' if int(key[3:])<=67 else 'V5新增条目','manuscript_contexts':contexts.get(key,[]),'problem_geometry_material_source_type':unknown,'numerical_method':unknown,'algorithm_tracks_index_cache_parallel':unknown,'conditions_mesh_groups_tracks_hardware_tolerance':unknown,'results_error_time_memory_scaling':unknown,'comparison_baseline':unknown,'research_implication':unknown,'evidence_location_page_figure_table_section':unknown,'fulltext_verification_status':'not_independently_verified_this_round','field_split_note':'核心证据字段保留专项矩阵原始措辞，某些字段为合并记录；未报告的子字段均未知。元数据成功与全文核验严格分开。','core_evidence_sources':[]}
    if key in geo:
        c=geo[key];out.update(problem_geometry_material_source_type=c[1],numerical_method=c[1],algorithm_tracks_index_cache_parallel=c[2],conditions_mesh_groups_tracks_hardware_tolerance=c[3],results_error_time_memory_scaling=c[3],comparison_baseline=c[3],research_implication=c[5],evidence_location_page_figure_table_section=c[4],fulltext_verification_status='source_limited_see_explicit_access_statement');out['core_evidence_sources'].append('references/geometry_evidence.md row '+key[3:])
    if key in gpu:
        g=gpu[key];out.update(problem_geometry_material_source_type=g['object_method'],numerical_method=g['object_method'],algorithm_tracks_index_cache_parallel=g['algorithm'],conditions_mesh_groups_tracks_hardware_tolerance=g['conditions_results'],results_error_time_memory_scaling=g['conditions_results'],comparison_baseline=g['baseline_evidence_location'],research_implication=g['interpretation_access'],evidence_location_page_figure_table_section=g['baseline_evidence_location'],fulltext_verification_status='source_limited_see_explicit_access_statement');out['core_evidence_sources'].append('references/gpu_evidence.json record '+key[3:])
    if key in app:
        c=app[key];out.update(problem_geometry_material_source_type=c[1],numerical_method=c[1],algorithm_tracks_index_cache_parallel=c[1],conditions_mesh_groups_tracks_hardware_tolerance=c[1],results_error_time_memory_scaling=c[2],comparison_baseline=c[2],research_implication=c[4],evidence_location_page_figure_table_section=c[3],fulltext_verification_status='source_limited_see_explicit_access_statement');out['core_evidence_sources'].append('references/application_evidence.md row '+key)
    records.append(out)
report={'source_sha256':hashlib.sha256(s.encode()).hexdigest(),'checked_date':'2026-11-08','scope':'69条目合并矩阵；身份元数据、原稿论断和本轮原文/摘要证据分列，缺口明确可见','records':records}
(ROOT/'references/evidence_matrix.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
fields=['key','provenance','doi','full_title','authors','identity_status','manuscript_contexts','problem_geometry_material_source_type','numerical_method','algorithm_tracks_index_cache_parallel','conditions_mesh_groups_tracks_hardware_tolerance','results_error_time_memory_scaling','comparison_baseline','research_implication','evidence_location_page_figure_table_section','fulltext_verification_status','core_evidence_sources']
with (ROOT/'references/evidence_matrix.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in records:
        i=r['identity'];row={k:r[k] for k in fields if k in r};row.update(key=i['reference_key'],doi=i['doi'],full_title=json.dumps(i['full_title_metadata'],ensure_ascii=False),authors=json.dumps(i['authors_metadata'],ensure_ascii=False),identity_status=i['identity_verification_status']+'; '+str(i['datacite_status']),manuscript_contexts=json.dumps(r['manuscript_contexts'],ensure_ascii=False),core_evidence_sources='; '.join(r['core_evidence_sources']));w.writerow(row)
print(f'{len(records)} records; {sum(bool(r["core_evidence_sources"]) for r in records)} source-limited core records; {sum(not r["core_evidence_sources"] for r in records)} explicit fulltext gaps')
