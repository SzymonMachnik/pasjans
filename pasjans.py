from colorama import init, Fore
init(autoreset=True)  # automatyczne resetowanie kolorów po każdej linii

import random

kolory = ["kier", "karo", "pik", "trefl"]
wartosci = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "W", "D", "K"]

class Karta:
    ikony = {"kier" : "♥", 
             "karo" : "♦",
             "pik" : "♠",
             "trefl" : "♣"}

    def __init__(self, kolor, wartosc):
        self.kolor = kolor
        self.wartosc = wartosc

    def pokaz_karte(self):
        if (self.kolor == "kier" or self.kolor == "karo"):
            print(Fore.RED + f"{self.ikony[self.kolor]} {self.wartosc}", end="")
        else:
            print(Fore.WHITE + f"{self.ikony[self.kolor]} {self.wartosc}", end="")
        
class Talia:


    def __init__(self):
        self.karty = [Karta(kolor, wartosc) for kolor in kolory for wartosc in wartosci]
        random.shuffle(self.karty)

    def pokaz_talie(self):
        for karta in self.karty:
            karta.pokaz_karte()

class StosRezerwowy:  
    def __init__(self, karty):
        self.karty = karty
        self.indeks = 0

    def pokaz_stos_rezerwowy(self):
        # for karta in self.karty:
        #     karta.pokaz_karte()
        self.karty[self.indeks].pokaz_karte()
        print("\n")

    def zwroc_pierwsza_karte(self):
        return self.karty[self.indeks]
    
    def przewin(self):
        self.indeks += 1
        if (self.indeks >= len(self.karty)):
            self.indeks = 0

    def usun_karte(self):
        self.karty.pop(self.indeks)

class StosGlowny:
    def __init__(self, karty):
        self.kolumny = {"1" : [karty[0]],
                        "2" : karty[1:3],
                        "3" : karty[3:6],
                        "4" : karty[6:10],
                        "5" : karty[10:15],
                        "6" : karty[15:21],
                        "7" : karty[21:]}
    
    def pokaz_stos_glowny(self):
        for kolumna in range(1, 8):
            for karta in self.kolumny[str(kolumna)]:
                karta.pokaz_karte()
            print("")
    
    def pokaz_stos_glowny2(self):
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
        kartaNaStosieGlownym = self.kolumny[kolumna][-1]
        if (kartaNaStosieGlownym.kolor == "kier" or kartaNaStosieGlownym.kolor == "karo"):
            if (nowaKarta.kolor == "kier" or nowaKarta.kolor == "karo"): return False
        else:
            if (nowaKarta.kolor == "pik" or nowaKarta.kolor == "trefl"): return False
        
        if (kartaNaStosieGlownym.wartosc == "A" or nowaKarta.wartosc == "K"): return False

        indeksWartosciKartyNaStosieGlownym = wartosci.index(kartaNaStosieGlownym.wartosc)
        if (nowaKarta.wartosc == wartosci[indeksWartosciKartyNaStosieGlownym - 1]): return True

        return False

    def dodaj_karte(self, karta, kolumna):
        self.kolumny[kolumna].append(karta)

def przeniesienie_karty_z_rezerwowego_do_glownego(kolumna):
    pierwsza_karta = stosRezerwowy.zwroc_pierwsza_karte()
    if (stosGlowny.czy_mozna_przeniesc_karte_do_kolumny(pierwsza_karta, kolumna)):
        # usun karte z rezerwowego
        stosRezerwowy.usun_karte()
        # dodaj do glownego
        stosGlowny.dodaj_karte(pierwsza_karta, kolumna)
        return True
    return False
   



class StosyKoncowe:
    def __init__(self):
        self.karo = []
        self.kier = []
        self.pik = []
        self.trefl = []


talia = Talia()
stosRezerwowy = StosRezerwowy(talia.karty[0:24])
stosGlowny = StosGlowny(talia.karty[24:])
stosRezerwowy.pokaz_stos_rezerwowy()
stosGlowny.pokaz_stos_glowny2()

aktualnaKarta = stosRezerwowy.zwroc_pierwsza_karte()

ruch = input("Ruch: ")
while (ruch != "q"):
    stosRezerwowy.przewin()
    stosRezerwowy.pokaz_stos_rezerwowy()
    stosGlowny.pokaz_stos_glowny2()


    for k in range(1, 8):
        przeniesienie_karty_z_rezerwowego_do_glownego(str(k))
    
    ruch = input("Ruch: ")