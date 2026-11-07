"""Reject any authoring root that resolves into V2 or outside the V3 tree."""
from pathlib import Path

def require_v3_root(root):
 root=Path(root).resolve()
 assert 'revision_v2' not in root.parts,root
 assert root.name=='revision_v3' or any(p.name=='revision_v3' and root.is_relative_to(p/'qa/rebuild_sandbox') for p in root.parents),root
 return root
