import unittest

from vending_analytics.domain.payment import CardPayment


class TestPayment(unittest.TestCase):  # STUDYME okruh 23
    def test_card_payment_inherits_is_paid(self) -> None:  # STUDYME okruh 2
        payment = CardPayment(status="paid", provider="Visa")  # STUDYME okruh 2

        self.assertTrue(payment.is_paid())  # STUDYME okruh 23
        self.assertEqual(payment.provider, "Visa")

    def test_from_dict(self) -> None:  # STUDYME okruh 28
        payment = CardPayment.from_dict(
            {
                "payment_status": "failed",
                "card_provider": "Mastercard",
            }
        )

        self.assertFalse(payment.is_paid())
        self.assertEqual(payment.provider, "Mastercard")
