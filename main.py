# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication

from src.controllers.mainWindowController import MainController
from server.serverUdp import UDPServer


if __name__ == "__main__":
    app = QApplication(sys.argv)

    server = UDPServer()
    server.start()

    mainController = MainController()
    mainController.show()

    sys.exit(app.exec())
