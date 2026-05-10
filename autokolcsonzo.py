from datetime import date
from typing import List, Optional
from auto import Auto
from berles import Berles


class Autokolcsonzo:
    """Autókölcsönző osztály, amely tartalmazza az autókat és bérléseket."""

    def __init__(self, nev: str):
        self.__nev = nev
        self.__autok: List[Auto] = []
        self.__berlesek: List[Berles] = []

    @property
    def nev(self) -> str:
        return self.__nev

    @nev.setter
    def nev(self, ertek: str):
        if not ertek or not ertek.strip():
            raise ValueError("A kölcsönző neve nem lehet üres.")
        self.__nev = ertek.strip()

    def auto_hozzaadasa(self, auto: Auto):
        """Autó hozzáadása a kölcsönzőhöz."""
        if any(a.rendszam == auto.rendszam for a in self.__autok):
            raise ValueError(f"Az autó ezzel a rendszámmal már szerepel: {auto.rendszam}")
        self.__autok.append(auto)

    def auto_berlese(self, rendszam: str, datum: date) -> Berles:
        """
        Autó bérlése egy napra.
        Visszaadja a bérlés objektumot (benne az árral).
        """
        if datum < date.today():
            raise ValueError("A bérlési dátum nem lehet múltbeli.")

        auto = self.__auto_keresese(rendszam)
        if auto is None:
            raise ValueError(f"Nem található autó ezzel a rendszámmal: {rendszam}")

        if not auto.elerheto:
            raise ValueError(f"Az autó ({rendszam}) jelenleg nem elérhető bérlésre.")

        # Ellenőrizzük, hogy arra a napra nincs-e már bérlés
        for b in self.__berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                raise ValueError(f"Ez az autó ({rendszam}) már foglalt erre a dátumra: {datum.strftime('%Y.%m.%d')}")

        auto.elerheto = False
        uj_berles = Berles(auto, datum)
        self.__berlesek.append(uj_berles)
        return uj_berles

    def berles_lemondasa(self, berles_id: int) -> bool:
        """
        Bérlés lemondása ID alapján.
        Visszaadja True-t, ha sikeres volt.
        """
        berles = self.__berles_keresese(berles_id)
        if berles is None:
            raise ValueError(f"Nem található bérlés ezzel az azonosítóval: {berles_id}")

        berles.auto.elerheto = True
        self.__berlesek.remove(berles)
        return True

    def berlesek_listazasa(self) -> List[Berles]:
        """Visszaadja az összes aktuális bérlés listáját."""
        return list(self.__berlesek)

    def autok_listazasa(self) -> List[Auto]:
        """Visszaadja az összes autó listáját."""
        return list(self.__autok)

    def elerheto_autok(self) -> List[Auto]:
        """Visszaadja az elérhető (szabad) autók listáját."""
        return [a for a in self.__autok if a.elerheto]

    def __auto_keresese(self, rendszam: str) -> Optional[Auto]:
        for auto in self.__autok:
            if auto.rendszam == rendszam:
                return auto
        return None

    def __berles_keresese(self, berles_id: int) -> Optional[Berles]:
        for berles in self.__berlesek:
            if berles.id == berles_id:
                return berles
        return None

    def __str__(self) -> str:
        return (f"Autókölcsönző: {self.__nev} | "
                f"Autók: {len(self.__autok)} | "
                f"Aktív bérlések: {len(self.__berlesek)}")
