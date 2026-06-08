import argparse
from pathlib import Path

from vending_analytics.application.sales_report import build_sales_summary  # STUDYME okruh 27
from vending_analytics.infrastructure.json_loader import load_transactions  # STUDYME okruh 19


def main() -> None:  # STUDYME okruh 26, 27
    parser = argparse.ArgumentParser(description="Vending sales analytics")  # STUDYME okruh 26
    parser.add_argument("file", type=Path, help="cesta k JSON souboru")  # STUDYME okruh 26
    args = parser.parse_args()  # STUDYME okruh 26

    transactions = load_transactions(args.file)
    summary = build_sales_summary(transactions)
    print(f"načteno {len(transactions)} transakcí")
    print(summary)


if __name__ == "__main__":  # STUDYME okruh 19
    main()
