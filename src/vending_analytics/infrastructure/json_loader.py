import json
from collections.abc import Iterator
from pathlib import Path

from vending_analytics.domain.transaction import Transaction  # STUDYME okruh 19


def iter_transactions(path: Path) -> Iterator[Transaction]:  # STUDYME okruh 7, 21
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)  # STUDYME okruh 28
    for item in raw:  # STUDYME okruh 20
        yield Transaction.from_dict(item)  # STUDYME okruh 21


def load_transactions(path: Path) -> list[Transaction]:  # STUDYME okruh 27
    return list(iter_transactions(path))  # STUDYME okruh 21
