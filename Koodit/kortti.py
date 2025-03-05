ASSA_KADESSA = 14
PATA2_KADESSA = 15
RUUTU10_KADESSA = 16

class Kortti:

    # Kortti-olion alustus
    def __init__(self, maa, arvo):
        self.maa = maa  # Pata, Risti, Ruutu tai Hertta
        self.arvo_kadessa = self.aseta_arvo_kadessa(maa, arvo)  # Kokonaislukuarvo 2-16
        self.arvo_poydassa = arvo  # Kokonaislukuarvo 1-13
        self.nimi = self.aseta_nimi(arvo)  # Numerokorteilla oma arvo merkkijonona
        # ja kuvakorteilla omansa

    # Erikoiskorttien arvon asettaminen
    def aseta_arvo_kadessa(self, maa, arvo):
        if arvo == 1:
            return ASSA_KADESSA
        if arvo == 2 and maa == "Pata":
            return PATA2_KADESSA
        if arvo == 10 and maa == "Ruutu":
            return RUUTU10_KADESSA
        return arvo

    # Nimen asettaminen
    def aseta_nimi(self, arvo):
        if arvo == 1:
            return "Ässä"
        if arvo == 11:
            return "Jätkä"
        if arvo == 12:
            return "Kuningatar"
        if arvo == 13:
            return "Kuningas"
        return str(arvo)

    def hanki_maa(self):
        return self.maa

    def hanki_arvo_poydassa(self):
        return self.arvo_poydassa

    def hanki_arvo_kadessa(self):
        return self.arvo_kadessa

    def hanki_nimi(self):
        return self.nimi

    # Kortin merkkijonoesitys
    def __str__(self):
        str = f"{self.maa}-{self.arvo_poydassa}"
        return str