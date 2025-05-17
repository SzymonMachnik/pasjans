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
        self.otwarta = False

    def pokaz_karte(self):
        if (self.otwarta == False):
            print("XXX", end="")
            return
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
        for karta in karty:
            karta.otwarta = True

    def pokaz_stos_rezerwowy(self):
        if (self.indeks >= len(self.karty)):
            self.indeks = 0
        if (len(self.karty) > 0):
            self.karty[self.indeks].pokaz_karte()
        else: print("\t", end="")
        

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
        
        for kolumna in range(1, 8):
            self.kolumny[str(kolumna)][-1].otwarta = True
    
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
        if (len(stosGlowny.kolumny[kolumna]) <= 0): return True
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

    def usun_karte(self, kolumna):
        self.kolumny[kolumna].pop()
        self.odkryjOstatniaKarte(kolumna)

    def czy_mozna_zabrac(self, kolumnaBierz, iloscKart):
        if (iloscKart > len(self.kolumny[kolumnaBierz]) or iloscKart <= 0): return False
        if (self.kolumny[kolumnaBierz][-iloscKart].otwarta == False): return False
        return True

    def czy_mozna_przeniesc_karty_z_glownego_do_glownego(self, kolumnaBierz, kolumnaDodaj, iloscKart):
        if (self.czy_mozna_zabrac(kolumnaBierz, iloscKart) == False): return False
        if (len(self.kolumny[kolumnaDodaj]) <= 0): return True
        pierwszaKartaNaKtoraDodaj = self.kolumny[kolumnaDodaj][-1]
        ostatniaKartaDoBrania = self.kolumny[kolumnaBierz][-iloscKart]
        # Czy kolor będzie przeciwny
        if (ostatniaKartaDoBrania.kolor == "kier" or ostatniaKartaDoBrania.kolor == "karo"):
            if (pierwszaKartaNaKtoraDodaj.kolor == "kier" or pierwszaKartaNaKtoraDodaj.kolor == "karo"): return False
        else:
            if (pierwszaKartaNaKtoraDodaj.kolor == "pik" or pierwszaKartaNaKtoraDodaj.kolor == "trefl"): return False
        
        if (pierwszaKartaNaKtoraDodaj.wartosc == "A" or ostatniaKartaDoBrania.wartosc == "K"): return False

        indeksWartosciPierwszejKartyNaKtoraDodaj = wartosci.index(pierwszaKartaNaKtoraDodaj.wartosc)
        if (ostatniaKartaDoBrania.wartosc == wartosci[indeksWartosciPierwszejKartyNaKtoraDodaj - 1]): return True

        return False

    def odkryjOstatniaKarte(self, kolumna):
        if (len(self.kolumny[kolumna]) > 0):
            self.kolumny[kolumna][-1].otwarta = True

    def przeniesienie_kart_z_glownego_do_glownego(self, kolumnaBierz, kolumnaDodaj, iloscKart):
        if (self.czy_mozna_przeniesc_karty_z_glownego_do_glownego(kolumnaBierz, kolumnaDodaj, iloscKart)):
            kartyDoPrzeniesienia = self.kolumny[kolumnaBierz][-iloscKart:]
            self.kolumny[kolumnaBierz] = self.kolumny[kolumnaBierz][:-iloscKart]
            self.odkryjOstatniaKarte(kolumnaBierz)
            self.kolumny[kolumnaDodaj].extend(kartyDoPrzeniesienia)
            return True
        return False

            




class StosyKoncowe:
    def __init__(self):
        self.karo = []
        self.kier = []
        self.pik = []
        self.trefl = []

    def czy_mozna_przeniesc_karte(self, nowaKarta):
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
        print("\t\t\t", end="")
        if (len(self.karo)):
            self.karo[-1].pokaz_karte()
        print("\t", end="")
        if (len(self.kier)):
            self.kier[-1].pokaz_karte()
        print("\t", end="")
        if (len(self.pik)):
            self.pik[-1].pokaz_karte()
        print("\t", end="")
        if (len(self.trefl)):
            self.trefl[-1].pokaz_karte()
        print("\t", end="")


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
    if (len(stosRezerwowy.karty) <= 0): return False
    if (len(stosGlowny.kolumny[kolumna]) <= 0): return False
    nowa_karta = stosGlowny.kolumny[kolumna][-1]
    if (stosyKoncowe.czy_mozna_przeniesc_karte(nowa_karta)):
        stosGlowny.usun_karte(kolumna)
        stosyKoncowe.dodaj_karte(nowa_karta)
        return True
    return False 
    


talia = Talia()
stosRezerwowy = StosRezerwowy(talia.karty[0:24])
stosGlowny = StosGlowny(talia.karty[24:])
stosyKoncowe = StosyKoncowe()
stosRezerwowy.pokaz_stos_rezerwowy()
stosyKoncowe.pokaz_stosy_koncowe()
print("\n")
stosGlowny.pokaz_stos_glowny2()

aktualnaKarta = stosRezerwowy.zwroc_pierwsza_karte()

ruch = ""
while (ruch != "q"):
    ruch = input("Ruch: ")

    if (ruch == "p"):
        stosRezerwowy.przewin()
    elif (ruch == "rk"):
        przeniesienie_karty_z_rezerwowego_do_koncowego()
    elif (len(ruch) == 4 and ruch[0:2] == "rg" and "1" <= ruch[3] and ruch[3] <= "7"):
        przeniesienie_karty_z_rezerwowego_do_glownego(ruch[3])
    elif (len(ruch) == 4 and ruch[0:2] == "gk" and "1" <= ruch[3] and ruch[3] <= "7"):
        przeniesienie_karty_z_glownego_do_koncowego(ruch[3]) 
    #gg 6 7 2
    elif ruch.startswith("gg") and ruch[3] in "1234567" and ruch[5] in "1234567":
        try:
            ilosc = int(ruch[7:])  # od znaku 7 do końca
            if 1 <= ilosc <= 13:
                stosGlowny.przeniesienie_kart_z_glownego_do_glownego(ruch[3], ruch[5], ilosc)
        except ValueError:
            print("Nieprawidłowa liczba kart.")

    stosRezerwowy.pokaz_stos_rezerwowy()
    stosyKoncowe.pokaz_stosy_koncowe()
    print("\n")
    stosGlowny.pokaz_stos_glowny2()
    