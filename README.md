# Vending Sales Analytics

## Popis projektu

Projekt slouží ke zpracování dat z prodejního automatu.  
Aplikace přijímá transakční data ve formátu JSON, ukládá je, validuje a následně z nich vytváří přehledy o prodejích.

Cílem projektu je ukázat praktické použití Pythonu na reálném datovém problému.  
Současně slouží jako hlavní projekt pro procvičení teoretických okruhů ze zkoušky — vše je integrováno přímo v aplikaci, bez samostatných učebních složek.

---

## Vstupní data

Data přicházejí jako JSON soubory do složky:

```text
data/transactions/<kod automatu>/
```

Příklad názvu souboru:

```text
2026-06-04.json
```

Každý záznam reprezentuje jednu transakci z automatu.

### Příklad transakce

```json
{
  "transaction_id": "TX-20260604-0001",
  "machine_id": "VM-001",
  "timestamp": "2026-06-04T14:32:10",
  "product_id": "P-101",
  "product_name": "Coca-Cola 0.5L",
  "price": 35,
  "payment_method": "card",
  "payment_status": "paid",
  "card_provider": "Visa"
}
```

---

## Základní tok dat

```text
JSON soubor
    ↓
načtení dat
    ↓
validace dat
    ↓
uložení / zpracování
    ↓
analýzy a reporty
```

---

## Co aplikace analyzuje

Aplikace může počítat například:

- počet transakcí
- počet úspěšných a neúspěšných plateb
- celkové tržby a průměrnou hodnotu transakce
- tržby podle produktu a automatu
- prodeje podle času (den, hodina, špičky)
- nejprodávanější produkty
- podíl karetních poskytovatelů (Visa / Mastercard)
- výkon a porovnání automatů

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
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── analytics/
│       ├── interfaces/
│       └── utils/
│
├── tests/
├── STUDYME.MD
└── README.MD
```

---

## Hlavní části aplikace

### `domain/`

Doménové objekty a pravidla — transakce, produkt, automat, platba.  
Zde se projeví OOP, dědičnost, abstraktní třídy, kompozice a serializace objektů.

### `application/`

Aplikační logika — import transakcí, validace, tvorba reportů, orchestrace analýz.  
Zde se projeví návrhové vzory (Strategy pro typy reportů, Observer pro logování) a testovatelný kód.

### `infrastructure/`

Načítání a ukládání dat, práce se soubory, JSON.  
Zde se projeví serializace, Adapter pro různé formáty vstupu a oddělení vrstev architektury.

### `analytics/`

Výpočty a agregace — Pandas, NumPy, Matplotlib.  
Reporty podle produktů, času, plateb a automatů.

### `interfaces/`

Ovládání aplikace — CLI (`argparse`) a případně jednoduché GUI.

### `utils/`

Společné pomocné funkce sdílené napříč vrstvami.

### `tests/`

Unit testy, mocking a TDD pro parser, validaci, reporty a doménovou logiku.

---

## Teorie v praxi

Teoretické okruhy ze `STUDYME.MD` nejsou v samostatných ukázkách — každý se uplatní přímo v kódu projektu:

| Okruh | Kde v projektu |
|---|---|
| OOP, dědičnost, abstraktní třídy | `domain/` — `Transaction`, `Product`, `Machine`, platby |
| Kompozice, protokoly, duck typing | `application/` — rozhraní reportů a generátorů |
| Návrhové vzory (Strategy, Adapter, Observer, Decorator) | `application/`, `infrastructure/` |
| NumPy, Pandas, Matplotlib | `analytics/` |
| Serializace JSON | `domain/`, `infrastructure/` |
| Unit testy, mock, TDD | `tests/` |
| CLI, argparse | `interfaces/` |
| Vrstvená architektura | celá struktura `src/vending_analytics/` |
| Generátory, iterátory | `infrastructure/` — lazy načítání transakcí |

---

## Příklad použití

```bash
python -m vending_analytics import data/transactions/VM-001/2026-06-04.json
python -m vending_analytics report daily
python -m vending_analytics report products
python -m vending_analytics chart revenue
```

---

## Účel projektu

Jedna aplikace, která řeší reálný problém (analytika prodejů automatu) a zároveň pokrývá praktické i teoretické téma kurzu: OOP, návrhové vzory, práce s daty, testování, serializace a architektura programu.
