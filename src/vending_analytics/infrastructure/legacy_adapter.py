import json
from dataclasses import dataclass
from pathlib import Path

from vending_analytics.domain.transaction import Transaction


@dataclass  # STUDYME okruh 10
class LegacyTransactionAdapter:  # STUDYME okruh 10
    def adapt(self, raw: dict) -> dict:  # STUDYME okruh 10
        return {
            "transaction_id": raw["id"],
            "machine_id": raw["machine"],
            "timestamp": raw["time"],
            "product_id": raw["product_code"],
            "product_name": raw["product"],
            "price": int(raw["amount"]),
            "payment_status": raw["status"],
            "card_provider": raw["card"],
        }

    def load(self, path: Path) -> list[Transaction]:  # STUDYME okruh 10
        with path.open(encoding="utf-8") as f:
            raw = json.load(f)

        return [Transaction.from_dict(self.adapt(item)) for item in raw]  # STUDYME okruh 28
