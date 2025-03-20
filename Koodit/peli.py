from kortti import Kortti
from pelaaja import Pelaaja
from poyta import Poyta
import random

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

    # Jakaa 4 korttia jokaiselle pelaajalle ja laittaa 4 korttia pöytään
    def jaa_kortit(self):
        for i in range(4 * (len(self.pelaajat) + 1)):
            satunnainen_kortti = random.choice(self.poyta.pakka)
            if i % (len(self.pelaajat) + 1) == len(self.pelaajat):
                self.poyta.lisaa_kortti_poytaan(satunnainen_kortti)
                self.poyta.poista_kortti_pakasta(satunnainen_kortti)
                continue
            self.pelaajat[i % (len(self.pelaajat) + 1)].lisaa_kortti_kateen(satunnainen_kortti)
            self.poyta.poista_kortti_pakasta(satunnainen_kortti)

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
            if kortti.hanki_arvo_poydassa() == pelattu_kortti.hanki_arvo_kadessa():
                valitut_kortit.remove(kortti)
        # Tarkistetaan jäljellä olevien summa
        if pelattu_kortti.hanki_arvo_kadessa() == self.summaa_kortit_poydassa(valitut_kortit):
            return True
        # Tarkistetaan onko jäljellä olevien summa pelatun kortin arvon monikerta
        if self.summaa_kortit_poydassa(valitut_kortit) % pelattu_kortti.hanki_arvo_kadessa() == 0:
            uusi_valitut_kortit = []
            # Käydään läpi kaikki mahdolliset osajoukot käyttäen bittitason operaatioita
            for maski in range(1, 2 ** len(valitut_kortit)):
                osajoukko = []
                summa = 0
                for i in range(0, len(valitut_kortit)):
                    if maski & (1 << i):
                        osajoukko.append(valitut_kortit[i])
                        summa += valitut_kortit[i].hanki_arvo_poydassa()
                if summa == pelattu_kortti.hanki_arvo_kadessa():
                    for kortti in osajoukko:
                        uusi_valitut_kortit.append(kortti)
            if set(valitut_kortit) == set(uusi_valitut_kortit):
                return True
        return False

    # Vertailee pelaajien korttipinoja ja antaa pisteitä sääntöjen mukaisesti
    def laske_pisteet(self):
        eniten_kortteja = self.pelaajat[0]
        eniten_patoja = self.pelaajat[0]
        for pelaaja in self.pelaajat:
            pelaaja.pisteet += pelaaja.hanki_mokit()
            pelaaja.mokit = 0
            for kortti in pelaaja.hanki_pino():
                if kortti.hanki_maa() == "Ruutu" and kortti.hanki_arvo_poydassa() == 10:
                    pelaaja.pisteet += 2
                if kortti.hanki_maa() == "Pata":
                    pelaaja.padat_pinossa += 1
                    if kortti.hanki_arvo_poydassa() == 2:
                        pelaaja.pisteet += 1
                if kortti.hanki_arvo_poydassa() == 1:
                    pelaaja.pisteet += 1
            if len(pelaaja.hanki_pino()) >= len(eniten_kortteja.hanki_pino()):
                if len(pelaaja.pino) == len(eniten_kortteja.pino) and not pelaaja == eniten_kortteja:
                    eniten_kortteja = pelaaja, eniten_kortteja
                else:
                    eniten_kortteja = pelaaja
            if pelaaja.padat_pinossa >= eniten_patoja.padat_pinossa:
                if pelaaja.padat_pinossa == eniten_patoja.padat_pinossa and not pelaaja == eniten_patoja:
                    eniten_patoja = pelaaja, eniten_patoja
                else:
                    eniten_patoja = pelaaja
        if len(eniten_kortteja) == 1:
            eniten_kortteja.pisteet += 1
        else:
            for pelaaja in eniten_kortteja:
                pelaaja.pisteet += 1
        if len(eniten_patoja) == 1:
            eniten_patoja.pisteet += 2
        else:
            for pelaaja in eniten_patoja:
                pelaaja.pisteet += 2

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



