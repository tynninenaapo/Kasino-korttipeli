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

    # Tarkistaa korttien laillisuuden
    # Jos kortit ovat lailliset, palauttaa True, muuten False
    # Pelattu_kortti on pelaajan käyttämä Kortti-olio
    # Valitut_kortit on lista pelaajan pöydästä valitsemia Kortti-olioita
    def tarkista_kortti(self, pelattu_kortti, valitut_kortit):
        # Tapaus, jossa valittuja kortteja on 1
        if len(valitut_kortit) == 1:
            if pelattu_kortti.hanki_arvo_kadessa() == valitut_kortit[0].hanki_arvo_poydassa():
                return True
            else:
                return False
        # Tapaus, jossa korttien summan arvo on pelatun kortin arvo
        if pelattu_kortti.hanki_arvo_kadessa() == self.summaa_kortit_poydassa(valitut_kortit):
            return True
        # Tapaus, jossa valitut kortit sisältävät useamman yhdistelmän, joiden arvo on pelatun kortin arvo
        for kortti in valitut_kortit:
            # Poistetaan listasta kortit, joiden arvo on sama kuin pelatulla kortilla
            if kortti.hanki_arvo_poydassa == pelattu_kortti.hanki_arvo_kadessa():
                valitut_kortit.remove(kortti)
        # Tarkistetaan jäljellä olevien summa
        if pelattu_kortti.hanki_arvo_kadessa() == self.summaa_kortit_poydassa(valitut_kortit):
            return True
        # Tarkistetaan onko jäljellä olevien summa pelatun kortin arvon monikerta
        if self.summaa_kortit_poydassa(valitut_kortit) % pelattu_kortti.hanki_arvo_kadessa() == 0:
            # Käydään läpi kaikki mahdolliset kombinaatiot:
            i = 1
            while i < len(valitut_kortit):
                j = 0
                while j < len(valitut_kortit) - i:
                    summa = self.summaa_kortit_poydassa(valitut_kortit[j : j + i])
                    if summa == pelattu_kortti.hanki_arvo_kadessa():
                        del valitut_kortit[j : j + i + 1]
                    j += 1
                i += 1

    # Pelaaja pelaa kortin
    def pelaa_kortti(self, pelaaja, pelattu_kortti, valitut_kortit):
        if self.tarkista_kortti(pelattu_kortti, valitut_kortit):
            pelaaja.poista_kortti_kadesta(pelattu_kortti)
            pelaaja.lisaa_kortti_pinoon(pelattu_kortti)
            for kortti in valitut_kortit:
                self.poyta.poista_kortti_poydasta(kortti)
                pelaaja.lisaa_kortti_pinoon(kortti)

    # Pelaaja laittaa kortin pöytään
    def laita_kortti_poytaan(self, pelaaja, kortti):
        pelaaja.poista_kortti_kadesta(kortti)
        self.poyta.lisaa_kortti_poytaan(kortti)

    # Parametrina lista kortteja
    # Summaa korttien arvot pöydässä yhteen
    def summaa_kortit_poydassa(self, kortit):
        summa = 0
        for kortti in kortit:
            summa += kortti.hanki_arvo_poydassa()
        return summa



