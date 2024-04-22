import sys

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

from source.screens.main_screen import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
