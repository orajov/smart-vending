Níže naleznete vypracované tematické okruhy ke zkoušce. Každý okruh má několik podtémat, která byste v rámci odpovědi měli pokrýt. Materiál vychází z přednášek a studijních materiálů (OOP, paměť, NumPy, importy, execution model, UI, architektura, serializace, vizualizace dat a testování).

---

## 1. Základní principy objektově orientovaného programování v Pythonu

**Třída, instance, atribut, metoda**
- **Třída** je šablona (předpis) popisující, jak vypadají a co umí objekty daného typu. Sdružuje data a operace nad nimi do jednoho pojmenovaného celku.
- **Instance (objekt)** je konkrétní výskyt třídy vytvořený jejím zavoláním (`obj = MyClass(...)`).
- **Atribut** je pojmenovaná hodnota uložená v objektu (data).
- **Metoda** je funkce definovaná uvnitř třídy, která popisuje chování objektu.

**Atributy instance vs. atributy třídy**
- *Atribut instance* je uložen v konkrétním objektu (typicky nastaven v `__init__` přes `self.x = ...`), každá instance má vlastní.
- *Atribut třídy* je sdílený všemi instancemi (definovaný přímo v těle třídy).

**Metoda instance vs. třídní metoda vs. statická metoda**
- *Metoda instance* – první parametr `self`, pracuje s konkrétním objektem.
- *Třídní metoda* – `@classmethod`, první parametr `cls`, pracuje s třídou (typicky alternativní konstruktory, např. `from_dict`).
- *Statická metoda* – `@staticmethod`, nedostává `self` ani `cls`, je to obyčejná funkce logicky patřící do třídy.

**Dunder metody** – speciální metody s dvojitým podtržítkem, které definují chování objektu vůči jazyku:
- `__init__` – inicializace objektu, `__str__`/`__repr__` – textová reprezentace, `__eq__` – porovnání, `__len__`, `__getitem__`, `__iter__`/`__next__` (iterace) atd.

**Zapouzdření (encapsulation)**
- Sdružení dat a operací do logického celku, často s omezením přímého přístupu k vnitřnímu stavu.
- V Pythonu je řízení přístupu spíše **konvence**: `_x` znamená „interní“, `__x` spouští name mangling.
- **Property, gettery a settery**: pomocí `@property` lze přistupovat k atributu jako k hodnotě, ale za přístupem může běžet logika (validace, výpočet).

**Příklad třídy s rozumným rozhraním**
```python
class Account:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount
```

---

## 2. Dědičnost v Pythonu

**Princip a vztah rodič–potomek**
- Dědičnost umožňuje, aby nově definovaná třída (potomek/odvozená třída) přebírala atributy a metody z již existující třídy (rodič/základní třída).
- Potomek může přidávat nové chování i upravovat (překrývat) zděděné.

**Vztah is-a**
- Dědičnost vyjadřuje vztah „je typu“ (a `Car` *is a* `Vehicle`). Vhodná je tam, kde potomek skutečně je specializací rodiče.

**`super()`**
- Volá metodu rodičovské třídy. Typicky v `__init__`, aby se správně inicializovaly zděděné atributy:
```python
class Vehicle:
    def __init__(self, name): self.name = name

class Car(Vehicle):
    def __init__(self, name, brand):
        super().__init__(name)
        self.brand = brand
```

**Překrývání metod (override)**
- Potomek definuje metodu stejného jména jako rodič a tím nahradí její chování pro instance potomka.

**Dědění atributů a metod**
- Pokud potomek atribut/metodu nedefinuje, Python ji hledá u rodiče (podle MRO – viz okruh 3).

**Příklad hierarchie**
```python
class Shape:
    def area(self) -> float: raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, a, b): self.a, self.b = a, b
    def area(self) -> float: return self.a * self.b
```

---

## 3. Vícenásobná dědičnost, MRO a diamond problem

**Dědičnost do hloubky vs. vícenásobná dědičnost**
- Do hloubky: lineární řetěz `A → B → C`.
- Vícenásobná: třída dědí z **více než jedné** rodičovské třídy zároveň (`class D(B, C)`).

**MRO – Method Resolution Order**
- Pořadí, v jakém Python prohledává třídy při hledání atributu/metody. Lze zobrazit `D.__mro__` nebo `D.mro()`. CPython používá algoritmus C3 linearizace.

**Proč záleží na pořadí rodičů**
- U `class D(B, C)` se nejprve hledá v `B`, pak v `C`. Změna pořadí může změnit, která metoda se zavolá.

**Diamond problem (diamond of death)**
- Vzniká, když dvě třídy (`B`, `C`) dědí ze společného předka `A` a další třída `D` dědí z obou. Otázka je, čí verzi metody použít. MRO problém deterministicky řeší (`D → B → C → A`).
```python
class A:
    def greet(self): print("A")
class B(A):
    def greet(self): print("B")
class C(A):
    def greet(self): print("C")
class D(B, C): pass
D().greet()   # "B" – díky MRO (D, B, C, A)
```

**Role `super()` ve vícenásobné dědičnosti**
- `super()` nevolá nutně „rodiče“, ale **další třídu v MRO**, čímž umožňuje řetězené (kooperativní) volání napříč hierarchií.

**Riziko**
- Vícenásobná dědičnost může vést k nepřehlednému návrhu, kde není jasné, odkud chování pochází.

---

## 4. Abstraktní třídy, typy a kompozice jako alternativa k dědičnosti

**Abstraktní třída**
- Definuje rozhraní (co potomci musí umět), ale sama není určena k instanciaci. Slouží jako „smlouva“ pro potomky.

**`ABC` a `@abstractmethod`**
```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
```
- Dědíme z `ABC`, abstraktní metody značíme `@abstractmethod`.
- Pokud potomek abstraktní metodu neimplementuje, **nelze vytvořit instanci** (`TypeError`).

**`type`, `isinstance`, `issubclass`**
- `type(obj)` – vrací typ objektu.
- `isinstance(obj, Cls)` – je objekt instancí třídy (i podtřídy)?
- `issubclass(Sub, Base)` – je třída podtřídou jiné?

**Kompozice místo dědičnosti**
- Místo „je typu“ použijeme „má/používá“ (has-a): objekt obsahuje jiné objekty a deleguje na ně práci. Vhodnější, když nejde o pravou specializaci. Snižuje provázanost a křehkost hierarchií.

**Mixin**
- Malá třída přidávající konkrétní funkčnost (např. logování) přes dědičnost, aniž by představovala hlavní typ objektu.
```python
class LoggerMixin:
    def log(self, msg): print(f"[LOG]: {msg}")
class Worker:
    def work(self): print("Working...")
class LoggingWorker(LoggerMixin, Worker): pass
```

**Rizika** – příliš složité a hluboké dědičné hierarchie jsou těžko čitelné, špatně se mění a testují.

---

## 5. Polymorfismus a duck typing

**Obecná myšlenka polymorfismu**
- Stejné volání (stejné rozhraní) může mít různé chování podle konkrétního objektu („stejné volání, různé chování“).

**Duck typing**
- „Když to kváká jako kachna…“ – v Pythonu nezáleží na typu objektu, ale na tom, zda má potřebné metody/atributy. Nezkoumáme typ, jen že objekt umí, co potřebujeme.

**Implicitní kontrakt**
- Funkce předpokládá, že objekt podporuje určité rozhraní (např. metodu `.area()`), aniž by to bylo formálně vynuceno typem.

**Výhody a nevýhody**
- (+) flexibilita, méně boilerplate, snadné rozšiřování.
- (−) chyby se projeví až za běhu, kontrakt není explicitní.

**Příklad polymorfní funkce bez dědičnosti**
```python
def total_area(shapes):
    return sum(s.area() for s in shapes)  # stačí, aby každý měl .area()
```

---

## 6. Subtypový polymorfismus, rozhraní a protokoly

**Subtypový polymorfismus**
- Objekt podtypu lze použít všude tam, kde se očekává nadtyp. Úzce souvisí s dědičností (potomek lze použít místo rodiče).

**Nominální vs. strukturální typování**
- *Nominální*: kompatibilita podle jména/dědičnosti (musím explicitně dědit z typu) – typické pro ABC.
- *Strukturální*: kompatibilita podle struktury (mám-li správné metody, jsem kompatibilní) – to je `Protocol`.

**`Protocol`**
```python
from typing import Protocol
class Animal(Protocol):
    def animalSound(self) -> None: ...
```
- Definuje rozhraní strukturálně – stačí mít odpovídající metody, není nutné dědit.

**ABC vs. Protocol**
- `ABC` = nominální (explicitní dědičnost, runtime kontrola při instanciaci).
- `Protocol` = strukturální (duck typing podpořený typovými anotacemi, kontrola hlavně statickým analyzátorem).

---

## 7. Iterátory a formy polymorfismu

**Iterovatelný objekt (iterable)**
- Objekt, přes který lze procházet (`for x in obj`). Umí vrátit iterátor přes `__iter__`.

**Iterable vs. iterátor**
- *Iterable* poskytuje iterátor (`iter(obj)`).
- *Iterátor* drží stav iterace a vrací další prvek přes `__next__`.

**`iter`, `next`, `StopIteration`**
- `iter(obj)` získá iterátor, `next(it)` vrátí další prvek; po vyčerpání iterátor vyvolá `StopIteration`.

**Vlastní iterátor**
```python
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self): return self
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1
        return self.n + 1
```

**Druhy polymorfismu**
- *Ad-hoc* (přetěžování, různé chování pro různé typy), *subtypový* (přes dědičnost/podtypy), *parametrický* (kód funguje pro libovolný typ – generika).
- **Generika** jsou projevem parametrického polymorfismu: jeden kód pracuje uniformně nad mnoha typy.

---

## 8. Základní UML vztahy

**K čemu UML**
- Unified Modeling Language – standardní způsob, jak vizualizovat návrh systému (třídy a vztahy mezi nimi) nezávisle na jazyce.

**Reprezentace třídy**
- Obdélník se třemi částmi: název, atributy, metody. Viditelnost: `+` veřejné, `-` privátní.

**Dědičnost a implementace rozhraní**
- Dědičnost: prázdná trojúhelníková šipka k rodiči. Implementace rozhraní (`<<interface>>`): přerušovaná čára s trojúhelníkem.

**Asociace, agregace, kompozice**
- *Asociace*: jeden objekt používá/zná jiný (např. `DataService` dostává `Logger` jako parametr).
- *Agregace* (weak has-a): celek obsahuje části, ale části přežijí zánik celku (`Project` ↔ `Developer`).
- *Kompozice* (strong has-a): části jsou existenčně závislé na celku, zanikají s ním (`Order` ↔ `OrderItem`).

**Příklad** – `Order` (kompozice) drží seznam `OrderItem`; `Report` (asociace/agregace) používá `SimInterface` jako zdroj dat.

---

## 9. Návrhové vzory a jejich role v návrhu programu

**Co je návrhový vzor**
- Obecné, ustálené řešení opakujícího se problému při návrhu programů. Popisuje role aktérů a jejich spolupráci.

**Není hotový kód**
- Není knihovna ani úryvek k vložení – je to **šablona/popis řešení**, kterou přizpůsobíme konkrétní situaci.

**Souvislost s OOP**
- Většina vzorů předpokládá OOP – aktivně využívají dědičnost a polymorfismus (sdružení dat a operací, odvozování složitějších objektů z jednodušších).

**Vliv jazyka**
- Podoba vzoru závisí na jazyce: Python (dynamický, interpretovaný, bez přetěžování funkcí, stručný) vs. C++ (statický, kompilovaný, přetěžování, silná compile-time kontrola). Některé vzory jsou v Pythonu díky jeho flexibilitě triviální nebo zbytečné.

**Původ** – „Gang of Four“ (GoF, 1994), 23 vzorů ve třech kategoriích: *creational, structural, behavioral*.

**Příklad užitečnosti** – sjednocení nekompatibilních rozhraní (Adapter), výměna algoritmu za běhu (Strategy), reakce více částí na událost (Observer).

**Riziko** – přehnané používání vzorů vede ke zbytečně složitému, „přeinženýrovanému“ návrhu.

---

## 10. Návrhový vzor Adapter

**Problém**
- Klient očekává určité rozhraní (Target), ale máme existující třídu/knihovnu (Adaptee) s jiným rozhraním. Nechceme/nemůžeme měnit ani klienta, ani původní implementaci (legacy kód, externí knihovna, zpětná kompatibilita).

**Role**
- *Client* – používá Target rozhraní.
- *Target interface* – rozhraní očekávané klientem.
- *Adapter* – převádí volání a data mezi světy, implementuje Target a deleguje na Adaptee.
- *Adaptee* – existující třída s jiným rozhraním.

**Proč neměnit originál** – legacy kód, externí závislost, jiné oddělení, zpětná kompatibilita.

**Typické použití** – integrace legacy API, sjednocení různých providerů, migrace mezi verzemi API.

**Příklad**
```python
class LegacySimulation:
    def get_results(self):
        return [(0.0, -1.2), (0.1, -1.18)]

class SimulationAdapter:           # implementuje fetch() očekávané Reportem
    def __init__(self, simulation): self.simulation = simulation
    def fetch(self):
        raw = self.simulation.get_results()
        return [{"time": t, "energy": e} for t, e in raw]
```

**Souvislost s polymorfismem** – Adapter funguje díky tomu, že klient pracuje přes rozhraní; adaptér je polymorfní náhradou očekávaného typu.

---

## 11. Návrhové vzory Strategy a Observer

**Strategy**
- Zapouzdřuje **rodinu zaměnitelných algoritmů** a umožňuje je vyměnit za běhu.
- Odděluje algoritmus (strategie) od objektu (context), který ho používá.
- Často využívá **kompozici**: context drží referenci na strategii a deleguje na ni.
```python
class Logger:
    def __init__(self, strategies): self.log_strategies = strategies
    def write_message(self, msg):
        for s in self.log_strategies: s.log(msg)
```

**Observer**
- Jeden objekt (*Subject/Publisher*) mění stav nebo generuje události; více nezávislých částí (*Observers/Subscribers*) chce reagovat.
- Observers se přihlásí k odběru (`subscribe`), Subject je při události notifikuje (`notify`).
- (+) volná vazba, snadné přidávání/odebírání reakcí za běhu; (−) pořadí notifikací a ladění toku událostí může být méně přehledné.
```python
class Simulation:
    def __init__(self): self._observers = []
    def subscribe(self, o): self._observers.append(o)
    def _notify(self, event):
        for o in self._observers: o.update(event)
```

**Kdy co** – Strategy: výběr algoritmu (např. způsob logování, řazení). Observer: rozesílání událostí (UI, metriky, logování reaguje na změnu modelu).

---

## 12. Decorator jako návrhový vzor a dekorátory v Pythonu

**Wrapper**
- Nová funkce/objekt, který **obalí** původní a přidá chování bez zásahu do jeho definice.

**Decorator pattern**
- Návrhový vzor pro rozšiřování chování objektu „zvenku“, bez úpravy původního objektu.

**Decorator pattern vs. `@decorator`**
- *Pattern* je obecná myšlenka obalování. *Syntaxe* `@decorator` v Pythonu je syntaktický cukr pro `f = decorator(f)`.

**Jak funguje dekorátor funkce**
```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(x, y): return x + y
```
- Dekorátor je funkce přijímající funkci a vracející obalenou funkci (využívá closure). Lze i parametrizovat (funkce vracející dekorátor).

**Dekorátory, memoizace a `lru_cache`**
- Typické použití dekorátoru je **memoizace** – ukládání výsledků do cache a jejich opětovné použití (zrychlení např. rekurzivního Fibonacciho).
- `functools.lru_cache` je hotová, lépe napsaná implementace memoizace (least recently used cache).
- Známé vestavěné dekorátory: `@classmethod`, `@staticmethod`, `@abstractmethod`, `@dataclass`, `@property`.

---

## 13. Paměť počítače, stack a heap

**Paměť jako adresovatelné pole bytů**
- Paměť je velké pole bytů, každý má svou adresu. Procesor čte/zapisuje data a pracuje s adresami.

**Proměnné a paměť**
- Proměnné v konečném důsledku odpovídají oblastem paměti (v C přímo, v Pythonu nepřímo přes objekty – viz okruh 15).

**Stack (zásobník)**
- Paměť pro volání funkcí. Každé volání vytvoří **stack frame** (lokální proměnné, parametry, návratová adresa). Funguje jako LIFO. Rychlá alokace, automatické uvolnění, omezená velikost. Nekonečná rekurze → **stack overflow**.

**Stack a volání funkcí**
- Každé nové volání přidá rámec; návrat z funkce rámec odstraní.

**Heap (halda)**
- Oblast pro **dynamickou alokaci** za běhu (v C `malloc`/`free`). Paměť zůstává, dokud se explicitně neuvolní. Pro velké struktury a objekty s neznámou životností.

**Stack vs. heap**

| Stack | Heap |
|---|---|
| automatická správa | ruční správa (v C) |
| rychlá alokace | pomalejší |
| malá velikost | velká velikost |
| lokální proměnné | dynamické struktury |

---

## 14. Ruční a automatická správa paměti

**Ruční správa (C)**
- Programátor alokuje a uvolňuje paměť sám.
- `malloc(size)` přidělí paměť na heapu, `free(p)` ji uvolní.
- (+) rychlost, kontrola; (−) náchylnost k chybám.

**Typické chyby**
- *Memory leak* – alokovaná paměť se nikdy neuvolní → roste spotřeba, zpomalení, pád.
- *Dangling pointer* – ukazatel na již uvolněnou paměť; zápis vede k **undefined behavior**.
- *Segmentation fault* – přístup do nepovolené oblasti (mimo pole, dereference `NULL`); OS proces ukončí (SIGSEGV).

**Undefined behavior**
- Situace, kdy jazyk nedefinuje, co se má stát – program může spadnout, fungovat náhodně, nebo zdánlivě správně.

**Automatická správa**
- Paměť spravuje runtime, ne programátor. Techniky: **reference counting**, **garbage collection**, region/arena, ownership.

**Reference counting vs. garbage collection**
- *Reference counting*: každý objekt si pamatuje počet referencí; při poklesu na 0 zaniká. Rychlé uvolnění, ale neřeší cykly.
- *Garbage collection*: periodicky hledá nedosažitelné objekty (včetně cyklů). Řeší cykly, ale s režií.

---

## 15. Správa paměti a proměnné v Pythonu

**Proměnná = jméno navázané na objekt**
- V Pythonu proměnná není oblast paměti (jako v C), ale **jméno odkazující na objekt**. Objekt obsahuje typ, hodnotu a metadata.

**Sdílení objektů**
- Více jmen může odkazovat na stejný objekt:
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4] – seznam je mutable a sdílený
```

**Příkaz `del`**
- `del` nemaže přímo objekt, ale **jméno (jednu referenci)**. Objekt zanikne, až když ztratí poslední referenci.

**Životnost objektu**
- Určuje ji **existence referencí**, ne místo v kódu. Objekt drží naživu vrácení z funkce, uložení do struktury, globální proměnná atd.

**Reference counting v CPythonu**
- CPython počítá reference na každý objekt; při poklesu na 0 ho typicky ihned uvolní. `sys.getrefcount(obj)` ukazuje o 1 více (dočasná reference z argumentu).

**Referenční cykly a GC**
- Když objekty odkazují na sebe navzájem, jejich počet referencí neklesne na 0 ani po smazání jmen. Takové cykly musí najít **generační garbage collector** (generace 0/1/2; mladší se kontrolují častěji). Modul `gc` umožňuje ladění (`gc.collect()`, `gc.get_threshold()`).

*Pozn.: reference counting je implementační detail CPythonu; jiné implementace (PyPy, Jython) mohou používat jen GC.*

---

## 16. NumPy

**Proč jsou Python cykly pomalé**
- Při každé iteraci Python načte objekt, zkontroluje typ, zavolá operátor, vytvoří nový objekt… To je pro miliony prvků pomalé.

**Základní myšlenka**
- Místo práce s jednotlivými čísly provádíme operace nad **celými poli najednou**; velká část výpočtu běží v optimalizovaném C kódu.

**`ndarray`**
- Základní datová struktura: homogenní pole pevného typu s libovolným počtem dimenzí. Atributy:
  - `shape` – rozměry, `dtype` – typ prvků, `ndim` – počet dimenzí, `size` – počet prvků.

**Indexování**
- Podobné seznamům: `a[3]`, `a[2:6]`; u vícerozměrných `m[0,1]`, `m[:,1]` (sloupec). Slicing typicky vytváří **view** (sdílí data), kopii lze vynutit `.copy()`.

**Vektorizace**
- Operace nad celými poli bez explicitních cyklů (`a + b`, `x**2`, `np.sin(x)`). Výpočet probíhá element-wise v C kódu.

**Vektorizace vs. Python cyklus**
- Vektorizovaný výpočet je výrazně rychlejší (méně režie, CPU cache, SIMD) a kratší/čitelnější.

**Příklad zjednodušení**
```python
x = np.linspace(0, 10, 1_000_000)
y = np.sin(x) + x**2          # místo cyklu s math.sin
```
- Doplňkově: **broadcasting** (operace mezi poli různých rozměrů), operace podél os (`axis=0/1`).

---

## 17. Základy práce s daty v Pandas

**Balík Pandas**
- Knihovna pro práci s tabulkovými daty postavená nad NumPy; základ datové analýzy.

**`Series`**
- Jednorozměrná pojmenovaná datová struktura (hodnoty + index).
```python
s = pd.Series(range(5), index=["a","b","c","d","e"])
```
- Operace probíhají **podle indexu** (alignment); chybějící hodnoty → `NaN`.

**Role indexu**
- Index pojmenovává řádky a řídí zarovnání při operacích a výběru.

**`DataFrame`**
- Dvourozměrná tabulka (sloupce mohou mít různý typ), každý sloupec je `Series`.

**Práce se sloupci a řádky**
- `df["one"]` – sloupec (Series), `df[["one","two"]]` – více sloupců.
- `df.loc["a"]` – řádek podle indexu, `df.iloc[2:]` – podle pořadí.

**Výběr dat / maskování**
```python
df[df["two"] > 2]              # boolean maskování
```

**Explorace dat**
- `df.head()`, `df.tail()`, `df.describe()` (souhrnné statistiky), `df.groupby(...).agg(...)`.

---

## 18. Základy vizualizace dat pomocí Matplotlib

**Základní princip**
- Knihovna pro kreslení grafů. Nejjednodušší použití přes `pyplot`:
```python
plt.plot(x, y, label="sin(x)")
plt.xlabel("x"); plt.ylabel("y"); plt.title("sinus")
plt.legend(); plt.show()
```

**Figure vs. Axes**
- *Figure* je celé „plátno“ (okno/obrázek), *Axes* je jeden konkrétní graf (souřadnicový systém) uvnitř figure. Více grafů přes `fig, (ax1, ax2) = plt.subplots(1, 2)`.

**Popisky, legenda, velikost**
- `set_xlabel/ylabel/title`, `legend()` (popisky sérií), `figsize=(š, v)` určuje velikost; uložení `fig.savefig("graf.jpg", dpi=300)`.

**Colormap**
- Mapování hodnot na barvy (`plt.get_cmap("viridis")`); užitečné pro kódování další dimenze dat (např. barva bodů ve scatter plotu, `colorbar`).

**Sloupcový graf**
```python
plt.bar(strany, hlasy, color=barvy)
plt.ylabel("hlasy (tis.)"); plt.show()
```

---

## 19. Import v Pythonu

**Modul jako objekt a namespace**
- Modul je objekt typu `ModuleType` obsahující namespace (`__dict__`). Import = vytvoření a naplnění tohoto namespace. Modul `.py` je tedy objekt + namespace.

**Fáze importu `import foo.bar`**
1. **Kontrola cache** (`sys.modules`) – pokud už je načten, vrátí se rovnou.
2. **Nalezení specifikace** – finders v `sys.meta_path` vrací `ModuleSpec`.
3. **Vytvoření objektu modulu**.
4. **Načtení/spuštění** (loaders, `exec_module`) – proběhne top-level kód.
5. **Name binding** – svázání modulu se jménem.

**`sys.modules` a jednorázové spuštění**
- Cache mapuje jména modulů na načtené objekty. Díky ní je modul **singleton** a top-level kód proběhne maximálně jednou (výkon, zamezení opakovaných side-effects, průchod cyklickými importy). Proto někdy „musíme restartovat kernel“.

**`PathFinder` a `sys.path`**
- `PathFinder` prohledává lokace v `sys.path` (current working directory, instalované balíčky, standardní knihovna) a u balíčků `__path__`.

**`python file.py` vs. `python -m package.module`**
- `python file.py` spustí soubor jako hlavní skript.
- `python -m package.module` nejdřív najde modul přes import machinery a spustí ho jako `__main__` se **správným balíčkovým kontextem** (důležité pro relativní importy a `__package__`).

**Absolutní vs. relativní importy**
- *Absolutní*: `from mypkg.core import parser` (jméno zadané přímo).
- *Relativní*: `from . import utils` (dopočítává se z `__package__`). Selže, pokud Python nezná balíčkový kontext – relativní importy jsou svázány s tím, jak byl modul spuštěn.

*Doplňkově:* `if __name__ == "__main__":` odděluje kód pro import od kódu pro přímé spuštění; import spouští kód → může mít vedlejší efekty (proto by měl být „levný“).

---

## 20. Rekurze, iterace, memoizace a dynamické programování

**Princip rekurze**
- Funkce volá sama sebe dříve, než je dokončeno předchozí volání. Často dobře odpovídá matematickému popisu problému (problém se rozpadá na podproblémy stejného typu).

**Base case a rekurzivní krok**
- *Base case*: triviální případ ukončující rekurzi. *Rekurzivní krok*: řešení složí z dílčích výsledků (`ways(n) = ways(n-1) + ways(n-2)`).

**Časová a paměťová náročnost**
- Naivní rekurze (Fibonacci/schody) vytváří strom volání s **exponenciálním** počtem volání (opakované výpočty). Rekurze navíc spotřebovává **stack** (paměť).

**Head vs. tail rekurze**
- *Head*: nejdřív rekurzivní volání, pak práce. *Tail*: nejdřív práce, rekurze na konci (stav se předává jako akumulátor `acc`). Tail rekurzi lze vždy převést na cyklus.

**Memoizace a cache**
- Uložení výsledků mezivýpočtů a jejich opětovné použití. Neměníme definici problému, jen způsob provádění.
- `functools.lru_cache` jako hotové řešení:
```python
from functools import lru_cache
@lru_cache
def ways(n):
    if n <= 1: return 1
    return ways(n-1) + ways(n-2)
```

**Rekurze vs. iterace**
- Rekurze = *co* počítáme (struktura, implicitní stack); iterace = *jak* počítáme (explicitní stav, smyčka, lepší kontrola, efektivita).
- **Dynamické programování**: rozklad na opakující se podproblémy, každý spočítat jen jednou – top-down (rekurze + memoizace) nebo bottom-up (iterace/tabelizace).

---

## 21. Lazy evaluation, generátory a yield

**Lazy evaluation**
- Výpočet se odloží až do chvíle, kdy je výsledek skutečně potřeba.

**List comprehension vs. generator expression**
- `[2*x for x in range(N)]` spočítá a uloží **vše najednou** (paměťově náročné).
- `(2*x for x in range(N))` počítá hodnoty **postupně, na vyžádání** (líně).

**Generátor**
- Funkce, která místo jedné hodnoty produkuje sekvenci hodnot postupně. Vytváří se pomocí `yield`.
```python
def ways_seq():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b
```

**Co dělá `yield`**
- Mění funkci na generátor; kromě návratu hodnoty **pozastaví běh funkce**. Další `next()` pokračuje od stejného místa.

**Zachování stavu**
- Při pozastavení se uchovají **lokální proměnné i pozice v kódu**, takže výpočet plynule navazuje.

**Kdy generátor místo seznamu**
- Velké/nekonečné sekvence, streamované zpracování, kde nepotřebujeme vše v paměti najednou.

---

## 22. Higher-order funkce, closure a lambda funkce

**Funkce jsou objekty (first-class citizens)**
- V Pythonu jsou funkce běžné objekty – lze je ukládat do proměnných, předávat a vracet.

**Funkce jako argumenty / návratové hodnoty**
- Funkci lze předat jiné funkci jako parametr i ji vrátit jako výsledek.

**Higher-order function (HOF)**
- Funkce, která přijímá funkci jako parametr nebo funkci vrací. Umožňuje abstrahovat chování a oddělit logiku od řízení (např. `map`, dekorátory).

**Closure (uzávěr)**
- Funkce + **zachycené prostředí** (proměnné z místa svého vzniku). Funkce si „pamatuje“ kontext, i když okolí zanikne.
```python
def make_adder(a):
    def adder(x):
        return x + a      # 'a' je zachyceno v closure
    return adder
add5 = make_adder(5)
add5(10)  # 15
```
- Technicky: `add5.__closure__` obsahuje cell objects se zachycenými proměnnými. Closure umožňuje návrat funkcí, dekorátory a zapouzdření stavu bez tříd.

**Lambda funkce**
- Anonymní funkce s krátkým zápisem, vhodná pro jednoduché jednorázové operace:
```python
squared = list(map(lambda x: x*x, [1, 2, 3, 4]))
```

---

## 23. Unit testy a testovatelný kód

**Unit vs. integrační vs. end-to-end testy**
- *Unit*: testování nejmenších izolovaných jednotek (funkce, třída). Nejlevnější a nejrychlejší.
- *Integrační*: ověření, že komponenty fungují dohromady.
- *End-to-end*: kontrola aplikace od začátku do konce. (Dále performance a functional testing.)

**Motivace unit testů**
- Ověřují funkčnost po změnách, dávají jistotu při refactoringu, slouží jako dokumentace očekávaného chování.

**Testy jako dokumentace**
- Z testů je vidět, jak se kód má používat a co od něj očekávat.

**Testovatelný kód**
- Kód, který lze snadno testovat. Principy:
  - *Separation of responsibilities* – jedna funkce, jeden účel.
  - *Explicit dependencies* – závislosti předané explicitně (parametry).
  - *Dependency injection* – předávání collaborátorů místo jejich vytváření uvnitř.
  - *Pure functions* – bez side effects, deterministické (stejný vstup → stejný výstup).
  - Minimum skrytého globálního stavu a I/O uvnitř logiky; **vracení hodnot místo `print`**.

**Čisté funkce a side effects**
- Čistá funkce nezávisí na vnějším stavu (čas, I/O) a nemění ho; špatně testovatelná funkce míchá I/O, magic constants a skryté závislosti (vede k *flaky tests*).

**Dependency injection**
```python
def final_price(base, tax=0.21):   # místo input()/print() uvnitř
    return base * (1 + tax)
```

**Oddělení výpočtu od I/O/UI** – jádro (výpočet) nemá volat `input()`/`print()`, číst soubory ani síť; to umožňuje testovat čistou logiku bez patchování okolí.

---

## 24. Modul `unittest`, mocking, patching a TDD

**Struktura testu**
- Test case = potomek `unittest.TestCase`; metody s prefixem `test_` jsou jednotlivé testy.
```python
import unittest
class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
```

**TestCase, testovací metody, assertions**
- Assertions: `assertEqual`, `assertAlmostEqual` (floaty), `assertTrue`, `assertRaises`, `subTest` (parametrizace). Čtyři koncepty: *test fixture, test case, test suite, test runner*.

**Test discovery a organizace**
- Testy ve složce `tests/` vedle balíčku, soubory s prefixem `test_` (obvykle jeden na modul). Spuštění `python3 -m unittest` (případně `-v`): proběhne discovery → sestaví TestSuite → TestRunner spustí.

**`setUp` a `tearDown`**
- `setUp`/`tearDown` se spouští před/po každém testu (příprava dat), `setUpClass`/`tearDownClass` jednou pro celý TestCase.

**Mocking a patching**
- *Mocking*: nahrazení objektu falešným (`Mock`) → izolované testování, nezávislé na side effects skutečného objektu. Lze kontrolovat volání (`assert_called_once_with`), nastavit `return_value`/`side_effect`.
- *Patching*: dynamické podstrčení mocku za skutečný objekt (`@patch("math.sqrt")` nebo `with patch(...)`).
```python
from unittest.mock import Mock
db = Mock()
db.load_user.return_value = {"name": "alice"}
service = UserService(db)            # dependency injection + mock
```

**TDD a cyklus red-green-refactor**
1. Napiš test, 2. nech ho selhat (**red**), 3. napiš minimum kódu, aby prošel (**green**), 4. **refactor**, 5. opakuj.
- TDD používá test jako nástroj návrhu, ne jen jako kontrolu po dopsání.

---

## 25. Uživatelská rozhraní a obecná struktura interaktivního programu

**Uživatelské rozhraní**
- Vrstva, přes kterou uživatel program ovládá – přijímá vstupy a poskytuje zpětnou vazbu. Typy: CLI, TUI, GUI, webové.

**Jednorázový skript vs. interaktivní program**
- *Skript*: načti data → zpracuj → vypiš → skonči.
- *Interaktivní program*: inicializuj stav → čekej na akce → reaguj na události → opakuj.

**Obecná struktura interaktivního programu**
```python
running = True
while running:
    event = get_event()      # získání vstupu/události
    handle_event(event)      # reakce na událost
    update_state()           # úprava vnitřního stavu
    render()                 # vykreslení aktuálního stavu
```

**Klíčové pojmy**
- *Hlavní smyčka* (main loop) – cyklus zpracovávající události.
- *Událost* – informace, že se něco stalo.
- *Obsluha události* (handler) – reakce na konkrétní událost.
- *Stav programu* – vnitřní data, která se mezi událostmi udržují.

**Příklady událostí** – stisk klávesy, kliknutí myší, příchozí zpráva, vypršení časovače, volba položky menu.

---

## 26. CLI, argparse a automatizace

**Command line interface (CLI)**
- Rozhraní založené na spuštění programu z příkazové řádky (jméno programu, argumenty, přepínače, případně stdin).

**Poziční argumenty, volitelné argumenty, přepínače**
- *Poziční*: obvykle hlavní objekt operace (vstupní soubor).
- *Volitelné*: mění chování (`-o/--output`).
- *Přepínač*: volitelný argument bez hodnoty (`action="store_true"`).

**Zásady návrhu dobrého CLI**
- Snadná spustitelnost bez zbytečných voleb; povinné argumenty jen kde dávají smysl; krátké přepínače pro časté a delší čitelné pro méně časté použití; výstižné názvy; srozumitelná nápověda a chybová hlášení.

**`argparse`**
```python
import argparse
parser = argparse.ArgumentParser(description="...")
parser.add_argument("input_file")
parser.add_argument("-o", "--output", default="out.txt")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("--count", type=int, default=10)
parser.add_argument("--mode", choices=["fast", "safe"])
args = parser.parse_args()
```
- Řeší poziční/volitelné argumenty, typy, výchozí hodnoty, omezení (`choices`), automatickou nápovědu (`--help`) a kontrolu chyb.

**Proč je CLI vhodné pro automatizaci**
- CLI program často nepoužívá člověk, ale je součástí řetězce nástrojů: vstup/výstup přes soubory a streamy, **pipes** a přesměrování (`cat data | python analyze.py`, `> output.txt`). Funguje jako stavební kámen většího workflow.

**CLI vs. TUI vs. GUI**
- *CLI*: jednoduché, skriptovatelné, dobře automatizovatelné.
- *TUI*: stále terminál, ale interaktivnější a bohatší (menu, okna, klávesové zkratky); modul **`cmd`** umožňuje rychle vytvořit jednoduché REPL shellové rozhraní.
- *GUI*: nejpohodlnější pro běžného uživatele, ale složitější na vývoj. Pojmy: **widget** (prvek), **layout** (rozmístění), **callback** (funkce volaná při události), **mainloop** (smyčka zpracovávající události). Knihovny: tkinter, PyQt/PySide, NiceGUI.

---

## 27. Základní koncepty architektury

**Separation of concerns**
- Každá část programu má jasnou roli (vstup, validace, výpočet, formátování, ukládání, logování). Čím více rolí má jedna funkce, tím hůř se mění a testuje.

**Cohesion a coupling**
- *Cohesion*: věci patřící k sobě jsou spolu, modul má jeden jasný účel (chceme **vysokou**).
- *Coupling*: míra závislosti mezi částmi (chceme **nízký**). Směr závislostí: vnější vrstvy závisí na vnitřních, jádro nezná UI/DB/formát.

**Běžný vs. diagnostický výstup**
- *stdout*: normální datový výstup (pro další program). *stderr*: chyby a diagnostika (pro člověka/logy). Lze je oddělit přesměrováním.

**`print` vs. `logging`**
- `print` je výstup programu, ale na diagnostiku slabý (nemá úrovně, špatně se filtruje, znečišťuje stdout).
- `logging` má úrovně: **DEBUG** (detail pro vývojáře), **INFO** (běžný průběh), **WARNING** (zvládnutá nečekaná situace), **ERROR** (operace selhala), **CRITICAL** (program nemůže pokračovat).

**MVC architektura**
- *Model*: data a pravidla. *View*: prezentace výsledků. *Controller*: přijímá vstup a volá správné operace. (V CLI: View = textový výstup, Controller = parsování argumentů.) Doplňkově: vrstvená architektura (UI → application → domain → infrastructure), ports & adapters.

**Dependency injection**
```python
def save_report(text, output):    # závislost (kam zapsat) předaná zvenku
    output.write(text)
```
- Závislost se předává zvenku (parametrem), ne natvrdo uvnitř → snadnější testování, nižší coupling, výměna implementace (soubor/`StringIO`/socket). Chyby z modelu hlásíme výjimkami; konfiguraci předáváme dovnitř.

---

## 28. Serializace dat a objektů v Pythonu

**Serializace a deserializace**
- *Serializace*: převod objektu/datové struktury do podoby, kterou lze uložit nebo přenést (text/bytes → soubor/síť/DB). *Deserializace*: opačný proces. Důvody: perzistence, komunikace (API), cache, reprodukovatelnost, ladění.

**Problémy při ukládání objektů**
- Objekt má identitu, invarianty, reference na jiné objekty, cache, vnější zdroje. Musíme rozhodnout, **co je skutečný stav objektu**. Naivní `obj.__dict__` je křehké (nemusí existovat – `__slots__`, ukládá implementační detail, přejmenování atributu rozbije stará data).

**JSON: co umí a co ne**
- JSON umí: objekt/slovník, pole, řetězec, číslo, `true`/`false`, `null`.
- JSON neumí přímo: vlastní třídy, množiny, funkce, otevřené soubory, NumPy pole, datum/čas (bez konverze), sdílené reference a cykly.
- (+) čitelný, jazykově nezávislý, vhodný pro konfigurace a API.

**Jak pomůže `dataclass`**
- `@dataclass` je vhodná pro objekty nesoucí data; `asdict()` převede (i vnořené) dataclass na slovník. Doporučený explicitní protokol `to_dict` / `from_dict` (alternativní konstruktor, prostor pro validaci a migraci verzí):
```python
@dataclass
class Geometry:
    R: float
    theta: float
    def to_dict(self): return {"R": self.R, "theta": self.theta}
    @classmethod
    def from_dict(cls, data): return cls(R=data["R"], theta=data["theta"])
```

**`pickle` – výhody a nevýhody**
- Standardní modul pro serializaci Python objektů; uloží mnoho objektů bez ručního převodu (binární, Python-specifický formát).
- (+) rychlá interní cache, dočasné mezivýsledky, komunikace mezi Python procesy.
- (−) není jazykově nezávislý, nevhodný jako veřejný formát a pro archivaci, rozbije se při přejmenování třídy/modulu, nečitelný.

**Bezpečnostní problém `pickle`**
- **Deserializace `pickle.load` může spustit libovolný kód.** Nikdy nenačítejte pickle z nedůvěryhodného zdroje (uživatel, internet, veřejné API) – použijte bezpečnější formát (např. JSON, který neobnovuje libovolné objekty).

**Obtížné případy** – sdílené reference a cykly (řeší se ID a odkazy + verzování formátu), vnější zdroje (ukládejte informaci k obnovení, ne živý zdroj).

**Pravidlo** – serializujte raději **data než živé objekty**; pro dlouhodobá data navrhněte explicitní formát s verzí. Nejdřív navrhněte data, až potom ukládání objektů.

---

*Konec okruhů.*