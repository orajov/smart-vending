from dataclasses import dataclass


@dataclass  # STUDYME okruh 1
class Payment:  # STUDYME okruh 2
    status: str

    def is_paid(self) -> bool:  # STUDYME okruh 1
        return self.status == "paid"


@dataclass  # STUDYME okruh 2
class CardPayment(Payment):  # STUDYME okruh 2
    provider: str

    @classmethod  # STUDYME okruh 1
    def from_dict(cls, data: dict) -> "CardPayment":  # STUDYME okruh 28
        return cls(
            status=data["payment_status"],
            provider=data["card_provider"],
        )
