from datetime import date
from auto import Auto


class Berles:
    """Az autóbérléshez szükséges osztály, amely egy autó bérlését egy napra tárolja."""

    _next_id = 1

    def __init__(self, auto: Auto, datum: date):
        self.__id = Berles._next_id
        Berles._next_id += 1
        self.__auto = auto
        self.__datum = datum
        self.__ar = auto.berleti_dij

    @property
    def id(self) -> int:
        return self.__id

    @property
    def auto(self) -> Auto:
        return self.__auto

    @property
    def datum(self) -> date:
        return self.__datum

    @property
    def ar(self) -> float:
        return self.__ar

    def __str__(self) -> str:
        return (f"Bérlés #{self.__id:03d} | {self.__auto.rendszam} ({self.__auto.tipus}) | "
                f"Dátum: {self.__datum.strftime('%Y.%m.%d')} | Ár: {self.__ar:,.0f} Ft")
