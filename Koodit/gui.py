from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QButtonGroup, QErrorMessage, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QListWidget
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon
from peli import Peli
from pelaaja import Pelaaja

# Pitää kirjaa aloitusvuorosta kierrosten edetessä
aloitusvuoro = 0


# Ensimmäinen ikkuna, joka aukeaa, kun ohjelman ajaa
class Aloitusikkuna(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.paa_widget = QWidget()
        self.paa_widget.setStyleSheet("background-color: darkgreen;")

        self.layout = QVBoxLayout()

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tekstikentta = QLabel("Kasino")
        self.tekstikentta.setStyleSheet("color: white;")
        tekstifontti = QFont()
        tekstifontti.setPointSize(80)
        tekstifontti.setBold(True)
        self.tekstikentta.setFont(tekstifontti)
        self.tekstikentta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.tekstikentta)

        self.uusi_peli_nappi = QPushButton("Uusi peli")
        self.uusi_peli_nappi.setStyleSheet("background-color: orange; color: white;")
        self.jatka_pelia_nappi = QPushButton("Jatka peliä")
        self.jatka_pelia_nappi.setStyleSheet("background-color: orange; color: white;")
        self.uusi_peli_nappi.setFixedSize(600, 200)
        self.jatka_pelia_nappi.setFixedSize(600, 200)

        fontti = QFont()
        fontti.setPointSize(30)
        fontti.setBold(True)
        self.uusi_peli_nappi.setFont(fontti)
        self.jatka_pelia_nappi.setFont(fontti)

        self.layout.addWidget(self.uusi_peli_nappi)
        self.layout.addWidget(self.jatka_pelia_nappi)

        self.uusi_peli_nappi.clicked.connect(self.uusi_peli_painettu)
        self.jatka_pelia_nappi.clicked.connect(self.jatka_pelia_painettu)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.layout)

        self.showFullScreen()

    # Uusi peli -nappi avaa pelaajienlisäysikkunan
    def uusi_peli_painettu(self):
        self.pelaajienlisaysikkuna = Pelaajienlisaysikkuna()
        self.pelaajienlisaysikkuna.show()
        QTimer.singleShot(1000, self.close)

    # Jatka peliä -nappi lukee pelitilanne.txt-tiedostosta tallennetun pelin
    # ja avaa suoraan peli-ikkunan
    def jatka_pelia_painettu(self):
        peli = Peli()
        paluuarvo = peli.lue_pelitilanne()
        if type(paluuarvo) == tuple:
            indeksi = paluuarvo[0]
            aloitus_vuoro = paluuarvo[1]
            self.peli_ikkuna = PeliIkkuna(peli, indeksi, False, aloitus_vuoro)
            self.peli_ikkuna.show()
            QTimer.singleShot(1000, self.close)
        elif paluuarvo is None:
            virheviesti = QErrorMessage(self)
            virheviesti.setWindowTitle("Virhe")
            virheviesti.showMessage("Ei tallennettua peliä!")
        else:
            virheviesti = QErrorMessage(self)
            virheviesti.setWindowTitle("Virhe")
            virheviesti.showMessage("Virhe tallennetussa pelitiedostossa")

    # Ohjelmasta voi poistua ESC-näppäimellä
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            vastaus = QMessageBox.question(self, "Vahvistus", "Haluatko varmasti poistua pelistä?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if vastaus == QMessageBox.StandardButton.Yes:
                self.close()


# Uusi peli -napin painamisen jälkeen aukeaa ikkuna, jossa voi lisätä 2-N pelaajaa
class Pelaajienlisaysikkuna(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.peli = Peli()

        self.paa_widget = QWidget()
        self.paa_widget.setStyleSheet("background-color: darkgreen;")
        self.paa_layout = QHBoxLayout()

        self.nappi_layout = QVBoxLayout()
        self.lista_layout = QVBoxLayout()

        self.lisaa_pelaaja_nappi = QPushButton("Lisää pelaaja")
        self.lisaa_pelaaja_nappi.setStyleSheet("background-color: orange; color: white;")
        self.lisaa_pelaaja_nappi.setFixedSize(600, 200)
        self.lisaa_pelaaja_nappi.clicked.connect(self.kysy_pelaajan_nimea)

        self.aloita_peli_nappi = QPushButton("Aloita peli")
        self.aloita_peli_nappi.setStyleSheet("background-color: orange; color: white;")
        self.aloita_peli_nappi.setFixedSize(600, 200)
        self.aloita_peli_nappi.clicked.connect(self.aloita_peli)

        nappifontti = QFont()
        nappifontti.setPointSize(30)
        nappifontti.setBold(True)
        self.lisaa_pelaaja_nappi.setFont(nappifontti)
        self.aloita_peli_nappi.setFont(nappifontti)

        self.palaa_nappi = QPushButton("Takaisin päävalikkoon")
        self.palaa_nappi.setStyleSheet("background-color: orange; color: white;")
        self.palaa_nappi.setFixedSize(300, 100)
        self.palaa_nappi.clicked.connect(self.palaa)

        self.tekstikentta = QLabel("Lisätyt pelaajat:")
        self.tekstikentta.setStyleSheet("color: white;")
        tekstifontti = QFont()
        tekstifontti.setPointSize(17)
        self.tekstikentta.setFont(tekstifontti)
        self.palaa_nappi.setFont(tekstifontti)

        self.pelaajalista = QListWidget()
        self.pelaajalista.setStyleSheet("background-color: white; color: black")
        self.pelaajalista.setFont(tekstifontti)

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

    # Kysyy pelaajan nimen ja luo pelaaja-olion annetulla nimellä
    def kysy_pelaajan_nimea(self):
        teksti, ok = QInputDialog.getText(self, "Anna pelaajan nimi", "Pelaajan nimi:")
        if ok:
            if len(teksti) == 0:
                virheviesti = QErrorMessage(self)
                virheviesti.setWindowTitle("Virhe")
                virheviesti.showMessage("Nimen tulee olla ainakin 1 merkkiä pitkä!")
            elif len(teksti) > 25:
                virheviesti = QErrorMessage(self)
                virheviesti.setWindowTitle("Virhe")
                virheviesti.showMessage("Liian pitkä nimi!")
            else:
                virhe = False
                for pelaaja in self.peli.pelaajat:
                    if pelaaja.hanki_nimi() == teksti:
                        virheviesti = QErrorMessage(self)
                        virheviesti.setWindowTitle("Virhe")
                        virheviesti.showMessage(f"Pelaaja nimellä {teksti} on lisätty jo peliin!")
                        virhe = True
                if not virhe:
                    pelaaja = Pelaaja(teksti)
                    self.peli.lisaa_pelaaja(pelaaja)
                    self.pelaajalista.addItem(pelaaja.hanki_nimi())

    # Kun pelaajia on lisätty tarpeeksi, metodi avaa peli-ikkunan
    def aloita_peli(self):
        if len(self.peli.pelaajat) < 2:
            virheviesti = QErrorMessage(self)
            virheviesti.setWindowTitle("Virhe")
            virheviesti.showMessage("Pelaajia tulee lisätä vähintään 2!")
        else:
            self.peli_ikkuna = PeliIkkuna(self.peli)
            self.peli_ikkuna.show()
            QTimer.singleShot(1000, self.close)

    # Palauttaa takaisin päävalikkoon
    def palaa(self):
        vastaus = QMessageBox.question(self, "Vahvistus", "Haluatko palata takaisin päävalikkoon?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if vastaus == QMessageBox.StandardButton.Yes:
            self.aloitus_ikkuna = Aloitusikkuna()
            self.aloitus_ikkuna.show()
            QTimer.singleShot(1000, self.close)

    # Ohjelmasta voi poistua ESC-näppäimellä
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            vastaus = QMessageBox.question(self, "Vahvistus", "Haluatko varmasti poistua pelistä?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if vastaus == QMessageBox.StandardButton.Yes:
                self.close()


# Ikkuna, jossa varsinaista peliä voi pelata
class PeliIkkuna(QMainWindow):

    def __init__(self, peli, indeksi=0, uusi_peli=True, aloitus_vuoro=0):
        super().__init__()
        self.setWindowTitle("Kasino")

        self.peli = peli

        self.indeksi = indeksi
        global aloitusvuoro
        aloitusvuoro = aloitus_vuoro

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
        self.paa_widget.setStyleSheet("background-color: darkgreen;")

        self.layout = QHBoxLayout()

        self.paa_layout = QVBoxLayout()
        self.sivu_layout = QVBoxLayout()

        self.tekstifontti = QFont()
        self.tekstifontti.setPointSize(17)

        self.palaa_alkuvalikkoon_nappi = QPushButton("Palaa päävalikkoon")
        self.palaa_alkuvalikkoon_nappi.setFixedSize(300, 100)
        self.palaa_alkuvalikkoon_nappi.setStyleSheet("background-color: orange; color: white;")
        self.palaa_alkuvalikkoon_nappi.setFont(self.tekstifontti)
        self.palaa_alkuvalikkoon_nappi.clicked.connect(self.palaa_paavalikkoon_painettu)
        self.sivu_layout.addWidget(self.palaa_alkuvalikkoon_nappi)

        self.tapahtumat_teksti = QLabel("Tapahtumat")
        self.tapahtumat_teksti.setStyleSheet("color: white;")
        self.tapahtumat_teksti.setFont(self.tekstifontti)
        self.sivu_layout.addWidget(self.tapahtumat_teksti)

        self.tapahtumat = QListWidget()
        self.tapahtumat.setStyleSheet("background-color: white; color: black;")
        self.tapahtumat.setFixedSize(400, 600)
        self.sivu_layout.addWidget(self.tapahtumat)

        self.layout.addLayout(self.sivu_layout)
        self.layout.addLayout(self.paa_layout)

        self.poyta_widget = QWidget()
        self.poyta_widget.setMinimumHeight(230)
        self.poyta_widget.setStyleSheet("background-color: saddlebrown;")
        self.poyta_layout = QVBoxLayout()
        self.poyta_widget.setLayout(self.poyta_layout)
        self.poyta_tekstikentta = QLabel("Pöydän kortit")
        self.poyta_tekstikentta.setStyleSheet("color: white;")
        self.poyta_layout.addWidget(self.poyta_tekstikentta)
        self.poyta_layout.addStretch()
        self.poyta_tekstikentta.setFont(self.tekstifontti)

        self.poyta_kortit_layout = QHBoxLayout()
        self.poyta_layout.addLayout(self.poyta_kortit_layout)
        self.poyta_kortit_layout2 = QHBoxLayout()
        self.poyta_layout.addLayout(self.poyta_kortit_layout2)

        self.pelaaja_widget = QWidget()
        self.pelaaja_widget.setFixedSize(870, 230)
        self.pelaaja_widget.setStyleSheet("background-color: saddlebrown;")
        self.pelaaja_layout = QVBoxLayout()
        self.pelaaja_widget.setLayout(self.pelaaja_layout)
        self.pelaaja_teksti_nappi_layout = QHBoxLayout()
        self.pelaaja_layout.addLayout(self.pelaaja_teksti_nappi_layout)
        self.pelaaja_layout.addStretch()

        self.pelaaja_tekstikentta = QLabel()
        self.pelaaja_teksti_nappi_layout.addWidget(self.pelaaja_tekstikentta)

        self.valmis_nappi = QPushButton("Valmis")
        self.valmis_nappi.setFixedSize(100, 20)
        self.valmis_nappi.setStyleSheet("background-color: orange; color: white;")
        self.valmis_nappi.clicked.connect(self.valmis_painettu)
        self.pelaaja_teksti_nappi_layout.addWidget(self.valmis_nappi)

        self.valmis_fontti = QFont()
        self.valmis_fontti.setBold(True)
        self.valmis_nappi.setFont(self.valmis_fontti)

        self.pelaaja_kortti_layout = QHBoxLayout()
        self.pelaaja_layout.addLayout(self.pelaaja_kortti_layout)

        self.pelaaja_kortti_nappiryhma = QButtonGroup()
        self.pelaaja_kortti_nappiryhma.setExclusive(True)

        self.paa_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.paivita_poydan_kortit()
        self.paivita_pelaajan_kortit()

        self.paa_layout.addStretch(10)
        self.paa_layout.addWidget(self.poyta_widget)
        self.paa_layout.addStretch(10)
        self.paa_layout.addWidget(self.pelaaja_widget)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.layout)

        self.showFullScreen()

    # Pelin alussa lisää KorttiNappi-oliot pöydälle
    def paivita_poydan_kortit(self):
        for kortti in self.peli.poyta.poydan_kortit:
            nappi = KorttiNappi(kortti)
            nappi.setIcon(QIcon(f"Kuvat/{kortti.__str__()}.png"))
            nappi.setIconSize(QSize(100, 160))
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            # Lähde: https://www.youtube.com/watch?v=HQNiSfb795A
            nappi.clicked.connect(lambda painettu, k=kortti: self.poydan_kortti_painettu(painettu, k))
            self.poyta_kortit_layout.addWidget(nappi)
            self.poydan_korttinapit.append(nappi)

    # Päivittää KorttiNappi -oliot jokaisen vuoron alussa
    def paivita_pelaajan_kortit(self):
        for kortti in self.pelaajan_vuoro.hanki_kasi():
            nappi = KorttiNappi(kortti)
            nappi.setIcon(QIcon(f"Kuvat/{kortti.__str__()}.png"))
            nappi.setIconSize(QSize(100, 160))
            nappi.setFixedSize(100, 160)
            nappi.setCheckable(True)
            self.pelaajan_korttinapit.append(nappi)
            self.pelaaja_kortti_nappiryhma.addButton(nappi)
            nappi.clicked.connect(lambda painettu, k=kortti: self.pelaajan_kortti_painettu(painettu, k))
            self.pelaaja_kortti_layout.addWidget(nappi)
        self.pelaaja_tekstikentta.setText(f"Omat kortit (Pelaaja \"{self.pelaajan_vuoro.hanki_nimi()}\")")
        self.pelaaja_tekstikentta.setFont(self.tekstifontti)
        self.pelaaja_tekstikentta.setStyleSheet("color: white;")
        self.valmis_nappi.setEnabled(True)

    # Hoitaa pöydän KorttiNappien toiminnallisuuden
    def poydan_kortti_painettu(self, painettu, kortti):
        if painettu:
            self.valitut_kortit.append(kortti)
        else:
            self.valitut_kortit.remove(kortti)

    # Hoitaa pelaajan KorttiNappien toiminnallisuuden
    def pelaajan_kortti_painettu(self, painettu, kortti):
        if painettu:
            self.pelattu_kortti = kortti
        else:
            self.pelattu_kortti = None

    # Hoitaa valmis -napin toiminnallisuuden, eli tarkistaa
    # pelaajan valitsemat kortit ja niiden mukaisella tavalla
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
                if len(self.poydan_korttinapit) == 0:
                    self.lisaa_tapahtuma(True)
                else:
                    self.lisaa_tapahtuma()
                self.pelattu_kortti = None
                self.valitut_kortit = []
                self.viimeisin_nostaja = self.pelaajan_vuoro
                self.valmis_nappi.setEnabled(False)
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
            self.lisaa_tapahtuma()
            self.pelattu_kortti = None
            self.valitut_kortit = []
            self.vuoronvaihto()
        else:
            virheviesti = QErrorMessage(self)
            virheviesti.setWindowTitle("Virhe")
            virheviesti.showMessage("Sinun tulee valita ainakin yksi pelattava kortti!")

    # Lisää tapahtumia listawidget -olioon sitä mukaa, kun
    # kortteja lisätään ja otetaan pöydästä
    def lisaa_tapahtuma(self, mokki=False):
        merkkijono = ""
        if len(self.valitut_kortit) == 0:
            merkkijono += f"{self.pelaajan_vuoro.hanki_nimi()} laittoi kortin {self.pelattu_kortti.__str__()} pöytään."
        elif len(self.valitut_kortit) == 1:
            merkkijono += f"{self.pelaajan_vuoro.hanki_nimi()} otti kortin {self.valitut_kortit[0].__str__()} pöydästä."
        elif len(self.valitut_kortit) == 2:
            merkkijono += f"{self.pelaajan_vuoro.hanki_nimi()} otti kortit {self.valitut_kortit[0].__str__()} ja {self.valitut_kortit[1].__str__()} pöydästä."
        else:
            merkkijono += f"{self.pelaajan_vuoro.hanki_nimi()} otti kortit "
            for i in range(len(self.valitut_kortit) - 1):
                merkkijono += f"{self.valitut_kortit[i].__str__()}, "
            merkkijono += f"ja {self.valitut_kortit[len(self.valitut_kortit) - 1].__str__()} pöydästä."
        if mokki:
            merkkijono += " (MÖKKI!)"
        self.tapahtumat.addItem(merkkijono)
        self.tapahtumat.scrollToBottom()

    # Lisää yhden KorttiNapin pöytään
    def lisaa_korttinappi_poytaan(self, kortti):
        nappi = KorttiNappi(kortti)
        nappi.setIcon(QIcon(f"Kuvat/{kortti.__str__()}.png"))
        nappi.setIconSize(QSize(100, 160))
        nappi.setFixedSize(100, 160)
        nappi.setCheckable(True)
        nappi.clicked.connect(lambda painettu, k=kortti: self.poydan_kortti_painettu(painettu, k))
        if len(self.poydan_korttinapit) <= 7:
            self.poyta_kortit_layout.addWidget(nappi)
        else:
            self.poyta_kortit_layout2.addWidget(nappi)
        self.poydan_korttinapit.append(nappi)

    # Poistaa yhden KorttiNapin pöydästä
    def poista_korttinappi_poydasta(self, kortti):
        for nappi in self.poydan_korttinapit[:]:
            if nappi.hanki_kortti() == kortti:
                nappi.deleteLater()
                self.poydan_korttinapit.remove(nappi)

    # Lisää yhden KorttiNapin pelaajalle
    def lisaa_korttinappi_pelaajalle(self, kortti):
        nappi = KorttiNappi(kortti)
        nappi.setIcon(QIcon(f"Kuvat/{kortti.__str__()}.png"))
        nappi.setIconSize(QSize(100, 160))
        nappi.setFixedSize(100, 160)
        nappi.setCheckable(True)
        self.pelaajan_korttinapit.append(nappi)
        self.pelaaja_kortti_nappiryhma.addButton(nappi)
        nappi.clicked.connect(lambda painettu, k=kortti: self.pelaajan_kortti_painettu(painettu, k))
        self.pelaaja_kortti_layout.addWidget(nappi)

    # Poistaa yhden KorttiNapin pelaajalta
    def poista_korttinappi_pelaajalta(self, kortti):
        for nappi in self.pelaajan_korttinapit[:]:
            if nappi.hanki_kortti() == kortti:
                self.pelaaja_kortti_layout.removeWidget(nappi)
                nappi.deleteLater()
                self.pelaajan_korttinapit.remove(nappi)
                break

    # Poistaa kaikki pelaajan KorttiNapit vuoron vaihtuessa
    def poista_kaikki_pelaajan_korttinapit(self):
        for nappi in self.pelaajan_korttinapit:
            nappi.deleteLater()
        self.pelaajan_korttinapit = []

    # Toteuttaa kaikki vuoronvaihdossa tarvittavat toimenpiteet
    # sekä tarkistaa, että pitääkö kierros päättää
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
            if self.indeksi == len(self.peli.pelaajat) - 1:
                self.indeksi = 0
            else:
                self.indeksi += 1
            self.pelaajan_vuoro = self.peli.pelaajat[self.indeksi]
            self.poista_kaikki_pelaajan_korttinapit()
            self.valmis_nappi.setEnabled(False)
            self.pelaaja_tekstikentta.setText(f"Vuoro vaihtuu pelaajalle {self.pelaajan_vuoro.hanki_nimi()} (5 sekuntia)...")
            QTimer.singleShot(5000, self.paivita_pelaajan_kortit)

    # Päättää kierroksen ja avaa kierroksenpäätösikkunan
    def kierros_paattyy(self):
        self.palaa_alkuvalikkoon_nappi.setEnabled(False)
        if self.viimeisin_nostaja:
            for kortti in self.peli.poyta.poydan_kortit:
                self.viimeisin_nostaja.lisaa_kortti_pinoon(kortti)
            self.peli.poyta.poydan_kortit = []
        self.paatosikkuna = KierrosPaattyyIkkuna(self.peli, self, self.indeksi)
        self.paatosikkuna.show()

    # Hoitaa Palaa päävalikkoon -napin toiminnallisuuden
    def palaa_paavalikkoon_painettu(self):
        vastaus = QMessageBox.question(self, "Vahvistus", "Olet poistumassa päävalikkoon. Haluatko tallentaa pelin?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        if vastaus == QMessageBox.StandardButton.Yes:
            self.peli.kirjoita_pelitilanne(self.indeksi, aloitusvuoro)
            self.aloitusikkuna = Aloitusikkuna()
            self.aloitusikkuna.show()
            QTimer.singleShot(1000, self.close)
        elif vastaus == QMessageBox.StandardButton.No:
            self.aloitusikkuna = Aloitusikkuna()
            self.aloitusikkuna.show()
            QTimer.singleShot(1000, self.close)
        elif vastaus == QMessageBox.StandardButton.Cancel:
            pass

    # Ohjelmasta voi poistua ESC-näppäimellä
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            vastaus = QMessageBox.question(self, "Vahvistus", "Olet poistumassa pelistä. Haluatko tallentaa pelin?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if vastaus == QMessageBox.StandardButton.Yes:
                self.peli.kirjoita_pelitilanne(self.indeksi, aloitusvuoro)
                self.close()
            elif vastaus == QMessageBox.StandardButton.No:
                self.close()
            elif vastaus == QMessageBox.StandardButton.Cancel:
                pass


# Ikkuna, joka aukeaa aina kierroksen päättyessä
class KierrosPaattyyIkkuna(QWidget):

    def __init__(self, peli, peli_ikkuna, indeksi):
        super().__init__()

        self.peli = peli
        self.peli_ikkuna = peli_ikkuna
        self.indeksi = indeksi

        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.setWindowTitle("Kierros päättyi!")
        self.setFixedSize((len(self.peli.pelaajat) + 1) * 110, 360)

        self.paalayout = QVBoxLayout()

        self.tekstikentta = QLabel("Tulokset:")
        self.paalayout.addWidget(self.tekstikentta)
        self.voittaja_tekstikentta = QLabel()
        self.paalayout.addWidget(self.voittaja_tekstikentta)

        self.taulukko = QTableWidget(8, len(self.peli.pelaajat) + 1)
        self.paalayout.addWidget(self.taulukko)

        self.nappi_layout = QHBoxLayout()

        self.lopeta_peli_nappi = QPushButton("Lopeta peli")
        self.lopeta_peli_nappi.setFixedSize(140, 30)
        self.lopeta_peli_nappi.clicked.connect(self.lopeta_peli_painettu)
        self.jatka_pelia_nappi = QPushButton("Jatka peliä")
        self.jatka_pelia_nappi.setFixedSize(140, 30)
        self.jatka_pelia_nappi.clicked.connect(self.jatka_pelia_painettu)

        self.nappi_layout.addWidget(self.lopeta_peli_nappi)
        self.nappi_layout.addWidget(self.jatka_pelia_nappi)
        self.paalayout.addLayout(self.nappi_layout)
        self.setLayout(self.paalayout)
        self.tayta_taulukko()
        self.show()

    # Täyttää taulukko-olioon pelaajien statistiikat
    # ja ilmoittaa voittajan, jos peli loppuu
    def tayta_taulukko(self):
        kuusitoista_pistetta = []
        self.taulukko.verticalHeader().setVisible(False)
        self.taulukko.horizontalHeader().setVisible(False)
        self.taulukko.setItem(0, 0, QTableWidgetItem("Pelaajan nimi"))
        self.taulukko.setItem(1, 0, QTableWidgetItem("Korttien määrä"))
        self.taulukko.setItem(2, 0, QTableWidgetItem("Patojen määrä"))
        self.taulukko.setItem(3, 0, QTableWidgetItem("Mökit"))
        self.taulukko.setItem(4, 0, QTableWidgetItem("Ässät"))
        self.taulukko.setItem(5, 0, QTableWidgetItem("Ruutu-10"))
        self.taulukko.setItem(6, 0, QTableWidgetItem("Pata-2"))
        self.taulukko.setItem(7, 0, QTableWidgetItem("Pisteet (yhteensä)"))
        self.peli.laske_pisteet()
        for i, pelaaja in enumerate(self.peli.pelaajat):
            self.taulukko.setItem(0, i + 1, QTableWidgetItem(pelaaja.hanki_nimi()))
            self.taulukko.setItem(1, i + 1, QTableWidgetItem(str(len(pelaaja.hanki_pino()))))
            self.taulukko.setItem(2, i + 1, QTableWidgetItem(str(pelaaja.padat_pinossa)))
            self.taulukko.setItem(3, i + 1, QTableWidgetItem(str(pelaaja.hanki_mokit())))
            self.taulukko.setItem(4, i + 1, QTableWidgetItem(str(pelaaja.assat_pinossa)))
            if pelaaja.on_ruutu10:
                self.taulukko.setItem(5, i + 1, QTableWidgetItem("Kyllä"))
            else:
                self.taulukko.setItem(5, i + 1, QTableWidgetItem("Ei"))
            if pelaaja.on_pata2:
                self.taulukko.setItem(6, i + 1, QTableWidgetItem("Kyllä"))
            else:
                self.taulukko.setItem(6, i + 1, QTableWidgetItem("Ei"))
            self.taulukko.setItem(7, i + 1, QTableWidgetItem(str(pelaaja.hanki_pisteet())))
            if pelaaja.hanki_pisteet() >= 16:
                kuusitoista_pistetta.append(pelaaja)
        if len(kuusitoista_pistetta) >= 1:
            self.jatka_pelia_nappi.setEnabled(False)
            self.lopeta_peli_nappi.setText("Palaa päävalikkoon")
            self.lopeta_peli_nappi.clicked.disconnect(self.lopeta_peli_painettu)
            self.lopeta_peli_nappi.clicked.connect(self.peli_loppu)
            max_pisteet = max(pelaaja.hanki_pisteet() for pelaaja in self.peli.pelaajat)
            voittajat = [pelaaja for pelaaja in self.peli.pelaajat if pelaaja.hanki_pisteet() == max_pisteet]
            if len(voittajat) == 1:
                self.voittaja_tekstikentta.setText(f"Voittaja on pelaaja {voittajat[0].hanki_nimi()}!")
            elif len(voittajat) == 2:
                self.voittaja_tekstikentta.setText(f"Pelaajilla {voittajat[0].hanki_nimi()} ja {voittajat[1].hanki_nimi()} tuli tasapeli!")
            else:
                merkkijono = ""
                for i in range(len(voittajat) - 1):
                    merkkijono += f"{voittajat[i].hanki_nimi()}, "
                merkkijono += f"ja {voittajat[len(voittajat) - 1].hanki_nimi()}"
                self.voittaja_tekstikentta.setText(f"Pelaajilla {merkkijono} tuli tasapeli!")

    # Hoitaa lopeta peli -napin toiminnallisuuden
    def lopeta_peli_painettu(self):
        vastaus = QMessageBox.question(self, "Vahvistus", "Olet poistumassa pelistä. Haluatko tallentaa pelin?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        if vastaus == QMessageBox.StandardButton.Yes:
            self.jatka_pelia_painettu()
            self.uusi_peli_ikkuna.close()
            self.peli.kirjoita_pelitilanne(aloitusvuoro, aloitusvuoro)
            self.peli_ikkuna.close()
            self.close()
        elif vastaus == QMessageBox.StandardButton.No:
            self.peli_ikkuna.close()
            self.close()
        elif vastaus == QMessageBox.StandardButton.Cancel:
            pass

    # Hoitaa jatka peliä -napin toiminnallisuuden
    def jatka_pelia_painettu(self):
        global aloitusvuoro
        if aloitusvuoro == len(self.peli.pelaajat) - 1:
            aloitusvuoro = 0
        else:
            aloitusvuoro += 1
        self.peli.uusi_kierros()
        self.uusi_peli_ikkuna = PeliIkkuna(self.peli, aloitusvuoro)
        self.uusi_peli_ikkuna.show()
        self.close()
        QTimer.singleShot(1000, self.peli_ikkuna.close)

    # Pelin päättyessä jatka peliä -nappi deaktivoituu
    # ja lopeta peli -nappi muuttuu palaa päävalikkoon
    # -napiksi, josta tämä metodi huolehtii
    def peli_loppu(self):
        vastaus = QMessageBox.question(self, "Vahvistus", "Haluatko varmasti palata takaisin alkuvalikkoon?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if vastaus == QMessageBox.StandardButton.Yes:
            self.aloitusikkuna = Aloitusikkuna()
            self.aloitusikkuna.show()
            self.close()
            QTimer.singleShot(1000, self.peli_ikkuna.close)
        if vastaus == QMessageBox.StandardButton.No:
            pass


# Oma luokka korttinapeille, jotta ne voidaan tunnistaa
# korttiensa perusteella
class KorttiNappi(QPushButton):

    def __init__(self, kortti):
        super().__init__()
        self.kortti = kortti

    def hanki_kortti(self):
        return self.kortti
