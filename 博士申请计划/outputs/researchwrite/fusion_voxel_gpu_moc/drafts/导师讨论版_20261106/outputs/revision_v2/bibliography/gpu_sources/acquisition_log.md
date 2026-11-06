# GPU来源获取记录

2026-11-06；全部来源用于本地核查。PDF、HTML/XML、抽取文本及页面图片均由本目录.gitignore排除，不提交版权全文。可提交内容仅本获取记录、JSON事实归纳和元数据、Markdown证据分析。

| 来源 | 路径/URL | 获取结果与核查范围 |
|---|---|---|
| OpenMOC作者接受稿 | 项目既有 ../../参考文献全文/09_Boyd_2014_OpenMOC_作者接受稿.pdf | 已读§3.4.3/§5.3；渲染p.11实看Fig.11型号，缓存openmoc-11.png |
| NuDEAL作者稿 | 项目既有 ../../sources/nudeal2026.txt 与参考文献全文/05_Kim_2026_NuDEAL_作者稿.pdf | 已核方法§III及TablesII—VI与脚注 |
| 宋佩涛2019 r20 | https://yznkxjs.xml-journal.net/cn/article/pdf/preview/10.7538/yzk.2019.youxian.0416.pdf | HTTP200 PDF，song2019.pdf/txt；渲染5/6页核图3、表1与型号 |
| 宋佩涛2020另一篇 | https://yznkxjs.xml-journal.net/cn/article/pdf/preview/10.7538/yzk.2019.youxian.0094.pdf | HTTP200 PDF，song2020.pdf/txt；渲染p.5核表3，区分GTX1080Ti/i9-7900X实验 |
| STREAM2024 KNS先行稿 | https://www.kns.org/files/pre_paper/51/24S-051-Siarhei.pdf | HTTP200，stream2024.pdf/txt，3页全文，明确64核/8A5000与八分之一堆芯 |
| STREAM2025 KNS改版 | https://www.kns.org/files/pre_paper/53/25S-240-Siarhei.pdf | HTTP200，kns_stream.pdf/txt，GPU-CMFD与节点配置；不等同2026期刊 |
| Song2026正式记录 | https://www.sciencedirect.com/science/article/pii/S0149197025005074 | web索引可读摘要、引言和片段；直接请求403；API返回元数据XML、openaccess=false，无正文；ResearchGate无全文，OpenAlex无公开稿 |
| STREAM2026正式记录 | https://www.sciencedirect.com/science/article/pii/S0010465525004539 | 可读摘要及片段；API仅元数据XML、无正文；型号未核 |
| ANT-MOC SC23 | https://sc23.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap300.html | 官方原始摘要可读；ACM pdf/am-pdf/epdf HTTP403；SC23猜测PDF地址404，不作证据；OpenAlex OA标志与实际可得性不同 |
| Zhou预印本 | 项目既有 ../../sources/multi_gpu2025.pdf；https://arxiv.org/abs/2503.17743 | 提取zhou_preprint.txt，读pp.6—9，只用于轨迹机制 |
| STRAUM正式全文 | https://www.researchgate.net/publication/390357834_GPU-based_multi-group_discrete_ordinates_transport_calculations_Parallel_computing_implementation_in_STRAUM | 作者Ao Zhang公开上传的正式全文HTML可读，核§3.2/3.3/Table1—6/§4.2；PDF链接404、Elsevier PDF/API无正文；不是只读二手摘要 |
| Denovo JET作者稿 | https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPJET3PR1619576_accepted_merged.pdf | HTTP200，denovo_fusion.pdf/txt；26个PDF页含封面，核方法与PDF16页TableIV及PDF18页结论，记录工况冲突 |
| Gong2011 | https://www.sciencedirect.com/science/article/pii/S0021999111002348 | 正式摘要可核M2050/X5670/Q6600及fixup；未得全文 |
| Zou2022 | https://www.sciencedirect.com/science/article/pii/S0306454922002067 | 正式摘要/§3/结论片段可核RTX2080Ti与TFSP；未得全文 |
| 新文献元数据 | api.crossref.org/works/{DOI} | STRAUM/Denovo/Gong的正式作者、卷期页与DOI交叉核对；Denovo不同仓储作者列表差异留JSON |

未使用Sci-Hub或绕过付费/登录限制；未向作者发送索取全文消息。未使用后续论文设备代替目标文章原始设备。
