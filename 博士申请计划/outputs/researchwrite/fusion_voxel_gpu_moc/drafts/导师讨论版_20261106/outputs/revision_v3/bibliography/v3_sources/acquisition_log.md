# V3 task164 获取记录

2026-11-07。全文/快照均仅保存在本目录且由局部.gitignore忽略。可提交本日志与上级事实归纳；不提交全文和截图。

- Crossref三篇DOI查询与OpenAlex三篇记录：requests HTTP200。初次urllib因本地证书链失败，已改标准requests重试一次，未禁用证书验证。缓存crossref_*.json/openalex_*.json，仅供本地检查。
- Song/STREAM的Crossref VOR TDM XML链接：HTTP200，但分别1869/1893字节，仅coredata，无正文；不称已取全文。
- ACM ANT-MOC PDF及full HTML：403，Cloudflare验证页；未绕过；OpenAlex OA标签不能替代实际全文。
- SC23官方pap300摘要、CNIC两份2023官方报道：web实际打开；CNIC12月原HTML已缓存。
- UNIST正式journal list与alumni新站：web实际打开；旧/alumni路径可能误跳学校总校友首页，新站准确路径为/reactorcore/alumni.do。
- 作者Doctor Thesis链接指向Drive文件夹1fq2GtTyJnmYrkI6w9AcDS8t5l5LE5rur；公开文件为[PHD_Thesis]_Siarhei_Dzianisau.pdf，file ID1hNlsf8ZFzX-zIOAU5rNnEhGHClHhKK9_。下载HTTP200、6519687字节、首字节%PDF。最终SHA见上级JSON。
- STREAM博士论文PDF25/46/47页已渲染并实际打开，核查硬件表和CPU型号内部矛盾；48/49/63/64页正文提取核查计时。论文不等于2026CPC实验。

精确URL、原文位置、访问等级和未解决项见../v3_hardware_followup.json。
