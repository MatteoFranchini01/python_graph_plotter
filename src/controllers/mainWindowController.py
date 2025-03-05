import random
import sys
import threading
import socket

from PySide6.QtCore import QTimer

from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Signal, QObject

from src.uiLoader import UiLoader
from src.graph.plotWidget import LivePlotWidget
from src.uiLoader import UiLoader
from src.model.ModelData import ModelData

class DataReceiver(QObject):
    """
    Segnale per aggiornare il grafico nel thread principale
    """
    data_received = Signal(float)

class MainController:

    def __init__(self):
        self.ui = UiLoader.load_ui("ui/mainwindow.ui")

        self.graphics_view = self.ui.findChild(QGraphicsView, "graphicsView")
        self.model = ModelData()
        self.plot = LivePlotWidget(self.graphics_view, self.model)

        self.host = "127.0.0.1"
        self.port = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.receiver = DataReceiver()
        self.receiver.data_received.connect(self.on_data_received)

        self.thread = threading.Thread(target=self.listen_udp, daemon=True)
        self.thread.start()

        self.x_counter = 0
        self.update_counter = 0

    def listen_udp(self):
        while True:
            data, _ = self.sock.recvfrom(1024)

            try:
                value = float(data.decode().strip())

                self.receiver.data_received.emit(value)

                self.x_counter += 1

            except ValueError:
                print(f"Errore nella conversione del valore: {data}")

    def on_data_received(self, value):
        """
        Gestisce il dato ricevuto e aggiorna il grafico
        """
        self.model.add_data(self.x_counter, value)
        self.x_counter += 1

        self.update_counter += 1

        if self.update_counter % 2 == 0:
            self.plot.update_plot()

    def show(self):
        """
        Mostra l'interfaccia utente
        """

        self.ui.show()
