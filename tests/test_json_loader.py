import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from vending_analytics.infrastructure.json_loader import load_transactions


class TestJsonLoader(unittest.TestCase):  # STUDYME okruh 23
    @patch("vending_analytics.infrastructure.json_loader.json.load")  # STUDYME okruh 24
    def test_load_transactions_without_real_file(self, mock_json_load) -> None:  # STUDYME okruh 24
        mock_json_load.return_value = [
            {
                "transaction_id": "TX-001",
                "machine_id": "VM-001",
                "timestamp": "2026-06-04T07:12:10",
                "product_id": "P-101",
                "product_name": "Coca-Cola 0.5L",
                "price": 35,
                "payment_status": "paid",
                "card_provider": "Visa",
            }
        ]

        mock_file = MagicMock()  # STUDYME okruh 24
        mock_path = MagicMock(spec=Path)  # STUDYME okruh 24
        mock_path.open.return_value.__enter__.return_value = mock_file

        result = load_transactions(mock_path)

        self.assertEqual(len(result), 1)  # STUDYME okruh 23
        self.assertEqual(result[0].transaction_id, "TX-001")
        mock_json_load.assert_called_once_with(mock_file)  # STUDYME okruh 24
