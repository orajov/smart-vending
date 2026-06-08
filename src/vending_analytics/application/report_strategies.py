import pandas as pd

from vending_analytics.analytics.product_report import build_product_report
from vending_analytics.application.sales_report import build_sales_summary
from vending_analytics.domain.transaction import Transaction


class SalesSummaryStrategy:  # STUDYME okruh 11
    def generate(self, transactions: list[Transaction]) -> dict:  # STUDYME okruh 5
        return build_sales_summary(transactions)


class ProductReportStrategy:  # STUDYME okruh 11
    def generate(self, transactions: list[Transaction]) -> pd.DataFrame:  # STUDYME okruh 5
        return build_product_report(transactions)
