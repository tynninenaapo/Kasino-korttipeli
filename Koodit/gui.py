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
        self.pelaaja_tekstikentta = QLabel()
        self.pelaaja_layout.addWidget(self.pelaaja_tekstikentta)

        self.pelaaja_kortti_layout = QHBoxLayout()
        self.pelaaja_layout.addLayout(self.pelaaja_kortti_layout)

        self.pelaaja_kortti_nappiryhma = QButtonGroup()
        self.pelaaja_kortti_nappiryhma.setExclusive(True)

        self.paa_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.paivita_poydan_kortit()
        self.paivita_pelaajan_kortit()

        self.paa_layout.addStretch(50)
        self.paa_layout.addLayout(self.poyta_layout)
        self.paa_layout.addStretch()
        self.paa_layout.addLayout(self.pelaaja_layout)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.paa_layout)

        self.showFullScreen()

    def paivita_poydan_kortit(self):
        x = 0
        y = 0
        for kortti in self.peli.poyta.poydan_kortit:
            nappi = QPushButton(f"{kortti.__str__()}")
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            nappi.clicked.connect(lambda painettu, k=kortti: self.poydan_kortti_painettu(painettu, k))
            if x == 0:
                self.poyta_kortit_layout.addWidget(nappi, x, y)
                x += 1
            if x == 1:
                self.poyta_kortit_layout.addWidget(nappi, x, y)
                x = 0
                y += 1

    def paivita_pelaajan_kortit(self):
        for kortti in self.peli.pelaajat[self.indeksi].hanki_kasi():
            nappi = QPushButton(f"{kortti.__str__()}")
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            self.pelaaja_kortti_nappiryhma.addButton(nappi)
            nappi.clicked.connect(lambda painettu, k=kortti: self.pelaajan_kortti_painettu(painettu, k))
            self.pelaaja_kortti_layout.addWidget(nappi)
        self.pelaaja_tekstikentta.setText(f"Omat kortit (Pelaaja \"{self.peli.pelaajat[self.indeksi].hanki_nimi()}\")")
        self.indeksi += 1

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
