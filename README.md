# 🚗 Autókölcsönző Rendszer

Egyszerű Python alapú autókölcsönző alkalmazás, amely lehetővé teszi autók bérlését, bérlések lemondását és az aktív bérlések megtekintését.

## Projekt struktúra

```
autokolcsonzo/
├── auto.py           # Auto (absztrakt), Szemelyauto, Teherauto osztályok
├── berles.py         # Berles osztály
├── autokolcsonzo.py  # Autokolcsonzo osztály (fő üzleti logika)
├── main.py           # Belépési pont, CLI felhasználói interfész
└── README.md
```

## Futtatás

```bash
python main.py
```

> Python 3.8+ szükséges. Külső csomag nem szükséges.

## Funkciók

- **Autók listázása** – az összes autó és elérhetőségük
- **Bérlések listázása** – aktív bérlések megtekintése
- **Autó bérlése** – szabad autó foglalása egy napra
- **Bérlés lemondása** – meglévő bérlés törlése

## Induló adatok

A program indulásakor automatikusan betöltődik:
- 4 autó (3 személyautó + 1 teherautó)
- 4 aktív bérlés
