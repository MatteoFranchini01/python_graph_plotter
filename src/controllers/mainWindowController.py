import threading
import socket

from PySide6.QtWidgets import QGraphicsView, QCheckBox, QDoubleSpinBox, QListView, QAbstractItemView, QPushButton
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

from src.uiLoader import UiLoader
from src.graph.plotWidget import LivePlotWidget
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
        self.listView = self.ui.findChild(QListView, "listView")
        self.stopRegBtn = self.ui.findChild(QPushButton, "stopRegButton")

        # Configurazione delle double spin box
        self.spinMax.setMinimum(-1000.0)
        self.spinMax.setMaximum(1000.0)
        self.spinMin.setMinimum(-1000.0)
        self.spinMax.setMaximum(1000.0)

        self.model = ModelData()
        self.plot = LivePlotWidget(self.graphics_view, self.model)

        # Collego i segnali della UI ai metodi del MainController
        self.stopRegBtn.clicked.connect(self.onStopRegBtnClicked)

        # Collego i segnali della UI ai metodi del grafico
        self.checkMin.toggled.connect(self.plot.toggle_min_visibility)
        self.checkMax.toggled.connect(self.plot.toggle_max_visibility)
        self.spinMin.valueChanged.connect(self.plot.set_min_value)
        self.spinMax.valueChanged.connect(self.plot.set_max_value)

        # Collego i segnali del grafico alla UI
        self.plot.update_min_value.connect(self.spinMin.setValue)
        self.plot.update_max_value.connect(self.spinMax.setValue)

        # Connessione con il server
        self.host = "127.0.0.1"
        self.udp_port = 5005
        self.tcp_port = 6000
        self.selected_variable = None

        # Comunicazione TCP per ottenere la lista di variabili
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((self.host, self.tcp_port))

        # Ricezione della lista di variabili
        self.receive_variable_list()

        # Configurazione della QListView come una lista con checkbox
        self.listView.setSelectionMode(QAbstractItemView.NoSelection)
        self.listView.clicked.connect(self.on_variable_selected)

        # Avvio del thread per ricevere dati UDP
        self.thread = threading.Thread(target=self.listen_udp, daemon=True)
        self.thread.start()

        self.x_counter = 0
        self.update_counter = 0

    def receive_variable_list(self):
        """
        Riceve la lista delle variabili dal server e la popola nella QListView
        """
        data = self.tcp_sock.recv(1024).decode().strip()

        variable_list = data.split(",")

        self.variable_model = QStandardItemModel()

        for var in variable_list:
            item = QStandardItem(var)
            item.setCheckable(True)
            item.setEditable(False)
            self.variable_model.appendRow(item)

        self.listView.setModel(self.variable_model)

    def on_variable_selected(self, index):
        """
        Quando l'utente seleziona una variabile, invia il nome al server via TCP
        """
        item = self.variable_model.itemFromIndex(index)

        if item.isCheckable():
            checked = item.checkState() == Qt.Checked
            selected_variable = item.text()

            if checked:
                if selected_variable != self.selected_variable:
                    self.selected_variable = selected_variable

                    self.model.clear_data()

                    self.plot.clear_plot()
                    self.plot.update_plot()

                    self.tcp_sock.sendall(selected_variable.encode())

            else:
                if selected_variable == self.selected_variable:
                    self.selected_variable = None

                    self.model.clear_data()

                    self.plot.clear_plot()

                    self.tcp_sock.sendall(b"STOP")

    def onStopRegBtnClicked(self):
        if self.selected_variable:
            self.tcp_sock.sendall(b"STOP_UDP")

            print("Flusso UDP fermato, il grafico rimane visibile")

    def listen_udp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.udp_port))

        self.receiver = DataReceiver()
        self.receiver.data_received.connect(self.on_data_received)

        while True:
            if not self.selected_variable:
                continue

            data, _ = self.sock.recvfrom(1024)

            try:
                message = data.decode().strip()

                parts = message.split(":")

                if len(parts) == 2:
                    var_name, value_str = parts
                    value = float(value_str)

                    self.receiver.data_received.emit(value)

                    self.x_counter += 1

                else:
                    raise ValueError("Formato messaggio non valido")

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
