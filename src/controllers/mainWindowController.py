import random
import sys
import threading
import socket

from PySide6.QtCore import QTimer

from PySide6.QtWidgets import QGraphicsView, QCheckBox, QDoubleSpinBox
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
        self.checkMax = self.ui.findChild(QCheckBox, "maxLineCheckBox")
        self.checkMin = self.ui.findChild(QCheckBox, "minLineCheckBox")
        self.spinMax = self.ui.findChild(QDoubleSpinBox, "maxSpinBox")
        self.spinMin = self.ui.findChild(QDoubleSpinBox, "minSpinBox")

        # Configurazione delle double spin box
        self.spinMax.setMinimum(-1000.0)
        self.spinMax.setMaximum(1000.0)
        self.spinMin.setMinimum(-1000.0)
        self.spinMax.setMaximum(1000.0)

        self.model = ModelData()
        self.plot = LivePlotWidget(self.graphics_view, self.model)

        # Collego i segnali della UI ai metodi del grafico
        self.checkMin.toggled.connect(self.plot.toggle_min_visibility)
        self.checkMax.toggled.connect(self.plot.toggle_max_visibility)
        self.spinMin.valueChanged.connect(self.plot.set_min_value)
        self.spinMax.valueChanged.connect(self.plot.set_max_value)

        # Collego i segnali del grafico alla UI
        self.plot.update_min_value.connect(self.spinMin.setValue)
        self.plot.update_max_value.connect(self.spinMax.setValue)

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
