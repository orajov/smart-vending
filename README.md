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

- [x] načíst transakce z JSON souboru (`infrastructure/json_loader.py`)
- [x] deserializovat záznam na `Transaction` (`domain/transaction.py`)
- [x] spočítat základní souhrn prodejů — počet transakcí, úspěšných/neúspěšných plateb, celkové tržby (`application/sales_report.py`)
- [x] report tržeb podle produktu přes Pandas — funkce existuje, zatím není napojená na CLI (`analytics/product_report.py`)
- [x] spustit přes CLI s jedním argumentem — cesta k JSON souboru (`__main__.py`)
- [x] unit testy pro `Transaction.from_dict` a `build_sales_summary` (`tests/`)

## Co ještě chybí

- [ ] rozšířené CLI příkazy (`report`, `chart`, import složky)
- [ ] další metriky — průměr, tržby podle automatu, časové analýzy, platební metody…
- [ ] OOP hierarchie v `domain/` (`Product`, `Machine`, platby)
- [ ] návrhové vzory (Strategy, Adapter, Observer)
- [ ] NumPy a Matplotlib v `analytics/`
- [ ] mockování a TDD

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
načtení dat (json_loader)
    ↓
deserializace na Transaction
    ↓
aplikční logika / analýzy
    ↓
výstup (CLI print / budoucí reporty)
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
│       ├── __main__.py          # CLI vstupní bod
│       ├── domain/
│       │   └── transaction.py   # Transaction dataclass
│       ├── application/
│       │   └── sales_report.py  # build_sales_summary
│       ├── infrastructure/
│       │   └── json_loader.py   # načítání JSON
│       └── analytics/
│           └── product_report.py # tržby podle produktu (Pandas)
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

Doménové objekty — zatím `Transaction` jako `@dataclass` s `from_dict` / `to_dict`.  
Plánováno: `Product`, `Machine`, hierarchie plateb, OOP a serializace.

### `application/`

Aplikační logika oddělená od I/O — `build_sales_summary()` vrací slovník s metrikami.  
Plánováno: orchestrace reportů, návrhové vzory (Strategy, Observer).

### `infrastructure/`

Načítání dat ze souborů — `load_transactions(path)` čte JSON a vrací `list[Transaction]`.  
Plánováno: lazy načítání, Adapter pro další formáty.

### `analytics/`

Agregace a reporty — `build_product_report()` používá Pandas pro tržby podle produktu.  
Plánováno: NumPy, Matplotlib, časové a platební analýzy.

### `tests/`

Unit testy (`unittest`) pro doménu a aplikační logiku.  
Plánováno: mockování I/O, TDD.

---

## Požadavky a instalace

- Python **3.12+**
- závislosti: `ruff`, `pandas` (viz [`requirements.txt`](requirements.txt))

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Spuštění

Z kořene projektu (s aktivním venv a nainstalovanými závislostmi):

```bash
PYTHONPATH=src python -m vending_analytics data/transactions/VM-001/2026-06-04.json
```

Příklad výstupu:

```text
načteno 50 transakcí
{'transaction_count': 50, 'paid_count': 45, 'failed_count': 5, 'total_revenue': 1575}
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
| CLI, `argparse` | ✅ | `__main__.py` — poziční argument `file` |
| Vrstvená architektura | ✅ | `domain/` · `application/` · `infrastructure/` |
| List comprehension, generátory | 🟡 | `sales_report.py`, `sum(t.price for t in paid)` |
| Pandas | 🟡 | `product_report.py` — zatím mimo CLI |
| Decorator (`@dataclass`, `@classmethod`) | 🟡 | `transaction.py` |
| OOP, dědičnost, abstraktní třídy | ⬜ | plánováno v `domain/` |
| Návrhové vzory | ⬜ | plánováno v `application/`, `infrastructure/` |
| NumPy, Matplotlib | ⬜ | plánováno v `analytics/` |
| Mock, TDD | ⬜ | plánováno v `tests/` |

Podrobná tabulka všech 28 okruhů: [`CHECKLIST.md`](CHECKLIST.md).

---

## Účel projektu

Jedna aplikace, která řeší reálný problém (analytika prodejů automatu) a postupně pokrývá praktické i teoretické téma kurzu: OOP, návrhové vzory, práce s daty, testování, serializace a architektura programu.
