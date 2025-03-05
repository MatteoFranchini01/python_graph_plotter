# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication

from src.controllers.mainWindowController import MainController


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainController = MainController()

    mainController.show()

    sys.exit(app.exec())
