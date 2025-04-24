import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from gui import GUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec())

