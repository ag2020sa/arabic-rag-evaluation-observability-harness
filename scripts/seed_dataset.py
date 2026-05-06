from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rag_eval_harness.datasets.synthetic import build_prompt_injection_cases
from rag_eval_harness.datasets.loader import write_jsonl


def main() -> None:
    write_jsonl("data/golden/synthetic_security_cases.jsonl", [x.model_dump() for x in build_prompt_injection_cases()])
    print("Wrote data/golden/synthetic_security_cases.jsonl")


if __name__ == "__main__":
    main()
