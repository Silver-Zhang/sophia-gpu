"""Enforce the user's explicit hold on Word regeneration and modification."""
from pathlib import Path
import json

B=Path(__file__).resolve().parent

def require_regeneration_approval():
    state_path=B/'review_state.json'
    if state_path.exists():
        state=json.loads(state_path.read_text())
        if not state.get('regeneration_approved',False):
            raise SystemExit('已阻止Word生成/改写：用户要求先核对保留全部删改批注；尚未明确确认重新生成。不得恢复已删除内容。请勿绕过此保护。')

if __name__=='__main__':require_regeneration_approval()
