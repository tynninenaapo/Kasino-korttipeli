from kortti import Kortti
from pelaaja import Pelaaja
from poyta import Poyta

MAAT = ["Pata", "Risti", "Ruutu", "Hertta"]

# Luokka, joka tuo muut pelissä tarvittavat luokat yhteen
class Peli:

    # Alustaaa Peli-olion
    def __init__(self, poyta):
        self.pelaajat = []      # Lista Pelaaja-olioita
        self.poyta = poyta

    # Lisää pelaajan pelaajalistaan
    def lisaa_pelaaja(self, pelaaja):
        self.pelaajat.append(pelaaja)

    # Luo 52 kortin korttipakan
    def luo_pakka(self):
        for alkio1 in MAAT:
            for alkio2 in range(1, 14):
                kortti = Kortti(alkio1, alkio2)
                self.poyta.lisaa_kortti_pakkaan(kortti)
