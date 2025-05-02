from PyQt6.QtWidgets import QButtonGroup, QErrorMessage, QGridLayout, QMainWindow, QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QListWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from peli import Peli
from pelaaja import Pelaaja
from kortti import Kortti
import time


class Aloitusikkuna(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.paa_widget = QWidget()

        self.layout = QVBoxLayout()

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.uusi_peli_nappi = QPushButton("Uusi peli")
        self.jatka_pelia_nappi = QPushButton("Jatka peliä")
        self.uusi_peli_nappi.setFixedSize(600, 200)
        self.jatka_pelia_nappi.setFixedSize(600, 200)

        self.layout.addWidget(self.uusi_peli_nappi)
        self.layout.addWidget(self.jatka_pelia_nappi)

        self.uusi_peli_nappi.clicked.connect(self.uusi_peli_painettu)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.layout)

        self.showFullScreen()

    def uusi_peli_painettu(self):
        self.pelaajienlisaysikkuna = Pelaajienlisaysikkuna()
        self.pelaajienlisaysikkuna.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class Pelaajienlisaysikkuna(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.peli = Peli()

        self.paa_widget = QWidget()
        self.paa_layout = QHBoxLayout()

        self.nappi_layout = QVBoxLayout()
        self.lista_layout = QVBoxLayout()

        self.lisaa_pelaaja_nappi = QPushButton("Lisää pelaaja")
        self.lisaa_pelaaja_nappi.setFixedSize(600, 200)
        self.lisaa_pelaaja_nappi.clicked.connect(self.kysy_pelaajan_nimea)

        self.aloita_peli_nappi = QPushButton("Aloita peli")
        self.aloita_peli_nappi.setFixedSize(600, 200)
        self.aloita_peli_nappi.clicked.connect(self.aloita_peli)

        self.palaa_nappi = QPushButton("Takaisin päävalikkoon")
        self.palaa_nappi.setFixedSize(300, 100)
        self.palaa_nappi.clicked.connect(self.palaa)

        self.tekstikentta = QLabel("Lisätyt pelaajat:")
        fontti = QFont()
        fontti.setPointSize(17)
        self.tekstikentta.setFont(fontti)


        self.pelaajalista = QListWidget()
        self.pelaajalista.setFont(fontti)

        self.nappi_layout.addWidget(self.lisaa_pelaaja_nappi)
        self.nappi_layout.addWidget(self.aloita_peli_nappi)
        self.nappi_layout.addStretch()
        self.nappi_layout.addWidget(self.palaa_nappi)

        self.paa_layout.addLayout(self.nappi_layout)

        self.lista_layout.addWidget(self.tekstikentta)
        self.lista_layout.addWidget(self.pelaajalista)

        self.paa_layout.addLayout(self.lista_layout)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.paa_layout)
        self.showFullScreen()

    def kysy_pelaajan_nimea(self):
        teksti, ok = QInputDialog.getText(self, "Anna pelaajan nimi", "Pelaajan nimi:")
        if ok:
            pelaaja = Pelaaja(teksti)
            self.peli.lisaa_pelaaja(pelaaja)
            self.pelaajalista.addItem(pelaaja.hanki_nimi())

    def aloita_peli(self):
        if len(self.peli.pelaajat) < 2:
            virheviesti = QErrorMessage(self)
            virheviesti.setWindowTitle("Virhe")
            virheviesti.showMessage("Pelaajia tulee lisätä vähintään 2!")
        else:
            self.peli_ikkuna = PeliIkkuna(self.peli)
            self.peli_ikkuna.show()
            self.close()

    def palaa(self):
        self.aloitus_ikkuna = Aloitusikkuna()
        self.aloitus_ikkuna.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class PeliIkkuna(QMainWindow):

    def __init__(self, peli):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.peli = peli

        self.indeksi = 0

        self.valitut_kortit = []

        self.pelattu_kortti = None

        self.pelaajan_korttinapit = []
        self.poydan_korttinapit = []

        self.peli.luo_pakka()
        self.peli.jaa_kortit()

        self.paa_widget = QWidget()

        self.paa_layout = QVBoxLayout()

        self.poyta_layout = QVBoxLayout()
        self.poyta_tesktikentta = QLabel("Pöydän kortit")
        self.poyta_layout.addWidget(self.poyta_tesktikentta)

        self.poyta_kortit_layout = QGridLayout()
        self.poyta_layout.addLayout(self.poyta_kortit_layout)

        self.pelaaja_layout = QVBoxLayout()
        self.pelaaja_teksti_nappi_layout = QHBoxLayout()
        self.pelaaja_layout.addLayout(self.pelaaja_teksti_nappi_layout)

        self.pelaaja_tekstikentta = QLabel()
        self.pelaaja_teksti_nappi_layout.addWidget(self.pelaaja_tekstikentta)

        self.valmis_nappi = QPushButton("Valmis")
        self.valmis_nappi.setFixedSize(100, 20)
        self.valmis_nappi.clicked.connect(self.valmis_painettu)
        self.pelaaja_teksti_nappi_layout.addWidget(self.valmis_nappi)

        self.pelaaja_kortti_layout = QHBoxLayout()
        self.pelaaja_layout.addLayout(self.pelaaja_kortti_layout)

        self.pelaaja_kortti_nappiryhma = QButtonGroup()
        self.pelaaja_kortti_nappiryhma.setExclusive(True)

        self.paa_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.paivita_poydan_kortit()
        self.paivita_pelaajan_kortit()

        self.paa_layout.addStretch(10)
        self.paa_layout.addLayout(self.poyta_layout)
        self.paa_layout.addStretch(10)
        self.paa_layout.addLayout(self.pelaaja_layout)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.paa_layout)

        self.showFullScreen()

    def paivita_poydan_kortit(self):
        for i, kortti in enumerate(self.peli.poyta.poydan_kortit):
            nappi = KorttiNappi(kortti)
            nappi.setText(f"{kortti.__str__()}")
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            self.poydan_korttinapit.append(nappi)
            nappi.clicked.connect(lambda painettu, k=kortti: self.poydan_kortti_painettu(painettu, k))
            rivi = i // 6
            sarake = i % 6
            self.poyta_kortit_layout.addWidget(nappi, rivi, sarake)



    def paivita_pelaajan_kortit(self):
        for kortti in self.peli.pelaajat[self.indeksi].hanki_kasi():
            nappi = KorttiNappi(kortti)
            nappi.setText(f"{kortti.__str__()}")
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            self.pelaajan_korttinapit.append(nappi)
            self.pelaaja_kortti_nappiryhma.addButton(nappi)
            nappi.clicked.connect(lambda painettu, k=kortti: self.pelaajan_kortti_painettu(painettu, k))
            self.pelaaja_kortti_layout.addWidget(nappi)
        self.pelaaja_tekstikentta.setText(f"Omat kortit (Pelaaja \"{self.peli.pelaajat[self.indeksi].hanki_nimi()}\")")

    def poydan_kortti_painettu(self, painettu, kortti):
        if painettu:
            self.valitut_kortit.append(kortti)
        else:
            self.valitut_kortit.remove(kortti)

    def pelaajan_kortti_painettu(self, painettu, kortti):
        if painettu:
            self.pelattu_kortti = kortti
        else:
            self.pelattu_kortti = None

    def valmis_painettu(self):
        if self.pelattu_kortti and len(self.valitut_kortit) > 0:
            totuusarvo, nostettu_kortti = self.peli.pelaa_kortti(self.peli.pelaajat[self.indeksi], self.pelattu_kortti, self.valitut_kortit)
            if totuusarvo:
                self.poista_korttinappi_pelaajalta(self.pelattu_kortti)
                self.lisaa_korttinappi_pelaajalle(nostettu_kortti)
                for kortti in self.valitut_kortit:
                    self.poista_korttinappi_poydasta(kortti)
                self.pelattu_kortti = None
            else:
                virheviesti = QErrorMessage(self)
                virheviesti.setWindowTitle("Virhe")
                virheviesti.showMessage("Valitsemasi kortit eivät ole sääntöjen mukaiset!")
        elif self.pelattu_kortti and len(self.valitut_kortit) == 0:
            self.poista_korttinappi_pelaajalta(self.pelattu_kortti)
            nostettu_kortti = self.peli.laita_kortti_poytaan(self.peli.pelaajat[self.indeksi], self.pelattu_kortti)
            self.lisaa_korttinappi_pelaajalle(nostettu_kortti)
            self.lisaa_korttinappi_poytaan(self.pelattu_kortti)
            self.pelattu_kortti = None
        else:
            virheviesti = QErrorMessage(self)
            virheviesti.setWindowTitle("Virhe")
            virheviesti.showMessage("Sinun tulee valita ainakin yksi pelattava kortti!")

    def lisaa_korttinappi_poytaan(self, kortti):
        nappi = KorttiNappi(kortti)
        nappi.setText(f"{kortti.__str__()}")
        nappi.setFixedSize(100, 160)
        nappi.setCheckable(True)
        self.poydan_korttinapit.append(nappi)
        nappi.clicked.connect(lambda painettu, k=kortti: self.poydan_kortti_painettu(painettu, k))
        rivi = (len(self.poydan_korttinapit) - 1) // 6
        sarake = (len(self.poydan_korttinapit) - 1) % 6
        self.poyta_kortit_layout.addWidget(nappi, rivi, sarake)

    def poista_korttinappi_poydasta(self, kortti):
        for nappi in self.poydan_korttinapit:
            if nappi.hanki_kortti() == kortti:
                nappi.setParent(None)
                nappi.deleteLater()
                self.poydan_korttinapit.remove(nappi)

    def lisaa_korttinappi_pelaajalle(self, kortti):
        nappi = KorttiNappi(kortti)
        nappi.setText(f"{kortti.__str__()}")
        nappi.setFixedSize(100, 160)
        nappi.setCheckable(True)
        self.pelaajan_korttinapit.append(nappi)
        self.pelaaja_kortti_nappiryhma.addButton(nappi)
        nappi.clicked.connect(lambda painettu, k=kortti: self.pelaajan_kortti_painettu(painettu, k))
        self.pelaaja_kortti_layout.addWidget(nappi)

    def poista_korttinappi_pelaajalta(self, kortti):
        for nappi in self.pelaajan_korttinapit:
            if nappi.hanki_kortti() == kortti:
                nappi.setParent(None)
                nappi.deleteLater()
                self.pelaajan_korttinapit.remove(nappi)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class KorttiNappi(QPushButton):

    def __init__(self, kortti):
        super().__init__()
        self.kortti = kortti

    def hanki_kortti(self):
        return self.kortti
