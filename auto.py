from abc import ABC, abstractmethod


class Auto(ABC):
    """Absztrakt osztály az autók alapvető attribútumainak definiálásához."""

    def __init__(self, rendszam: str, tipus: str, berleti_dij: float):
        self.__rendszam = rendszam
        self.__tipus = tipus
        self.__berleti_dij = berleti_dij
        self.__elerheto = True

    @property
    def rendszam(self) -> str:
        return self.__rendszam

    @property
    def tipus(self) -> str:
        return self.__tipus

    @property
    def berleti_dij(self) -> float:
        return self.__berleti_dij

    @berleti_dij.setter
    def berleti_dij(self, ertek: float):
        if ertek <= 0:
            raise ValueError("A bérleti díjnak pozitívnak kell lennie.")
        self.__berleti_dij = ertek

    @property
    def elerheto(self) -> bool:
        return self.__elerheto

    @elerheto.setter
    def elerheto(self, ertek: bool):
        self.__elerheto = ertek

    @abstractmethod
    def leiras(self) -> str:
        pass

    def __str__(self) -> str:
        allapot = "Elérhető" if self.__elerheto else "Bérelt"
        return (f"[{self.auto_tipus()}] {self.__rendszam} | {self.__tipus} | "
                f"{self.__berleti_dij:,.0f} Ft/nap | {allapot}")

    @abstractmethod
    def auto_tipus(self) -> str:
        pass


class Szemelyauto(Auto):
    """Személyautók specifikus attribútumait tartalmazó osztály."""

    def __init__(self, rendszam: str, tipus: str, berleti_dij: float, ulohelyek: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__ulohelyek = ulohelyek

    @property
    def ulohelyek(self) -> int:
        return self.__ulohelyek

    @ulohelyek.setter
    def ulohelyek(self, ertek: int):
        if ertek < 2 or ertek > 9:
            raise ValueError("Az ülőhelyek száma 2 és 9 között kell legyen.")
        self.__ulohelyek = ertek

    def auto_tipus(self) -> str:
        return "Személyautó"

    def leiras(self) -> str:
        return (f"Személyautó: {self.tipus} | Rendszám: {self.rendszam} | "
                f"Ülőhelyek: {self.__ulohelyek} | Díj: {self.berleti_dij:,.0f} Ft/nap")


class Teherauto(Auto):
    """Teherautók specifikus attribútumait tartalmazó osztály."""

    def __init__(self, rendszam: str, tipus: str, berleti_dij: float, teherbiras_tonna: float):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__teherbiras_tonna = teherbiras_tonna

    @property
    def teherbiras_tonna(self) -> float:
        return self.__teherbiras_tonna

    @teherbiras_tonna.setter
    def teherbiras_tonna(self, ertek: float):
        if ertek <= 0:
            raise ValueError("A teherbírásnak pozitívnak kell lennie.")
        self.__teherbiras_tonna = ertek

    def auto_tipus(self) -> str:
        return "Teherautó"

    def leiras(self) -> str:
        return (f"Teherautó: {self.tipus} | Rendszám: {self.rendszam} | "
                f"Teherbírás: {self.__teherbiras_tonna} t | Díj: {self.berleti_dij:,.0f} Ft/nap")
