from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

import yaml

from rag_eval_harness.schemas import GoldenExample


def load_jsonl(path: str | Path) -> List[dict]:
    records: List[dict] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return records


def load_golden_examples(path: str | Path) -> List[GoldenExample]:
    return [GoldenExample.model_validate(x) for x in load_jsonl(path)]


def load_yaml(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_jsonl(path: str | Path, records: Iterable[dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
