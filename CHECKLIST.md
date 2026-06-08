# Checklist okruhů ze zkoušky

Pokrytí teorie z [`STUDYME.MD`](STUDYME.MD) v projektu **smart-vending**.

Legenda: ✅ pokryto · 🟡 částečně · ⬜ zatím ne

---

## OOP a návrh

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 1 | Základní principy OOP (třída, instance, atribut, metoda) | 🟡 | `domain/transaction.py`, `domain/payment.py` — třídy, atributy, `@classmethod`, `is_paid()` |
| 2 | Dědičnost | ✅ | `Payment` → `CardPayment` v `domain/payment.py`; `Transaction.payment` |
| 3 | Vícenásobná dědičnost, MRO, diamond problem | ⬜ | — |
| 4 | Abstraktní třídy, ABC, kompozice, mixin | ⬜ | kompozice `Transaction.payment` existuje, ABC zatím ne |
| 5 | Polymorfismus a duck typing | 🟡 | `is_paid()` přes dědičnost; Strategy třídy bez společného base class |
| 6 | Subtypový polymorfismus, Protocol | ✅ | `ReportStrategy` Protocol v `application/report_protocol.py` |
| 7 | Iterátory a formy polymorfismu | ✅ | `iter_transactions()` vrací `Iterator[Transaction]`, `yield` v `json_loader.py` |
| 8 | Základní UML vztahy | ⬜ | zatím jen v dokumentaci |

## Návrhové vzory

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 9 | Návrhové vzory obecně | 🟡 | Strategy + Adapter implementovány, Observer chybí |
| 10 | Adapter | ✅ | `LegacyTransactionAdapter` v `infrastructure/legacy_adapter.py` |
| 11 | Strategy a Observer | 🟡 | Strategy: `SalesSummaryStrategy`, `ProductReportStrategy`; Observer zatím ne |
| 12 | Decorator (vzor + `@decorator`) | 🟡 | `@dataclass`, `@classmethod` v `transaction.py`, `payment.py` |

## Paměť

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 13 | Stack a heap | ⬜ | teorie, v projektu zatím ne |
| 14 | Ruční a automatická správa paměti | ⬜ | teorie |
| 15 | Správa paměti a proměnné v Pythonu | ⬜ | teorie |

## Data a vizualizace

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 16 | NumPy | ⬜ | plánováno v `analytics/` |
| 17 | Pandas | ✅ | `product_report.py`, CLI `--report products` |
| 18 | Matplotlib | ✅ | `charts.py` — `save_product_revenue_chart()`, PNG při `--report products` |

## Jazyk a execution model

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 19 | Import v Pythonu | ✅ | balíčková struktura, absolutní importy, `__main__.py`, `if __name__ == "__main__"` |
| 20 | Rekurze, iterace, memoizace, DP | 🟡 | list comprehension ve `sales_report.py`, iterace v `json_loader.py` |
| 21 | Lazy evaluation, generátory, `yield` | ✅ | `iter_transactions()` s `yield`; `load_transactions()` volá `list(...)` |
| 22 | Higher-order funkce, closure, lambda | ⬜ | — |

## Testování

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 23 | Unit testy a testovatelný kód | ✅ | `tests/` — doména, aplikace, oddělení logiky od I/O |
| 24 | `unittest`, mocking, patching, TDD | 🟡 | `@patch`, `MagicMock` v `test_json_loader.py`; TDD zatím ne |

## UI a architektura

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 25 | UI a struktura interaktivního programu | 🟡 | CLI s volbou reportu (`--report`), zatím bez plnohodnotného menu |
| 26 | CLI a `argparse` | ✅ | `__main__.py` — poziční argument `file`, `--report summary\|products` |
| 27 | Základní koncepty architektury | ✅ | vrstvy `domain/` · `application/` · `infrastructure/`, DI přes parametry, Strategy |
| 28 | Serializace dat (JSON, dataclass) | ✅ | `json.load`, `Transaction.from_dict` / `to_dict`, `CardPayment.from_dict` |

---

## Shrnutí

| Stav | Počet |
|------|-------|
| ✅ pokryto | 12 |
| 🟡 částečně | 8 |
| ⬜ ne | 8 |
| **Celkem** | **28** |

---

## Co už aplikace umí (funkčně)

- [x] Načíst transakce z JSON souboru (včetně lazy iterátoru)
- [x] Deserializovat záznam na `Transaction` s `CardPayment`
- [x] OOP hierarchie plateb (`Payment` → `CardPayment`)
- [x] Spočítat základní souhrn prodejů (počty, tržby z `paid`)
- [x] Report tržeb podle produktu (Pandas) a PNG graf (Matplotlib)
- [x] CLI s `--report summary|products`
- [x] Strategy pattern pro volbu reportu
- [x] Adapter pro starý JSON formát (`LegacyTransactionAdapter`)
- [x] Unit testy pro doménu, aplikaci a mockované načítání JSON

## Co ještě chybí (viz [`TODO`](TODO))

- [ ] další metriky (průměr, tržby podle automatu, časové analýzy, platební metody…)
- [ ] doménové třídy `Product`, `Machine`
- [ ] návrhový vzor Observer
- [ ] NumPy v `analytics/`
- [ ] import celé složky transakcí, samostatný CLI příkaz pro graf
- [ ] TDD workflow

---

*Poslední aktualizace podle stavu kódu v `src/` a `tests/`.*
