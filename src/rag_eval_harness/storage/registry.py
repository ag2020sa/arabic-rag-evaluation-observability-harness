from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict


def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def artifact_metadata(path: str | Path) -> Dict[str, str | int]:
    p = Path(path)
    return {"path": str(p), "sha256": file_sha256(p), "bytes": p.stat().st_size}
