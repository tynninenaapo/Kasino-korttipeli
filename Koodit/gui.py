from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


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

        self.paa_widget = QWidget()
        self.layout = QVBoxLayout()

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.paa_widget)
        self.paa_widget.setLayout(self.layout)
        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()