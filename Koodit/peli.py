from kortti import Kortti
from pelaaja import Pelaaja
from poyta import Poyta
import random

MAAT = ["Pata", "Risti", "Ruutu", "Hertta"]


# Luokka, joka tuo muut pelissä tarvittavat luokat yhteen
class Peli:

    # Alustaaa Peli-olion
    def __init__(self):
        self.pelaajat = []      # Lista Pelaaja-olioita
        self.poyta = Poyta()

    # Lisää pelaajan pelaajalistaan
    def lisaa_pelaaja(self, pelaaja):
        self.pelaajat.append(pelaaja)

    # Luo 52 kortin korttipakan
    def luo_pakka(self):
        for alkio1 in MAAT:
            for alkio2 in range(1, 14):
                kortti = Kortti(alkio1, alkio2)
                self.poyta.lisaa_kortti_pakkaan(kortti)

    # Kirjoittaa pelitilanteen tiedostoon "pelitilanne.txt"
    def kirjoita_pelitilanne(self, indeksi):
        tiedosto = open("pelitilanne.txt", "w")
        if indeksi < 10:
            tiedosto.write("1")
        else:
            tiedosto.write("2")
        indeksi = f"{indeksi}"
        tiedosto.write(indeksi)
        for pelaaja in self.pelaajat:
            str = ""
            if len(pelaaja.hanki_nimi()) < 10:
                str += f"0{len(pelaaja.hanki_nimi())}{pelaaja.hanki_nimi()}"
            else:
                str += f"{len(pelaaja.hanki_nimi())}{pelaaja.hanki_nimi()}"
            if pelaaja.hanki_mokit() < 10:
                str += f"0{pelaaja.hanki_mokit()}"
            else:
                str += f"{pelaaja.hanki_mokit()}"
            if pelaaja.hanki_pisteet() < 10:
                str += f"0{pelaaja.hanki_pisteet()}"
            else:
                str += f"{pelaaja.hanki_pisteet()}"
            for kortti in pelaaja.hanki_kasi():
                if len(kortti.__str__()) < 10:
                    str += f"0{len(kortti.__str__())}{kortti.__str__()}"
                else:
                    str += f"{len(kortti.__str__())}{kortti.__str__()}"
            str += "99"
            for kortti in pelaaja.hanki_pino():
                if len(kortti.__str__()) < 10:
                    str += f"0{len(kortti.__str__())}{kortti.__str__()}"
                else:
                    str += f"{len(kortti.__str__())}{kortti.__str__()}"
            str += "99\n"
            tiedosto.write(str)
        str = "99"
        for kortti in self.poyta.pakka:
            if len(kortti.__str__()) < 10:
                str += f"0{len(kortti.__str__())}{kortti.__str__()}"
            else:
                str += f"{len(kortti.__str__())}{kortti.__str__()}"
        str += "99"
        for kortti in self.poyta.poydan_kortit:
            if len(kortti.__str__()) < 10:
                str += f"0{len(kortti.__str__())}{kortti.__str__()}"
            else:
                str += f"{len(kortti.__str__())}{kortti.__str__()}"
        str += "99"
        tiedosto.write(str)
        tiedosto.close()

    # Lukee pelitilanteen tiedostosta "pelitilanne.txt"
    def lue_pelitilanne(self):
        tiedosto = open("pelitilanne.txt", "r")
        kortit = ""
        indeksi_pituus = int(tiedosto.read(1))
        indeksi = int(tiedosto.read(indeksi_pituus))
        for rivi in tiedosto:
            i = 0
            rivi = rivi.rstrip()
            nimen_pituus = int(rivi[i:i + 2])
            i += 2
            if nimen_pituus == 99:
                kortit = rivi
                break
            nimi = rivi[i:i + nimen_pituus]
            i += nimen_pituus
            pelaaja = Pelaaja(nimi)
            self.pelaajat.append(pelaaja)
            mokit = int(rivi[i:i + 2])
            pelaaja.mokit = mokit
            i += 2
            pisteet = int(rivi[i:i + 2])
            pelaaja.pisteet = pisteet
            i += 2
            pituus = int(rivi[i:i + 2])
            i += 2
            while pituus != 99:
                str = rivi[i:i + pituus]
                i += pituus
                osat = str.split("-")
                if osat[0] == "Pata":
                    maa = "Pata"
                elif osat[0] == "Risti":
                    maa = "Risti"
                elif osat[0] == "Ruutu":
                    maa = "Ruutu"
                else:
                    maa = "Hertta"
                if osat[1] == "Assa":
                    arvo = 1
                elif osat[1] == "Kuningas":
                    arvo = 13
                elif osat[1] == "Kuningatar":
                    arvo = 12
                elif osat[1] == "Jatka":
                    arvo = 11
                else:
                    arvo = int(osat[1])
                kortti = Kortti(maa, arvo)
                pelaaja.lisaa_kortti_kateen(kortti)
                pituus = int(rivi[i:i + 2])
                i += 2
            pituus = int(rivi[i:i + 2])
            i += 2
            while pituus != 99:
                str = rivi[i:i + pituus]
                i += pituus
                osat = str.split("-")
                if osat[0] == "Pata":
                    maa = "Pata"
                elif osat[0] == "Risti":
                    maa = "Risti"
                elif osat[0] == "Ruutu":
                    maa = "Ruutu"
                else:
                    maa = "Hertta"
                if osat[1] == "Assa":
                    arvo = 1
                elif osat[1] == "Kuningas":
                    arvo = 13
                elif osat[1] == "Kuningatar":
                    arvo = 12
                elif osat[1] == "Jatka":
                    arvo = 11
                else:
                    arvo = int(osat[1])
                kortti = Kortti(maa, arvo)
                pelaaja.lisaa_kortti_pinoon(kortti)
                pituus = int(rivi[i:i + 2])
        i = 2
        pituus = int(kortit[i:i + 2])
        i += 2
        while pituus != 99:
            str = kortit[i:i + pituus]
            i += pituus
            osat = str.split("-")
            if osat[0] == "Pata":
                maa = "Pata"
            elif osat[0] == "Risti":
                maa = "Risti"
            elif osat[0] == "Ruutu":
                maa = "Ruutu"
            else:
                maa = "Hertta"
            if osat[1] == "Assa":
                arvo = 1
            elif osat[1] == "Kuningas":
                arvo = 13
            elif osat[1] == "Kuningatar":
                arvo = 12
            elif osat[1] == "Jatka":
                arvo = 11
            else:
                arvo = int(osat[1])
            kortti = Kortti(maa, arvo)
            self.poyta.lisaa_kortti_pakkaan(kortti)
            pituus = int(kortit[i:i + 2])
            i += 2
        pituus = int(kortit[i:i + 2])
        i += 2
        while pituus != 99:
            str = kortit[i:i + pituus]
            i += pituus
            osat = str.split("-")
            if osat[0] == "Pata":
                maa = "Pata"
            elif osat[0] == "Risti":
                maa = "Risti"
            elif osat[0] == "Ruutu":
                maa = "Ruutu"
            else:
                maa = "Hertta"
            if osat[1] == "Assa":
                arvo = 1
            elif osat[1] == "Kuningas":
                arvo = 13
            elif osat[1] == "Kuningatar":
                arvo = 12
            elif osat[1] == "Jatka":
                arvo = 11
            else:
                arvo = int(osat[1])
            kortti = Kortti(maa, arvo)
            self.poyta.lisaa_kortti_poytaan(kortti)
            pituus = int(kortit[i:i + 2])
            i += 2
        tiedosto.close()
        return indeksi

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
                    pelaaja.assat_pinossa += 1
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
        if type(eniten_kortteja) != tuple:
            eniten_kortteja.pisteet += 1
        else:
            for pelaaja in eniten_kortteja:
                pelaaja.pisteet += 1
        if type(eniten_patoja) != tuple:
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
            if len(self.poyta.poydan_kortit) == 0:
                pelaaja.mokit += 1
            nostettu_kortti = self.nosta_kortti(pelaaja)
            return True, nostettu_kortti
        else:
            return False, None


    # Pelaaja laittaa kortin pöytään
    def laita_kortti_poytaan(self, pelaaja, kortti):
        pelaaja.poista_kortti_kadesta(kortti)
        self.poyta.lisaa_kortti_poytaan(kortti)
        nostettu_kortti = self.nosta_kortti(pelaaja)
        return nostettu_kortti

    # Valitsee pakasta satunnaisen kortin ja lisää pelaajan käteen
    def nosta_kortti(self, pelaaja):
        if len(self.poyta.pakka) != 0:
            satunnainen_kortti = random.choice(self.poyta.pakka)
            pelaaja.lisaa_kortti_kateen(satunnainen_kortti)
            self.poyta.poista_kortti_pakasta(satunnainen_kortti)
            return satunnainen_kortti
        return None

    # Nollaa pelaajien tilastot uutta kierrosta varten
    def uusi_kierros(self):
        for pelaaja in self.pelaajat:
            pelaaja.kasi = []
            pelaaja.pino = []
            pelaaja.padat_pinossa = 0
            pelaaja.assat_pinossa = 0
            pelaaja.mokit = 0
        self.poyta.poydan_kortit = []
        self.poyta.pakka = []


    # Parametrina lista kortteja
    # Summaa korttien arvot pöydässä yhteen
    def summaa_kortit_poydassa(self, kortit):
        summa = 0
        for kortti in kortit:
            summa += kortti.hanki_arvo_poydassa()
        return summa



