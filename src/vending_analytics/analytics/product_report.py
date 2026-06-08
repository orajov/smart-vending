import pandas as pd

from vending_analytics.domain.transaction import Transaction


def build_product_report(transactions: list[Transaction]) -> pd.DataFrame:  # STUDYME okruh 17
    rows = [t.to_dict() for t in transactions if t.payment_status == "paid"]  # STUDYME okruh 28
    df = pd.DataFrame(rows)  # STUDYME okruh 17

    return (
        df.groupby("product_name", as_index=False)["price"]
        .sum()
        .rename(columns={"price": "revenue"})
        .sort_values("revenue", ascending=False)
    )  # STUDYME okruh 17
