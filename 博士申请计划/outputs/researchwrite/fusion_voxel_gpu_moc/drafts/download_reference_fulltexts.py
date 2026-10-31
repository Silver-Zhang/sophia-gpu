from pathlib import Path
import urllib.request,urllib.parse,ssl,json,re,hashlib,concurrent.futures,shutil,time
from io import BytesIO
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'参考文献全文'
OUT.mkdir(exist_ok=True)
REFS=json.loads((ROOT/'sources/参考文献核验与编号记录.json').read_text())['references']
CTX=ssl.create_default_context(cafile='/etc/ssl/cert.pem')
SPECS={
1:('01_Moreno_2024_ParaStell_期刊版.pdf','https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1384788/pdf','期刊正式版'),
2:('02_Liew_Ku_1991_CIT_Shielding_期刊版.pdf','https://www.ans.org/pubs/journals/download/article-29687/','期刊正式版'),
3:('03_Tsige-Tamirat_2007_McCad_ITER_期刊版.pdf','https://www.sciencedirect.com/science/article/pii/S0920379607003407/pdfft?isDTMRedir=true&download=true','期刊正式版'),
4:('04_Zhou_2025_GPU_MOC_arXiv预印本.pdf','local:multi_gpu2025.pdf','arXiv预印本'),
5:('05_Kim_2026_NuDEAL_作者稿.pdf','local:nudeal2026.pdf','作者原始稿；正式发表DOI见清单'),
6:('06_Amanatides_Woo_1987_Fast_Voxel_Traversal_作者公开版.pdf','https://www.cs.yorku.ca/~amana/research/grid.pdf','作者主页公开版'),
7:('07_Zhang_2021_AMReX_公开排版稿.pdf','https://arxiv.org/pdf/2009.12009','arXiv公开稿，按文件首页核验版本'),
8:('08_Gaston_2021_MOC_Unstructured_Mesh_期刊版.pdf','https://www.tandfonline.com/doi/pdf/10.1080/00295450.2021.1871995','期刊正式版'),
9:('09_Boyd_2014_OpenMOC_作者接受稿.pdf','local:openmoc2014.pdf','MIT机构仓储作者接受稿'),
10:('10_NVIDIA_2026_CUDA_Best_Practices_Guide.pdf','https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf','官方技术指南'),
11:('11_Adinets_2014_Warp_Aggregated_Atomics_官方全文.html','https://developer.nvidia.com/blog/cuda-pro-tip-optimized-filtering-warp-aggregated-atomics/','官方博客HTML全文'),
12:('12_Baker_2013_Goal_Based_Mesh_Adaptivity_期刊版.pdf','https://www.sciencedirect.com/science/article/pii/S0306454912004744/pdfft?isDTMRedir=true&download=true','期刊正式版'),
13:('13_Wagner_2014_FW-CADIS_期刊版.pdf','https://web.ornl.gov/~peplowde/p068.pdf','作者机构公开期刊版')}

def retrieve(n):
    ref=REFS[n-1];name,url,version=SPECS[n];p=OUT/name
    result={'number':n,'title':ref['title'],'doi':ref.get('doi'),'file':None,'source':url,'version':version,'si_requested':True,'si_status':'待逐项核对','status':'pending','attempts':[]}
    try:
        if url.startswith('local:'):data=(ROOT/'sources'/url[6:]).read_bytes();actual=url
        else:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (academic reference retrieval)','Accept':'application/pdf,text/html;q=0.9,*/*;q=0.5'})
            with urllib.request.urlopen(req,timeout=35,context=CTX) as response:data=response.read(80*1024*1024);actual=response.url
        result['attempts'].append({'url':url,'resolved_url':actual,'bytes':len(data)})
        if name.endswith('.pdf'):
            if not data.startswith(b'%PDF-'):raise ValueError('Response is not PDF; not saved as paper')
            reader=PdfReader(BytesIO(data));text=' '.join((p.extract_text() or '') for p in reader.pages[:3]);norm=lambda s:''.join(re.findall(r'[a-z0-9]+',s.lower()))
            expected=norm(ref['title']);hay=norm(text)
            # Publisher cover pages and typographic hyphens can alter whitespace only.
            if expected not in hay:raise ValueError('PDF title mismatch; requires manual verification')
            result.update({'pages':len(reader.pages),'first_page':(reader.pages[0].extract_text() or '')[:1400]})
        else:
            text=data.decode('utf-8','replace')
            if ref['title'].lower() not in text.lower() or len(text)<15000:raise ValueError('Not a verified full-text HTML page')
        p.write_bytes(data);result.update({'file':name,'status':'open_access_downloaded' if not url.startswith('local:') else 'verified_local_fulltext_copied','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    except Exception as e:result['status']='download_failed';result['error']=str(e)
    print(json.dumps({k:result.get(k) for k in ['number','status','pages','bytes','error']},ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(retrieve,range(1,14)))
    (ROOT/'qa_logs/下载首轮核验.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
