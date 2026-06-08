from vending_analytics.domain.transaction import Transaction


def build_sales_summary(transactions: list[Transaction]) -> dict:  # STUDYME okruh 27
    paid = [t for t in transactions if t.payment.is_paid()]  # STUDYME okruh 20
    failed = [t for t in transactions if not t.payment.is_paid()]  # STUDYME okruh 20

    return {
        "transaction_count": len(transactions),
        "paid_count": len(paid),
        "failed_count": len(failed),
        "total_revenue": sum(t.price for t in paid),  # STUDYME okruh 21
    }
