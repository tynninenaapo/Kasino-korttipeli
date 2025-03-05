from kortti import Kortti

class Poyta:

    def __init__(self):
        self.poydan_kortit = []
        self.pakka = []

    def lisaa_kortti_poytaan(self, kortti):
        self.poydan_kortit.append(kortti)

    def poista_kortti_poydasta(self, kortti):
        self.poydan_kortit.remove(kortti)

    def poista_kortti_pakasta(self, kortti):
        self.pakka.remove(kortti)