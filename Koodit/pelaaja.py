from kortti import Kortti

class Pelaaja:

    # Pelaaja-olion alustus
    def __init__(self, nimi):
        self.nimi = nimi    # Pelaajan nimi
        self.kasi = []      # Lista pelaajan kädessä olevia Kortti-olioita
        self.pino = []      # Lista pelaajan kierroksen aikana keräämiä Kortti-olioita
        self.mokit = 0      # Pelaajan mökit (kokonaislukuarvo)
        self.pisteet = 0    # Pelaajan pisteet (kokonaislukuarvo)
        self.padat_pinossa = 0      # Patakortit pelaajan pinossa pistelaskua varten (kokonaislukuarvo)
        self.assat_pinossa = 0      # Ässät pinossa pistelaskua varten (kokonaislukuarvo)

    # Lisää kortin pelaajan käteen
    def lisaa_kortti_kateen(self, kortti):
        self.kasi.append(kortti)

    # Lisää kortin pelaajan pinoon
    def lisaa_kortti_pinoon(self, kortti):
        self.pino.append(kortti)

    # Poistaa kortin pelaajan kädestä
    def poista_kortti_kadesta(self, kortti):
        self.kasi.remove(kortti)

    def hanki_nimi(self):
        return self.nimi

    def hanki_kasi(self):
        return self.kasi

    def hanki_pino(self):
        return self.pino

    def hanki_mokit(self):
        return self.mokit

    def hanki_pisteet(self):
        return self.pisteet
