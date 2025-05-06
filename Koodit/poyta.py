class Poyta:

    # Pöytä-olion alustus
    def __init__(self):
        self.poydan_kortit = []     # Lista pöydässä olevista Kortti-olioista
        self.pakka = []             # Lista pakassa olevista Kortti-olioista

    # Lisää kortin pöytään
    def lisaa_kortti_poytaan(self, kortti):
        self.poydan_kortit.append(kortti)

    # Poistaa kortin pöydästä
    def poista_kortti_poydasta(self, kortti):
        self.poydan_kortit.remove(kortti)

    # Lisää kortin pakkaan
    def lisaa_kortti_pakkaan(self, kortti):
        self.pakka.append(kortti)

    # Poistaa kortin pakasta
    def poista_kortti_pakasta(self, kortti):
        self.pakka.remove(kortti)
