from dataclasses import dataclass

from vending_analytics.domain.payment import CardPayment


@dataclass  # STUDYME okruh 12
class Transaction:  # STUDYME okruh 1
    transaction_id: str
    machine_id: str
    timestamp: str
    product_id: str
    product_name: str
    price: int
    payment: CardPayment

    @classmethod  # STUDYME okruh 1
    def from_dict(cls, data: dict) -> "Transaction":  # STUDYME okruh 28
        return cls(
            transaction_id=data["transaction_id"],
            machine_id=data["machine_id"],
            timestamp=data["timestamp"],
            product_id=data["product_id"],
            product_name=data["product_name"],
            price=data["price"],
            payment=CardPayment.from_dict(data),  # STUDYME okruh 2, 28
        )

    def to_dict(self) -> dict:  # STUDYME okruh 1, 28
        return {
            "transaction_id": self.transaction_id,
            "machine_id": self.machine_id,
            "timestamp": self.timestamp,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "payment_status": self.payment.status,
            "card_provider": self.payment.provider,
        }
