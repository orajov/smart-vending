import unittest

from vending_analytics.application.sales_report import build_sales_summary
from vending_analytics.domain.transaction import Transaction


class TestSalesReport(unittest.TestCase):  # STUDYME okruh 23
    def test_build_sales_summary(self) -> None:  # STUDYME okruh 23
        transactions = [
            Transaction.from_dict(
                {  # STUDYME okruh 28
                    "transaction_id": "TX-001",
                    "machine_id": "VM-001",
                    "timestamp": "2026-06-04T07:12:10",
                    "product_id": "P-101",
                    "product_name": "Coca-Cola 0.5L",
                    "price": 35,
                    "payment_status": "paid",
                    "card_provider": "Visa",
                }
            ),
            Transaction.from_dict(
                {
                    "transaction_id": "TX-002",
                    "machine_id": "VM-001",
                    "timestamp": "2026-06-04T08:12:10",
                    "product_id": "P-102",
                    "product_name": "Pepsi 0.5L",
                    "price": 34,
                    "payment_status": "failed",
                    "card_provider": "Mastercard",
                }
            ),
        ]

        summary = build_sales_summary(transactions)  # STUDYME okruh 27

        self.assertEqual(summary["transaction_count"], 2)
        self.assertEqual(summary["paid_count"], 1)
        self.assertEqual(summary["failed_count"], 1)
        self.assertEqual(summary["total_revenue"], 35)
