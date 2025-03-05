from kortti import Kortti

class Pelaaja:

    def __init__(self, nimi):
        self.nimi = nimi
        self.kasi = []
        self.pino = []
        self.mokit = 0
        self.pisteet = 0

    def lisaa_kortti_kateen(self, kortti):
        self.kasi.append(kortti)

    def lisaa_kortti_pinoon(self, kortti):
        self.pino.append(kortti)

    def poista_kortti_kadesta(self, kortti):
        self.pino.remove(kortti)

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
