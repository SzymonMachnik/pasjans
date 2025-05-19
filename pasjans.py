from colorama import init, Fore
init(autoreset=True)  # automatyczne resetowanie kolorów po każdej linii

from copy import deepcopy # do zapisywania stanu gry

import random # do tasowania kart

# Definicje kolorów i wartości kart
kolory = ["kier", "karo", "pik", "trefl"]
wartosci = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# Klasa reprezentująca pojedynczą kartę
class Karta:

    def __init__(self, kolor, wartosc):
        self.kolor = kolor
        self.wartosc = wartosc
        self.odwrocona = False # Zmienna określająca, czy karta jest odwrócona do wartością góry
        self.ikony = {"kier" : "♥", 
                      "karo" : "♦",
                      "pik" : "♠",
                      "trefl" : "♣"}

    def pokaz_karte(self):
        # Wyświetlenie karty: zakrytej lub odkrytej z kolorem
        if (self.odwrocona == False):
            print("XXX", end="")
            return
        if (self.czy_czerwona_karta()):
            print(Fore.RED + f"{self.ikony[self.kolor]} {self.wartosc}", end="")
        else:
            print(Fore.WHITE + f"{self.ikony[self.kolor]} {self.wartosc}", end="")
        
    def czy_czerwona_karta(self):
        # Sprawdzenie czy karta ma czerwony kolor
        return self.kolor in ["kier", "karo"]
        
# Klasa reprezentująca talię kart
class Talia:
    def __init__(self):
        # Tworzenie talii kart i tasowanie
        self.karty = [Karta(kolor, wartosc) for kolor in kolory for wartosc in wartosci]
        random.shuffle(self.karty)

# Klasa stosu rezerwowego (24 karty)
class StosRezerwowy:  
    def __init__(self, karty):
        self.karty = karty
        self.indeks = 0 # Indeks aktualnie wyświetlanej karty

        # Odkrywamy wszystkie karty w stosie rezerwowym
        for karta in karty:
            karta.odwrocona = True

    def pokaz_stos_rezerwowy(self):
        # Pokazuje aktualną kartę, resetuje indeks jeśli przekroczony
        if (self.indeks >= len(self.karty)):
            self.indeks = 0
            random.shuffle(self.karty)
        if (len(self.karty) > 0):
            self.karty[self.indeks].pokaz_karte()        

    def zwroc_pierwsza_karte(self):
        return self.karty[self.indeks]
    
    def przewin(self):
        self.indeks += 1

    def usun_karte(self):
        self.karty.pop(self.indeks)

# Klasa stosu głównego - 7 kolumn kart
class StosGlowny:
    def __init__(self, karty):
        # Tworzenie kolumn o rosnącej liczbie kart
        self.kolumny = {"1" : [karty[0]],
                        "2" : karty[1:3],
                        "3" : karty[3:6],
                        "4" : karty[6:10],
                        "5" : karty[10:15],
                        "6" : karty[15:21],
                        "7" : karty[21:]}
        
        # Odkrywamy ostatnią kartę w każdej kolumnie
        for kolumna in range(1, 8):
            self.kolumny[str(kolumna)][-1].odwrocona = True
    
    def pokaz_stos_glowny(self):
        # Wyświetla wszystkie kolumny
        maksymalna_liczba_kart_w_kolumnie = 0
        for kolumna in range(1, 8):
            if (len(self.kolumny[str(kolumna)]) > maksymalna_liczba_kart_w_kolumnie):
                maksymalna_liczba_kart_w_kolumnie = len(self.kolumny[str(kolumna)])

        for rzad in range(0, maksymalna_liczba_kart_w_kolumnie):
            for kolumna in range(1, 8):
                if (len(self.kolumny[str(kolumna)]) > rzad):
                    self.kolumny[str(kolumna)][rzad].pokaz_karte()
                print("\t", end="")
            print("")

    def czy_mozna_przeniesc_karte_do_kolumny(self, nowaKarta, kolumna):
        # Sprawdza, czy karta może być dodana na szczyt wybranej kolumny
        if (len(self.kolumny[kolumna]) == 0):
            if (nowaKarta.wartosc == "K"): return True
            else: return False
        kartaNaStosieGlownym = self.kolumny[kolumna][-1]

        # Sprawdzenie czy karty są innego koloru
        if (kartaNaStosieGlownym.czy_czerwona_karta() == nowaKarta.czy_czerwona_karta()): return False
        
        if (kartaNaStosieGlownym.wartosc == "A" or nowaKarta.wartosc == "K"): return False

        indeksWartosciKartyNaStosieGlownym = wartosci.index(kartaNaStosieGlownym.wartosc)
        if (nowaKarta.wartosc == wartosci[indeksWartosciKartyNaStosieGlownym - 1]): return True

        return False

    def dodaj_karte(self, karta, kolumna):
        self.kolumny[kolumna].append(karta)

    def usun_karte(self, kolumna):
        self.kolumny[kolumna].pop()
        self.odkryjOstatniaKarte(kolumna)

    def czy_mozna_zabrac(self, kolumnaBierz, iloscKart):
        # Sprawdza, czy można zabrać kartę z kolumny (czy jest ona odkryta)
        if (iloscKart > len(self.kolumny[kolumnaBierz]) or iloscKart <= 0): return False
        if (self.kolumny[kolumnaBierz][-iloscKart].odwrocona == False): return False
        return True

    def czy_mozna_przeniesc_karty_z_glownego_do_glownego(self, kolumnaBierz, kolumnaDodaj, iloscKart):
        if (self.czy_mozna_zabrac(kolumnaBierz, iloscKart) == False): return False
        ostatniaKartaDoBrania = self.kolumny[kolumnaBierz][-iloscKart]

        return self.czy_mozna_przeniesc_karte_do_kolumny(ostatniaKartaDoBrania, kolumnaDodaj)

    def odkryjOstatniaKarte(self, kolumna):
        if (len(self.kolumny[kolumna]) > 0):
            self.kolumny[kolumna][-1].odwrocona = True

    def przeniesienie_kart_z_glownego_do_glownego(self, kolumnaBierz, kolumnaDodaj, iloscKart):
        if (self.czy_mozna_przeniesc_karty_z_glownego_do_glownego(kolumnaBierz, kolumnaDodaj, iloscKart)):
            kartyDoPrzeniesienia = self.kolumny[kolumnaBierz][-iloscKart:]
            self.kolumny[kolumnaBierz] = self.kolumny[kolumnaBierz][:-iloscKart]
            self.odkryjOstatniaKarte(kolumnaBierz)
            self.kolumny[kolumnaDodaj].extend(kartyDoPrzeniesienia)
            return True
        return False

# Klasa stosów końcowych (cele gry)
class StosyKoncowe:
    def __init__(self):
        self.karo = []
        self.kier = []
        self.pik = []
        self.trefl = []

    def czy_mozna_przeniesc_karte(self, nowaKarta):
        # Sprawdza czy karta pasuje do stosu końcowego według koloru i wartości
        indeksWartosciKarty = wartosci.index(nowaKarta.wartosc)
        if (nowaKarta.kolor == "kier"):
            if (len(self.kier) == indeksWartosciKarty):
                return True
        elif (nowaKarta.kolor == "karo"):
            if (len(self.karo) == indeksWartosciKarty):
                return True
        elif (nowaKarta.kolor == "pik"):
            if (len(self.pik) == indeksWartosciKarty):
                return True
        else:
            if (len(self.trefl) == indeksWartosciKarty):
                return True
        return False
    
    def dodaj_karte(self, nowaKarta):
        if (nowaKarta.kolor == "kier"):
            self.kier.append(nowaKarta)
        elif (nowaKarta.kolor == "karo"):
            self.karo.append(nowaKarta)
        elif (nowaKarta.kolor == "pik"):
            self.pik.append(nowaKarta)
        else:
            self.trefl.append(nowaKarta)
    
    def pokaz_stosy_koncowe(self):
        # Wyświetla aktualne górne karty stosów końcowych
        print("\t\t\t", end="")
        for stos in [self.karo, self.kier, self.pik, self.trefl]:
            if stos:
                stos[-1].pokaz_karte()
            print("\t", end="")
        # print()

    def czy_wygrana(self):
        # Wygrana gdy każdy stos końcowy ma 13 kart
        return all(len(stos) == 13 for stos in [self.karo, self.kier, self.pik, self.trefl])

# Funkcje pomocnicze do przenoszenia kart pomiędzy stosami
def przeniesienie_karty_z_rezerwowego_do_glownego(kolumna):
    if (len(stosRezerwowy.karty) <= 0): return False
    pierwsza_karta = stosRezerwowy.zwroc_pierwsza_karte()
   
    if (stosGlowny.czy_mozna_przeniesc_karte_do_kolumny(pierwsza_karta, kolumna)):
        stosRezerwowy.usun_karte()
        stosGlowny.dodaj_karte(pierwsza_karta, kolumna)
        return True
    return False

def przeniesienie_karty_z_rezerwowego_do_koncowego():
    if (len(stosRezerwowy.karty) <= 0): return False
    pierwsza_karta = stosRezerwowy.zwroc_pierwsza_karte()
    if (stosyKoncowe.czy_mozna_przeniesc_karte(pierwsza_karta)):
        stosRezerwowy.usun_karte()
        stosyKoncowe.dodaj_karte(pierwsza_karta)
        return True
    return False 

def przeniesienie_karty_z_glownego_do_koncowego(kolumna):
    if (len(stosGlowny.kolumny[kolumna]) <= 0): return False
    nowa_karta = stosGlowny.kolumny[kolumna][-1]
    if (stosyKoncowe.czy_mozna_przeniesc_karte(nowa_karta)):
        stosGlowny.usun_karte(kolumna)
        stosyKoncowe.dodaj_karte(nowa_karta)
        return True
    return False 

# Klasa odpowiadająca za obsługę gry — wyświetlanie, zapisywanie stanu, cofanie ruchów
class ObslugaGry:
    def __init__(self):
        self.historia = [] # Lista przechowująca historię stanów gry (do cofania ruchów)

    # Wyświetla tytuł gry w formie ASCII art
    def wyswietl_tytul(self):
        print(r"""
    ██████╗  █████╗ ███████╗    ██╗ █████╗ ███╗   ██╗███████╗
    ██╔══██╗██╔══██╗██╔════╝    ██║██╔══██╗████╗  ██║██╔════╝
    ██████╔╝███████║███████╗    ██║███████║██╔██╗ ██║███████╗
    ██╔═══╝ ██╔══██║╚════██║    ██║██╔══██║██║╚██╗██║╚════██║
    ██║     ██║  ██║███████║██████║██║  ██║██║ ╚████║███████║
    ╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝""")

    # Wyświetla instrukcję sterowania grą
    def wyswietl_instrukcje(self):
        print(f"""
    I N S T R U K C J A   S T E R O W A N I A

    Ruchy ogólne:
        - p       >> Przewiń kartę w stosie rezerwowym
        - q       >> Zakończ grę
        - h       >> Wyświetl pomoc (tę instrukcję)

    Ruchy ze stosu rezerwowego:
        - rk      >> Przenieś kartę do stosu końcowego
        - rg X    >> Przenieś kartę do kolumny głównej X (1–7)

    Ruchy z kolumny głównej:
        - gk X    >> Przenieś kartę z kolumny głównej X do stosu końcowego

    Przenoszenie między kolumnami głównymi:
        - gg X Y Z  >> Przenieś Z kart z kolumny głównej X do Y

    Cel gry:
        Ułóż wszystkie karty w 4 stosach końcowych od Asa do Króla w odpowiednich kolorach.
    """)

    # Wyświetla aktualny stan gry: stos rezerwowy, końcowy i główny
    def wyswietl_stan_gry(self):
        self.wyswietl_przerwe()
        print("Stos rezerwowy (r)\tStosy końcowe (k)")
        stosRezerwowy.pokaz_stos_rezerwowy()
        stosyKoncowe.pokaz_stosy_koncowe()
        print("\n")
        print("Stos główny (g)")
        stosGlowny.pokaz_stos_glowny()

    # Wyświetla linię oddzielającą dla czytelności
    def wyswietl_przerwe(self):
        print("\n====================================================|\n")

    # Zapisuje obecny stan gry do historii (max. 3 poprzednie stany)
    def zapisz_stan(self):
        if len(self.historia) == 3:
            self.historia.pop(0)  # Usuwa najstarszy zapisany stan
        stan = (
            deepcopy(stosRezerwowy),
            deepcopy(stosGlowny),
            deepcopy(stosyKoncowe)
        )
        self.historia.append(stan)

    # Przywraca ostatni zapisany stan gry (cofnięcie ruchu)
    def cofnij_ruch(self):
        global stosRezerwowy, stosGlowny, stosyKoncowe
        if len(self.historia) == 0:
            print("Brak ruchów do cofnięcia.")
            return False
        ostatni_stan = self.historia.pop()
        stosRezerwowy, stosGlowny, stosyKoncowe = ostatni_stan
        return True
    
    # Wyświetla menu główne z decyzją użytkownika: nowa gra lub wyjście
    def wyswietl_menu_glowne(self):
        return input(f"""
    - n    >> Nowa gra
    - q    >> Zamknij grę
    
Decyzja: """).lower().strip()



# Główna pętla gry
if __name__ == "__main__":

    ruch = ""           # Ostatni wykonany ruch gracza
    gra = True          # Zmienna decydująca, czy gra trwa
    wygrana = False     # Zmienna wygranej
    decyzjaOGrze = ""   # Zmienna przechowująca decyzję użytkownika po zakończeniu rozgrywki
    
    while (gra):
        # Inicjalizacja nowej talii i rozłożenie kart
        talia = Talia()
        stosRezerwowy = StosRezerwowy(talia.karty[0:24])
        stosGlowny = StosGlowny(talia.karty[24:])
        stosyKoncowe = StosyKoncowe()
        obslugaGry = ObslugaGry()

        # Wyświetlenie tytułu i instrukcji na początku gry
        obslugaGry.wyswietl_tytul()
        obslugaGry.wyswietl_instrukcje()
        obslugaGry.wyswietl_stan_gry()

        # Pętla wykonująca się do zakończenia gry lub wygranej
        while (ruch != "q" and wygrana == False):
            ruch = input("Ruch: ").strip().lower()

            # Obsługa komendy 'p' – przewinięcie stosu rezerwowego
            if (ruch == "p"):
                obslugaGry.zapisz_stan()
                stosRezerwowy.przewin()
                obslugaGry.wyswietl_stan_gry()
                wygrana = stosyKoncowe.czy_wygrana()
            
            # Obsługa komendy 'rk' – przeniesienie karty do stosu końcowego
            elif (ruch == "rk"):
                obslugaGry.zapisz_stan()
                przeniesienie_karty_z_rezerwowego_do_koncowego()
                obslugaGry.wyswietl_stan_gry()
                wygrana = stosyKoncowe.czy_wygrana()

             # Obsługa komendy 'rg X' – z rezerwowego do głównego stosu X
            elif (len(ruch) == 4 and ruch[0:2] == "rg" and "1" <= ruch[3] and ruch[3] <= "7"):
                obslugaGry.zapisz_stan()
                przeniesienie_karty_z_rezerwowego_do_glownego(ruch[3])
                obslugaGry.wyswietl_stan_gry()
                wygrana = stosyKoncowe.czy_wygrana()

            # Obsługa komendy 'gk X' – z głównego X do końcowego
            elif (len(ruch) == 4 and ruch[0:2] == "gk" and "1" <= ruch[3] and ruch[3] <= "7"):
                obslugaGry.zapisz_stan()
                przeniesienie_karty_z_glownego_do_koncowego(ruch[3])
                obslugaGry.wyswietl_stan_gry()
                wygrana = stosyKoncowe.czy_wygrana()
            
            # Obsługa komendy 'gg X Y Z' – przeniesienie Z kart między kolumnami głównymi
            elif (len(ruch) >= 8 and ruch.startswith("gg") and ruch[3] in "1234567" and ruch[5] in "1234567"):
                try:
                    ilosc = int(ruch[7:])  # Liczba kart do przeniesienia
                    if 1 <= ilosc <= 13:
                        obslugaGry.zapisz_stan()
                        stosGlowny.przeniesienie_kart_z_glownego_do_glownego(ruch[3], ruch[5], ilosc)
                        obslugaGry.wyswietl_stan_gry()
                        wygrana = stosyKoncowe.czy_wygrana()
                except ValueError:
                    print("Nieprawidłowa liczba kart.")

            # Cofnięcie ruchu
            elif ruch == "c":
                if (obslugaGry.cofnij_ruch()):
                    obslugaGry.wyswietl_stan_gry()

            # Wyświetlenie instrukcji
            elif (ruch == "h"):
                obslugaGry.wyswietl_przerwe()
                obslugaGry.wyswietl_instrukcje()

            # Zakończenie gry
            elif (ruch == "q"):
                print("\nDOBRZE CI POSZŁO. SPRÓBUJ JESZCZE RAZ!")
            
            # Obsługa nieprawidłowego polecenia
            else:
                print("""Błędny ruch. Wybierz "h", aby wyświetlić instrukcję,""")


        # Komunikat po wygraniu gry
        if (wygrana):
            print("\tGRATULACJE WYGRAŁEŚ!!!")

        # Reset zmiennych stanu
        ruch = ""
        wygrana = False

        # Zapytanie użytkownika, czy chce rozpocząć nową grę, czy zamknąć grę
        while (decyzjaOGrze != "q" and decyzjaOGrze != "n"):
            decyzjaOGrze = obslugaGry.wyswietl_menu_glowne()
            
            if (decyzjaOGrze == "q"):
                gra = False
        
        decyzjaOGrze = ""
                