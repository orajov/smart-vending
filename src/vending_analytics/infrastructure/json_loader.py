import json
from pathlib import Path

from vending_analytics.domain.transaction import Transaction  # STUDYME okruh 19


def load_transactions(path: Path) -> list[Transaction]:  # STUDYME okruh 27
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)  # STUDYME okruh 28

    return [Transaction.from_dict(item) for item in raw]  # STUDYME okruh 20
