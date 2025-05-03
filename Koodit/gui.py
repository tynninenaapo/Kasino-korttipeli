from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QButtonGroup, QErrorMessage, QGridLayout, QMainWindow, QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QListWidget
from PyQt6.QtCore import Qt, QTimer
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
        self.jatka_pelia_nappi.clicked.connect(self.jatka_pelia_painettu)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.layout)

        self.showFullScreen()

    def uusi_peli_painettu(self):
        self.pelaajienlisaysikkuna = Pelaajienlisaysikkuna()
        self.pelaajienlisaysikkuna.show()
        self.close()

    def jatka_pelia_painettu(self):
        peli = Peli()
        indeksi = peli.lue_pelitilanne()
        self.peli_ikkuna = PeliIkkuna(peli, indeksi, False)
        self.peli_ikkuna.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            vastaus = QMessageBox.question(self, "Vahvistus", "Haluatko varmasti poistua pelistä?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if vastaus == QMessageBox.StandardButton.Yes:
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
            vastaus = QMessageBox.question(self, "Vahvistus", "Haluatko varmasti poistua pelistä?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if vastaus == QMessageBox.StandardButton.Yes:
                self.close()


class PeliIkkuna(QMainWindow):

    def __init__(self, peli, indeksi=0, uusi_peli=True):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.peli = peli

        self.indeksi = indeksi

        self.valitut_kortit = []

        self.pelattu_kortti = None

        self.pelaajan_korttinapit = []
        self.poydan_korttinapit = []

        if uusi_peli:
            self.peli.luo_pakka()
            self.peli.jaa_kortit()

        self.pelaajan_vuoro = self.peli.pelaajat[self.indeksi]
        self.viimeisin_nostaja = None

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
        for kortti in self.pelaajan_vuoro.hanki_kasi():
            nappi = KorttiNappi(kortti)
            nappi.setText(f"{kortti.__str__()}")
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            self.pelaajan_korttinapit.append(nappi)
            self.pelaaja_kortti_nappiryhma.addButton(nappi)
            nappi.clicked.connect(lambda painettu, k=kortti: self.pelaajan_kortti_painettu(painettu, k))
            self.pelaaja_kortti_layout.addWidget(nappi)
        self.pelaaja_tekstikentta.setText(f"Omat kortit (Pelaaja \"{self.pelaajan_vuoro.hanki_nimi()}\")")

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
        if len(self.pelaajan_vuoro.hanki_kasi()) == 0:
            self.vuoronvaihto()
        if self.pelattu_kortti and len(self.valitut_kortit) > 0:
            totuusarvo, nostettu_kortti = self.peli.pelaa_kortti(self.pelaajan_vuoro, self.pelattu_kortti, self.valitut_kortit)
            if totuusarvo:
                self.poista_korttinappi_pelaajalta(self.pelattu_kortti)
                if nostettu_kortti:
                    self.lisaa_korttinappi_pelaajalle(nostettu_kortti)
                for kortti in self.valitut_kortit:
                    self.poista_korttinappi_poydasta(kortti)
                self.pelattu_kortti = None
                self.valitut_kortit = []
                self.viimeisin_nostaja = self.pelaajan_vuoro
                self.vuoronvaihto()
            else:
                virheviesti = QErrorMessage(self)
                virheviesti.setWindowTitle("Virhe")
                virheviesti.showMessage("Valitsemasi kortit eivät ole sääntöjen mukaiset!")
        elif self.pelattu_kortti and len(self.valitut_kortit) == 0:
            self.poista_korttinappi_pelaajalta(self.pelattu_kortti)
            nostettu_kortti = self.peli.laita_kortti_poytaan(self.pelaajan_vuoro, self.pelattu_kortti)
            if nostettu_kortti:
                self.lisaa_korttinappi_pelaajalle(nostettu_kortti)
            self.lisaa_korttinappi_poytaan(self.pelattu_kortti)
            self.pelattu_kortti = None
            self.vuoronvaihto()
            self.kierros_paattyy()
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

    def poista_kaikki_pelaajan_korttinapit(self):
        for nappi in self.pelaajan_korttinapit:
            nappi.setParent(None)
            nappi.deleteLater()
        self.pelaajan_korttinapit = []

    def vuoronvaihto(self):
        nolla_korttia = 0
        for pelaaja in self.peli.pelaajat:
            if len(pelaaja.hanki_kasi()) == 0:
                nolla_korttia += 1
            else:
                break
        if nolla_korttia == len(self.peli.pelaajat):
            self.kierros_paattyy()
        else:
            self.valmis_nappi.setEnabled(False)
            if self.indeksi == len(self.peli.pelaajat) - 1:
                self.indeksi = 0
            else:
                self.indeksi += 1
            self.pelaajan_vuoro = self.peli.pelaajat[self.indeksi]
            self.poista_kaikki_pelaajan_korttinapit()
            self.pelaaja_tekstikentta.setText(f"Vuoro vaihtuu pelaajalle {self.pelaajan_vuoro.hanki_nimi()} (10 sekuntia)...")
            self.paivita_pelaajan_kortit()
            self.valmis_nappi.setEnabled(True)


    def kierros_paattyy(self):
        for kortti in self.peli.poyta.poydan_kortit:
            self.viimeisin_nostaja.lisaa_kortti_kateen(kortti)
        self.peli.poyta.poydan_kortit = []
        self.paatosikkuna = KierrosPaattyyIkkuna(self.peli, self)
        self.paatosikkuna.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            vastaus = QMessageBox.question(self, "Vahvistus", "Olet poistumassa pelistä. Haluatko tallentaa pelin?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if vastaus == QMessageBox.StandardButton.Yes:
                # self.peli.kirjoita_pelitilanne(self.indeksi)
                self.close()
            elif vastaus == QMessageBox.StandardButton.No:
                self.close()
            elif vastaus == QMessageBox.StandardButton.Cancel:
                pass

class KierrosPaattyyIkkuna(QWidget):

    def __init__(self, peli, peli_ikkuna):
        super().__init__()

        self.peli = peli
        self.peli_ikkuna = peli_ikkuna

        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint )

        self.setWindowTitle("Kierros päättyi!")
        self.setFixedSize((len(self.peli.pelaajat) + 1) * 110, 330)

        self.paalayout = QVBoxLayout()

        self.tekstikentta = QLabel("Tulokset:")
        self.paalayout.addWidget(self.tekstikentta)

        self.taulukko = QTableWidget(8, len(self.peli.pelaajat) + 1)
        self.paalayout.addWidget(self.taulukko)

        self.nappi_layout = QHBoxLayout()

        self.lopeta_peli_nappi = QPushButton("Lopeta peli")
        self.lopeta_peli_nappi.setFixedSize(100, 30)
        self.lopeta_peli_nappi.clicked.connect(self.lopeta_peli_painettu)
        self.jatka_pelia_nappi = QPushButton("Jatka peliä")
        self.jatka_pelia_nappi.setFixedSize(100, 30)

        self.nappi_layout.addWidget(self.lopeta_peli_nappi)
        self.nappi_layout.addWidget(self.jatka_pelia_nappi)
        self.paalayout.addLayout(self.nappi_layout)
        self.setLayout(self.paalayout)
        self.tayta_taulukko()
        self.show()


    def tayta_taulukko(self):
        self.taulukko.verticalHeader().setVisible(False)
        self.taulukko.horizontalHeader().setVisible(False)
        self.taulukko.setItem(0, 0, QTableWidgetItem("Pelaajan nimi"))
        self.taulukko.setItem(1, 0, QTableWidgetItem("Korttien määrä"))
        self.taulukko.setItem(2, 0, QTableWidgetItem("Patojen määrä"))
        self.taulukko.setItem(3, 0, QTableWidgetItem("Mökit"))
        self.taulukko.setItem(4, 0, QTableWidgetItem("Ässät"))
        self.taulukko.setItem(5, 0, QTableWidgetItem("Ruutu-10"))
        self.taulukko.setItem(6, 0, QTableWidgetItem("Pata-2"))
        self.taulukko.setItem(7, 0, QTableWidgetItem("Pisteet"))
        self.peli.laske_pisteet()
        for i, pelaaja in enumerate(self.peli.pelaajat):
            self.taulukko.setItem(0, i + 1, QTableWidgetItem(pelaaja.hanki_nimi()))
            self.taulukko.setItem(1, i + 1, QTableWidgetItem(str(len(pelaaja.hanki_pino()))))
            self.taulukko.setItem(2, i + 1, QTableWidgetItem(str(pelaaja.padat_pinossa)))
            self.taulukko.setItem(3, i + 1, QTableWidgetItem(str(pelaaja.hanki_mokit())))
            self.taulukko.setItem(4, i + 1, QTableWidgetItem(str(pelaaja.assat_pinossa)))
            for kortti in pelaaja.hanki_pino():
                if kortti.__str__() == "Ruutu-10":
                    self.taulukko.setItem(5, i + 1, QTableWidgetItem("X"))
                else:
                    self.taulukko.setItem(5, i + 1, QTableWidgetItem("O"))
                if kortti.__str__() == "Pata-2":
                    self.taulukko.setItem(6, i + 1, QTableWidgetItem("X"))
                else:
                    self.taulukko.setItem(6, i + 1, QTableWidgetItem("O"))
            if len(pelaaja.hanki_pino()) == 0:
                self.taulukko.setItem(5, i + 1, QTableWidgetItem("O"))
                self.taulukko.setItem(6, i + 1, QTableWidgetItem("O"))
            self.taulukko.setItem(7, i + 1, QTableWidgetItem(str(pelaaja.hanki_pisteet())))

    def lopeta_peli_painettu(self):
        vastaus = QMessageBox.question(self, "Vahvistus", "Olet poistumassa pelistä. Haluatko tallentaa pelin?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        if vastaus == QMessageBox.StandardButton.Yes:
            # self.peli.kirjoita_pelitilanne(self.indeksi)
            self.peli_ikkuna.close()
            self.close()
        elif vastaus == QMessageBox.StandardButton.No:
            self.peli_ikkuna.close()
            self.close()
        elif vastaus == QMessageBox.StandardButton.Cancel:
            pass


class KorttiNappi(QPushButton):

    def __init__(self, kortti):
        super().__init__()
        self.kortti = kortti

    def hanki_kortti(self):
        return self.kortti
