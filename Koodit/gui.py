from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QListWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from peli import Peli
from pelaaja import Pelaaja
from kortti import Kortti


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
        self.peli_ikkuna = PeliIkkuna()
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

    def __init__(self):
        super().__init__()
