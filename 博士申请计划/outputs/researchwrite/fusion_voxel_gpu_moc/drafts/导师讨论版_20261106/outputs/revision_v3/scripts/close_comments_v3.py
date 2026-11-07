"""Keep V2 dispositions as history, record only the V3 targeted followups."""
from pathlib import Path
import json,csv
V=Path(__file__).resolve().parents[1]
from safety_v3 import require_v3_root
require_v3_root(V)
rows=json.loads((V/'planning/V2批注处理台账.json').read_text())
for r in rows:
 r['v2_status']=r.pop('status')
 r['v3_status']='保留V2结果，未扩大本轮修订范围'
 r['v3_action']='本轮标题/正文差异及人工删改保护检查确认未反向恢复内容。'
 if r['id']=='164':
  r['v3_status']='限定证据补查完成；正式硬件缺项保留'
  r['v3_action']='新查出版社TDM、OpenAlex、作者单位及作者学位论文。ANT-MOC设备类别确认东方/16000 DCU；Song/ANT/STREAM正式GPU商品型号与CPU表仍未获取。新获STREAM学位全文的256核/8.61与15.44倍不与正式版128核/22.1与40.5倍拼接。见bibliography/v3_hardware_followup.*；3.1及表2只补可核DCU类别。'
 if r['id']=='175':
  r['v3_status']='限定证据补查完成；多群深穿透GPU伴随性能缺项保留'
  r['v3_action']='3.2增加Pryer2026预印本的GPU固定源DG/反向微分及独立转置系统一致性检验，以及Shift2025的CPU确定论预计算/GPU蒙卡分工。保留OpenSn静态路径与实测层级的区别；没有把批处理或MC倍率写成GPU伴随加速。见bibliography/v3_gpu_adjoint_followup.*。'
with (V/'qa/批注状态.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(V/'qa/批注状态.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
md=['# V3批注状态','', '原38条逐项原文及V2处理保留于JSON/CSV；V3不重判其他36条的历史状态。本轮对164与175完成可获得证据范围内的限定核查，缺失字段不以推断填补。','']
for r in rows:
 md.extend([f"## {r['id']}：{r['v3_status']}",'',r['v3_action'],''])
(V/'qa/批注状态.md').write_text('\n'.join(md).rstrip()+'\n')
print('Recorded 38 historical dispositions and 2 targeted V3 followups, with evidence gaps explicit.')
