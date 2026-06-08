import argparse
from pathlib import Path

from vending_analytics.analytics.charts import save_product_revenue_chart  # STUDYME okruh 18
from vending_analytics.application.report_strategies import (
    ProductReportStrategy,
    SalesSummaryStrategy,
)
from vending_analytics.infrastructure.json_loader import load_transactions  # STUDYME okruh 19


def main() -> None:  # STUDYME okruh 26, 27
    parser = argparse.ArgumentParser(description="Vending sales analytics")  # STUDYME okruh 26
    parser.add_argument("file", type=Path, help="cesta k JSON souboru")  # STUDYME okruh 26
    parser.add_argument(
        "--report",
        choices=["summary", "products"],
        default="summary",
    )  # STUDYME okruh 26
    args = parser.parse_args()  # STUDYME okruh 26

    transactions = load_transactions(args.file)

    strategies = {  # STUDYME okruh 11
        "summary": SalesSummaryStrategy(),
        "products": ProductReportStrategy(),
    }
    result = strategies[args.report].generate(transactions)  # STUDYME okruh 5, 6

    print(f"načteno {len(transactions)} transakcí")

    if args.report == "products":
        print(result.to_string(index=False))  # STUDYME okruh 17
        save_product_revenue_chart(result, Path("product_revenue.png"))  # STUDYME okruh 18
        print("graf uložen: product_revenue.png")
    else:
        print(result)


if __name__ == "__main__":  # STUDYME okruh 19
    main()
