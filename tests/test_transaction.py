import unittest

from vending_analytics.domain.transaction import Transaction


class TestTransaction(unittest.TestCase):
    def test_from_dict_creates_transaction(self) -> None:  # STUDYME okruh 23
        data = {
            "transaction_id": "TX-20260604-0001",
            "machine_id": "VM-001",
            "timestamp": "2026-06-04T07:12:10",
            "product_id": "P-101",
            "product_name": "Coca-Cola 0.5L",
            "price": 35,
            "payment_status": "paid",
            "card_provider": "Visa",
        }

        tx = Transaction.from_dict(data)  # STUDYME okruh 28

        self.assertEqual(tx.transaction_id, "TX-20260604-0001")
        self.assertEqual(tx.machine_id, "VM-001")
        self.assertEqual(tx.timestamp, "2026-06-04T07:12:10")
        self.assertEqual(tx.product_id, "P-101")
        self.assertEqual(tx.product_name, "Coca-Cola 0.5L")
        self.assertEqual(tx.price, 35)
        self.assertTrue(tx.payment.is_paid())
        self.assertEqual(tx.payment.provider, "Visa")
