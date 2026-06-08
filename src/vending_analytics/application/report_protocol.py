from typing import Protocol

from vending_analytics.domain.transaction import Transaction


class ReportStrategy(Protocol):  # STUDYME okruh 6
    def generate(self, transactions: list[Transaction]) -> object: ...  # STUDYME okruh 5
