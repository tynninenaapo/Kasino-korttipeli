import sys
from PyQt6.QtWidgets import QApplication
from gui import Aloitusikkuna


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Aloitusikkuna()
    sys.exit(app.exec())
