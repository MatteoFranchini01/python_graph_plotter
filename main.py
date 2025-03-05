# This Python file uses the following encoding: utf-8
import sys
import threading

from PySide6.QtWidgets import QApplication

from src.controllers.mainWindowController import MainController
from server.serverUdp import UDPServer


def start_server():
    server = UDPServer()

    server.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    server_thread = threading.Thread(target=start_server, daemon=True)

    server_thread.start()

    mainController = MainController()

    mainController.show()

    sys.exit(app.exec())
