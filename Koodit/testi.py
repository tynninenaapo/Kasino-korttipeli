import unittest
from kortti import Kortti
from poyta import Poyta
from peli import Peli

class Testi(unittest.TestCase):

    def testaa_korttien_tarkistusta1(self):
        peli = Peli()

        valitut_kortit = [Kortti("Ruutu", 10)]
        pelattu_kortti = Kortti("Pata", 10)
        self.assertTrue(peli.tarkista_kortti(pelattu_kortti, valitut_kortit))

        pelattu_kortti = Kortti("Pata", 9)
        self.assertFalse(peli.tarkista_kortti(pelattu_kortti, valitut_kortit))

    def testaa_korttien_tarkistusta2(self):
        peli = Peli()

        valitut_kortit = [Kortti("Pata", 4), Kortti("Ruutu", 7)]
        pelattu_kortti = Kortti("Hertta", 11)
        self.assertTrue(peli.tarkista_kortti(pelattu_kortti, valitut_kortit))

    def testaa_korttien_tarkistusta3(self):
        peli = Peli()

        valitut_kortit = [Kortti("Pata", 4), Kortti("Ruutu", 7), Kortti("Hertta", 11)]
        pelattu_kortti = Kortti("Risti", 11)
        self.assertTrue(peli.tarkista_kortti(pelattu_kortti, valitut_kortit))

    def testaa_korttien_tarkistusta4(self):
        peli = Peli()

        valitut_kortit = [Kortti("Pata", 4), Kortti("Ruutu", 7),
                          Kortti("Hertta", 11), Kortti("Risti", 8), Kortti("Pata", 3)]
        pelattu_kortti = Kortti("Risti", 11)
        self.assertTrue(peli.tarkista_kortti(pelattu_kortti, valitut_kortit))


if __name__ == '__main__':
    unittest.main()