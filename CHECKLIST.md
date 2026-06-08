# Checklist okruhů ze zkoušky

Pokrytí teorie z [`STUDYME.MD`](STUDYME.MD) v projektu **smart-vending**.

Legenda: ✅ pokryto · 🟡 částečně · ⬜ zatím ne

---

## OOP a návrh

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 1 | Základní principy OOP (třída, instance, atribut, metoda) | 🟡 | `domain/transaction.py` — `Transaction`, atributy, `@classmethod`, `to_dict` |
| 2 | Dědičnost | ⬜ | plánováno v README (`Product`, `Machine`, platby) |
| 3 | Vícenásobná dědičnost, MRO, diamond problem | ⬜ | — |
| 4 | Abstraktní třídy, ABC, kompozice, mixin | ⬜ | — |
| 5 | Polymorfismus a duck typing | ⬜ | — |
| 6 | Subtypový polymorfismus, Protocol | ⬜ | — |
| 7 | Iterátory a formy polymorfismu | ⬜ | zatím jen `for` / list comprehension |
| 8 | Základní UML vztahy | ⬜ | zatím jen v dokumentaci |

## Návrhové vzory

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 9 | Návrhové vzory obecně | ⬜ | — |
| 10 | Adapter | ⬜ | plánováno v `infrastructure/` |
| 11 | Strategy a Observer | ⬜ | plánováno v `application/` |
| 12 | Decorator (vzor + `@decorator`) | 🟡 | `@dataclass`, `@classmethod` v `transaction.py` |

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
| 17 | Pandas | ⬜ | plánováno v `analytics/` |
| 18 | Matplotlib | ⬜ | plánováno v `analytics/` |

## Jazyk a execution model

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 19 | Import v Pythonu | ✅ | balíčková struktura, absolutní importy, `__main__.py`, `if __name__ == "__main__"` |
| 20 | Rekurze, iterace, memoizace, DP | 🟡 | list comprehension ve `sales_report.py`, iterace v `json_loader.py` |
| 21 | Lazy evaluation, generátory, `yield` | 🟡 | generator expression v `sum(t.price for t in paid)` |
| 22 | Higher-order funkce, closure, lambda | ⬜ | — |

## Testování

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 23 | Unit testy a testovatelný kód | ✅ | `tests/`, oddělení logiky od I/O, čistá `build_sales_summary` |
| 24 | `unittest`, mocking, patching, TDD | 🟡 | `unittest.TestCase` + assertions; mock/TDD zatím ne |

## UI a architektura

| # | Okruh | Stav | Kde / poznámka |
|---|-------|------|----------------|
| 25 | UI a struktura interaktivního programu | ⬜ | zatím jednorázový CLI skript |
| 26 | CLI a `argparse` | ✅ | `__main__.py` — poziční argument `file` |
| 27 | Základní koncepty architektury | ✅ | vrstvy `domain/` · `application/` · `infrastructure/`, DI přes parametry |
| 28 | Serializace dat (JSON, dataclass) | ✅ | `json.load`, `Transaction.from_dict` / `to_dict` |

---

## Shrnutí

| Stav | Počet |
|------|-------|
| ✅ pokryto | 5 |
| 🟡 částečně | 6 |
| ⬜ ne | 17 |
| **Celkem** | **28** |

---

## Co už aplikace umí (funkčně)

- [x] Načíst transakce z JSON souboru
- [x] Deserializovat záznam na `Transaction`
- [x] Spočítat základní souhrn prodejů (počty, tržby z `paid`)
- [x] Spustit přes CLI (`python -m vending_analytics <soubor.json>`)
- [x] Unit testy pro `Transaction.from_dict` a `build_sales_summary`

## Co ještě chybí (viz [`TODO`](TODO))

- [ ] další metriky (průměr, tržby podle produktu/automatu, časové analýzy…)
- [ ] OOP hierarchie v `domain/`
- [ ] návrhové vzory (Strategy, Adapter, Observer)
- [ ] Pandas / NumPy / Matplotlib v `analytics/`
- [ ] mockování a rozšířené CLI příkazy z README

---

*Poslední aktualizace podle stavu kódu v `src/` a `tests/`.*
