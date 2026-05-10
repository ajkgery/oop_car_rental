from datetime import date, timedelta
from autokolcsonzo import Autokolcsonzo
from auto import Szemelyauto, Teherauto


# ─────────────────────────────────────────────
#  ANSI színkódok
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    BG_BLUE    = "\033[44m"
    BG_CYAN    = "\033[46m"
    BG_BLACK   = "\033[40m"


# ─────────────────────────────────────────────
#  Segédfüggvények
# ─────────────────────────────────────────────
def fejlec(szoveg: str):
    szelesseg = 60
    print()
    print(f"{C.BG_BLUE}{C.WHITE}{C.BOLD}{'─' * szelesseg}{C.RESET}")
    print(f"{C.BG_BLUE}{C.WHITE}{C.BOLD}  {szoveg:<{szelesseg - 2}}{C.RESET}")
    print(f"{C.BG_BLUE}{C.WHITE}{C.BOLD}{'─' * szelesseg}{C.RESET}")


def siker(szoveg: str):
    print(f"\n{C.GREEN}{C.BOLD}  ✔  {szoveg}{C.RESET}")


def hiba(szoveg: str):
    print(f"\n{C.RED}{C.BOLD}  ✘  {szoveg}{C.RESET}")


def info(szoveg: str):
    print(f"{C.CYAN}  ▸  {szoveg}{C.RESET}")


def elvalaszto():
    print(f"{C.DIM}{'─' * 60}{C.RESET}")


def datum_beolvasas(prompt: str) -> date:
    """Dátum bekérése YYYY-MM-DD formátumban."""
    while True:
        szoveg = input(f"{C.YELLOW}  {prompt} (ÉÉÉÉ-HH-NN): {C.RESET}").strip()
        try:
            ev, ho, nap = szoveg.split("-")
            d = date(int(ev), int(ho), int(nap))
            return d
        except (ValueError, AttributeError):
            hiba("Érvénytelen dátumformátum. Próbáld újra (pl. 2026-05-15).")


def int_beolvasas(prompt: str) -> int:
    while True:
        try:
            return int(input(f"{C.YELLOW}  {prompt}: {C.RESET}").strip())
        except ValueError:
            hiba("Kérlek, számot adj meg.")


# ─────────────────────────────────────────────
#  Előre betöltött adatok
# ─────────────────────────────────────────────
def adatok_inicializalasa() -> Autokolcsonzo:
    kolcsonzo = Autokolcsonzo("BudaCar Autókölcsönző")

    # 3 autó
    a1 = Szemelyauto("ABC-123", "Toyota Corolla",   12_000, ulohelyek=5)
    a2 = Szemelyauto("XYZ-789", "BMW 3-as sorozat", 25_000, ulohelyek=5)
    a3 = Teherauto ("FGH-456", "Mercedes Sprinter", 35_000, teherbiras_tonna=3.5)

    for auto in [a1, a2, a3]:
        kolcsonzo.auto_hozzaadasa(auto)

    ma = date.today()

    # 4 bérlés (dátumok a jövőben, hogy érvényesek legyenek)
    kolcsonzo.auto_berlese("ABC-123", ma + timedelta(days=1))
    kolcsonzo.auto_berlese("XYZ-789", ma + timedelta(days=2))
    kolcsonzo.auto_berlese("FGH-456", ma + timedelta(days=3))

    # a 4. bérléshez visszaállítjuk ABC-123-at (különben foglalt lenne)
    # új szabad autót adunk a 4. bérléshez – tegyünk hozzá egy 4. autót átmenetileg
    a4 = Szemelyauto("DEF-321", "Volkswagen Golf", 14_000, ulohelyek=5)
    kolcsonzo.auto_hozzaadasa(a4)
    kolcsonzo.auto_berlese("DEF-321", ma + timedelta(days=1))

    return kolcsonzo


# ─────────────────────────────────────────────
#  Menü funkciók
# ─────────────────────────────────────────────
def autok_listazasa(kolcsonzo: Autokolcsonzo):
    fejlec("AUTÓK LISTÁJA")
    autok = kolcsonzo.autok_listazasa()
    if not autok:
        info("Nincs autó a rendszerben.")
        return
    for auto in autok:
        allapot_szin = C.GREEN if auto.elerheto else C.RED
        allapot = "✔ Szabad" if auto.elerheto else "✘ Foglalt"
        print(f"  {C.BOLD}{auto.rendszam}{C.RESET}  {C.DIM}|{C.RESET}  "
              f"{auto.tipus:<22} {C.DIM}|{C.RESET}  "
              f"{auto.berleti_dij:>10,.0f} Ft/nap  {C.DIM}|{C.RESET}  "
              f"{allapot_szin}{allapot}{C.RESET}  {C.DIM}[{auto.auto_tipus()}]{C.RESET}")


def berlesek_listazasa(kolcsonzo: Autokolcsonzo):
    fejlec("AKTÍV BÉRLÉSEK")
    berlesek = kolcsonzo.berlesek_listazasa()
    if not berlesek:
        info("Jelenleg nincs aktív bérlés.")
        return
    for b in berlesek:
        print(f"  {C.BOLD}#{b.id:03d}{C.RESET}  {C.DIM}|{C.RESET}  "
              f"{b.auto.rendszam}  {C.DIM}|{C.RESET}  "
              f"{b.auto.tipus:<22} {C.DIM}|{C.RESET}  "
              f"{b.datum.strftime('%Y.%m.%d')}  {C.DIM}|{C.RESET}  "
              f"{C.YELLOW}{b.ar:>10,.0f} Ft{C.RESET}")


def auto_berlese_menu(kolcsonzo: Autokolcsonzo):
    fejlec("AUTÓ BÉRLÉSE")
    elerheto = kolcsonzo.elerheto_autok()

    if not elerheto:
        info("Jelenleg nincs elérhető autó.")
        return

    info("Elérhető autók:")
    for auto in elerheto:
        print(f"    {C.BOLD}{auto.rendszam}{C.RESET}  –  {auto.tipus}  "
              f"({auto.berleti_dij:,.0f} Ft/nap)  [{auto.auto_tipus()}]")

    elvalaszto()
    rendszam = input(f"{C.YELLOW}  Rendszám: {C.RESET}").strip().upper()
    datum = datum_beolvasas("Bérlés dátuma")

    try:
        berles = kolcsonzo.auto_berlese(rendszam, datum)
        siker(f"Bérlés rögzítve! Azonosító: #{berles.id:03d}  |  Összeg: {berles.ar:,.0f} Ft")
    except ValueError as e:
        hiba(str(e))


def berles_lemondasa_menu(kolcsonzo: Autokolcsonzo):
    fejlec("BÉRLÉS LEMONDÁSA")
    berlesek = kolcsonzo.berlesek_listazasa()

    if not berlesek:
        info("Nincs lemondható bérlés.")
        return

    berlesek_listazasa(kolcsonzo)
    elvalaszto()
    berles_id = int_beolvasas("Lemondandó bérlés azonosítója (#)")

    try:
        kolcsonzo.berles_lemondasa(berles_id)
        siker(f"#{berles_id:03d} azonosítójú bérlés sikeresen lemondva.")
    except ValueError as e:
        hiba(str(e))


# ─────────────────────────────────────────────
#  Fő program
# ─────────────────────────────────────────────
def main():
    kolcsonzo = adatok_inicializalasa()

    # Üdvözlő képernyő
    print()
    print(f"{C.BG_BLACK}{C.CYAN}{C.BOLD}")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║          🚗  AUTÓKÖLCSÖNZŐ RENDSZER  🚗              ║")
    print("  ║                                                      ║")
    print(f"  ║  {C.WHITE}{kolcsonzo.nev:<52}{C.CYAN}║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(C.RESET)
    info("A rendszer inicializálva. 4 autó és 4 bérlés betöltve.")

    menu_elemek = {
        "1": ("Autók listázása",     autok_listazasa),
        "2": ("Bérlések listázása",  berlesek_listazasa),
        "3": ("Autó bérlése",        auto_berlese_menu),
        "4": ("Bérlés lemondása",    berles_lemondasa_menu),
        "0": ("Kilépés",             None),
    }

    while True:
        print()
        print(f"{C.BOLD}{C.WHITE}  FŐMENÜ{C.RESET}")
        elvalaszto()
        for k, (felirat, _) in menu_elemek.items():
            szin = C.RED if k == "0" else C.CYAN
            print(f"  {szin}{C.BOLD}[{k}]{C.RESET}  {felirat}")
        elvalaszto()

        valasztas = input(f"{C.YELLOW}  Választás: {C.RESET}").strip()

        if valasztas == "0":
            siker("Viszlát!")
            break
        elif valasztas in menu_elemek:
            _, func = menu_elemek[valasztas]
            func(kolcsonzo)
        else:
            hiba("Érvénytelen választás. Kérlek, 0–4 közötti számot adj meg.")


if __name__ == "__main__":
    main()
