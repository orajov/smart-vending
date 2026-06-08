# Vending Sales Analytics

Analytika prodejů z prodejních automatů — studijní projekt v Pythonu.

Repozitář: [github.com/orajov/smart-vending](https://github.com/orajov/smart-vending)

---

## Popis projektu

Projekt zpracovává transakční data z prodejních automatů ve formátu JSON.  
Aplikace data načte, deserializuje do doménových objektů a počítá základní přehledy o prodejích.

Cílem je ukázat praktické použití Pythonu na reálném datovém problému a zároveň procvičit teoretické okruhy ze zkoušky — vše je integrováno přímo v aplikaci, bez samostatných učebních složek.

Podrobný přehled pokrytí teorie: [`STUDYME.md`](STUDYME.md) · [`CHECKLIST.md`](CHECKLIST.md)  
Plánované metriky a reporty: [`TODO`](TODO)

---

## Co aplikace umí teď

- [x] načíst transakce z JSON souboru — včetně lazy iterátoru (`infrastructure/json_loader.py`)
- [x] deserializovat záznam na `Transaction` s vnořenou platbou `CardPayment` (`domain/transaction.py`, `domain/payment.py`)
- [x] OOP hierarchie plateb — `Payment` → `CardPayment` s metodou `is_paid()`
- [x] spočítat základní souhrn prodejů — počet transakcí, úspěšných/neúspěšných plateb, celkové tržby (`application/sales_report.py`)
- [x] report tržeb podle produktu přes Pandas (`analytics/product_report.py`)
- [x] uložit sloupcový graf tržeb podle produktu (`analytics/charts.py`)
- [x] návrhový vzor Strategy — volitelné reporty přes `ReportStrategy` Protocol (`application/report_protocol.py`, `report_strategies.py`)
- [x] návrhový vzor Adapter — převod starého JSON formátu (`infrastructure/legacy_adapter.py`)
- [x] CLI s argumentem `--report summary|products` (`__main__.py`)
- [x] unit testy pro doménu, aplikační logiku a mockované načítání JSON (`tests/`)

## Co ještě chybí

- [ ] další metriky — průměr, tržby podle automatu, časové analýzy, platební metody…
- [ ] další doménové třídy — `Product`, `Machine`
- [ ] návrhový vzor Observer
- [ ] NumPy v `analytics/`
- [ ] import celé složky transakcí, samostatný CLI příkaz pro graf
- [ ] TDD workflow

Kompletní seznam plánovaných analýz je v [`TODO`](TODO).

---

## Vstupní data

Data přicházejí jako JSON soubory do složky:

```text
data/transactions/<kód automatu>/
```

Příklad názvu souboru:

```text
2026-06-04.json
```

Soubor obsahuje pole transakcí. Každý záznam reprezentuje jednu transakci z automatu.

### Příklad transakce

```json
{
  "transaction_id": "TX-20260604-0001",
  "machine_id": "VM-001",
  "timestamp": "2026-06-04T07:12:10",
  "product_id": "P-101",
  "product_name": "Coca-Cola 0.5L",
  "price": 35,
  "payment_status": "paid",
  "card_provider": "Visa"
}
```

---

## Základní tok dat

```text
JSON soubor
    ↓
načtení dat (json_loader / legacy_adapter)
    ↓
deserializace na Transaction + CardPayment
    ↓
Strategy reportu (summary / products)
    ↓
výstup (CLI print / Pandas tabulka / PNG graf)
```

---

## Struktura projektu

```text
smart-vending/
├── data/
│   └── transactions/
│       └── VM-001/
│           └── 2026-06-04.json
│
├── src/
│   └── vending_analytics/
│       ├── __main__.py              # CLI vstupní bod (--report)
│       ├── domain/
│       │   ├── transaction.py       # Transaction dataclass
│       │   └── payment.py           # Payment, CardPayment (dědičnost)
│       ├── application/
│       │   ├── sales_report.py      # build_sales_summary
│       │   ├── report_protocol.py   # ReportStrategy Protocol
│       │   └── report_strategies.py # Strategy pro summary / products
│       ├── infrastructure/
│       │   ├── json_loader.py       # načítání JSON, iter_transactions
│       │   └── legacy_adapter.py    # Adapter pro starý formát
│       └── analytics/
│           ├── product_report.py    # tržby podle produktu (Pandas)
│           └── charts.py            # sloupcový graf (Matplotlib)
│
├── tests/
├── pyproject.toml
├── requirements.txt
├── CHECKLIST.md
├── STUDYME.md
├── TODO
└── README.md
```

Plánované složky, které zatím neexistují: `interfaces/`, `utils/`.

---

## Hlavní části aplikace

### `domain/`

Doménové objekty — `Transaction` jako `@dataclass` s `from_dict` / `to_dict` a vnořenou platbou.  
Hierarchie plateb: `Payment` (základní stav) → `CardPayment` (dědičnost, `provider`, `is_paid()`).  
Plánováno: `Product`, `Machine`, abstraktní třídy.

### `application/`

Aplikační logika oddělená od I/O — `build_sales_summary()` vrací slovník s metrikami.  
Strategy pattern: `ReportStrategy` Protocol a implementace `SalesSummaryStrategy`, `ProductReportStrategy`.  
Plánováno: Observer pro notifikace o reportech.

### `infrastructure/`

Načítání dat ze souborů — `load_transactions(path)` a lazy `iter_transactions(path)` s `yield`.  
Adapter — `LegacyTransactionAdapter` mapuje starší JSON schéma na aktuální formát.

### `analytics/`

Agregace a vizualizace — `build_product_report()` používá Pandas, `save_product_revenue_chart()` Matplotlib.  
Plánováno: NumPy, časové a platební analýzy.

### `tests/`

Unit testy (`unittest`) pro doménu, aplikační logiku a mockované I/O (`@patch`, `MagicMock`).  
Plánováno: TDD workflow.

---

## Požadavky a instalace

- Python **3.12+**
- závislosti: `ruff`, `pandas`, `matplotlib` (viz [`requirements.txt`](requirements.txt))

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Spuštění

Z kořene projektu (s aktivním venv a nainstalovanými závislostmi):

```bash
# základní souhrn prodejů (výchozí)
PYTHONPATH=src python -m vending_analytics data/transactions/VM-001/2026-06-04.json

# report tržeb podle produktu + PNG graf
PYTHONPATH=src python -m vending_analytics data/transactions/VM-001/2026-06-04.json --report products
```

Příklad výstupu (`--report summary`):

```text
načteno 50 transakcí
{'transaction_count': 50, 'paid_count': 45, 'failed_count': 5, 'total_revenue': 1575}
```

Příklad výstupu (`--report products`):

```text
načteno 50 transakcí
  product_name  revenue
Coca-Cola 0.5L      420
    Pepsi 0.5L      340
         ...
graf uložen: product_revenue.png
```

---

## Testy

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Lint a formátování (Ruff):

```bash
ruff check src tests
ruff format src tests
```

---

## Teorie v praxi

Teoretické okruhy ze [`STUDYME.md`](STUDYME.md) se uplatňují přímo v kódu. Aktuální stav pokrytí:

| Okruh | Stav | Kde v projektu |
|---|---|---|
| Import, balíčková struktura | ✅ | `src/vending_analytics/`, absolutní importy, `__main__.py` |
| Serializace JSON, dataclass | ✅ | `json_loader.py`, `Transaction.from_dict` / `to_dict` |
| Unit testy, testovatelný kód | ✅ | `tests/`, čistá `build_sales_summary` bez I/O |
| Mockování I/O | ✅ | `test_json_loader.py` — `@patch`, `MagicMock` |
| CLI, `argparse` | ✅ | `__main__.py` — `--report summary\|products` |
| Vrstvená architektura | ✅ | `domain/` · `application/` · `infrastructure/` |
| Dědičnost, polymorfismus | ✅ | `Payment` → `CardPayment`, `is_paid()` |
| Protocol, Strategy | ✅ | `ReportStrategy`, `SalesSummaryStrategy`, `ProductReportStrategy` |
| Adapter | ✅ | `LegacyTransactionAdapter` |
| Generátory, lazy načítání | ✅ | `iter_transactions()` s `yield` |
| List comprehension | 🟡 | `sales_report.py`, `sum(t.price for t in paid)` |
| Pandas | ✅ | `product_report.py`, CLI `--report products` |
| Matplotlib | ✅ | `charts.py`, PNG graf při `--report products` |
| Decorator (`@dataclass`, `@classmethod`) | 🟡 | `transaction.py`, `payment.py` |
| NumPy | ⬜ | plánováno v `analytics/` |
| Observer, ABC | ⬜ | plánováno |
| TDD | ⬜ | plánováno v `tests/` |

Podrobná tabulka všech 28 okruhů: [`CHECKLIST.md`](CHECKLIST.md).

---

## Účel projektu

Jedna aplikace, která řeší reálný problém (analytika prodejů automatu) a postupně pokrývá praktické i teoretické téma kurzu: OOP, návrhové vzory, práce s daty, testování, serializace a architektura programu.
