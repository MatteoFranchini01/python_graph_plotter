"""
===============================================================================
 Project:      Python Graph Plotter
 File:         mainWindowController.py
 Author:       Matteo Franchini
 Created:      05/03/2025
 License:      MIT License (c) 2025 Matteo Franchini
 Repository:   https://github.com/MatteoFranchini01/python_graph_plotter
===============================================================================
 MIT License

 Copyright (c) 2025 Matteo Franchini

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 IN THE SOFTWARE.
===============================================================================
"""

import threading
import socket

from PySide6.QtWidgets import QGraphicsView, QCheckBox, QDoubleSpinBox, QListView, QAbstractItemView, QPushButton, QMessageBox
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

class MainController(QObject):
    alert_signal = Signal(str)      # Funzionalità solo per MacOS

    def __init__(self):
        super().__init__()

        self.ui = UiLoader.load_ui("ui/mainwindow.ui")

        self.graphics_view = self.ui.findChild(QGraphicsView, "graphicsView")
        self.checkMax = self.ui.findChild(QCheckBox, "maxLineCheckBox")
        self.checkMin = self.ui.findChild(QCheckBox, "minLineCheckBox")
        self.alertMax = self.ui.findChild(QCheckBox, "alertMaxCheckBox")
        self.alertMin = self.ui.findChild(QCheckBox, "alertMinCheckBox")
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
        self.alertMax.stateChanged.connect(self.toggle_alert_max)
        self.alertMin.stateChanged.connect(self.toggle_alert_min)

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

        # Variabile per tracciare l'ultimo alert
        self.alert_box = None

        # Imposto le soglie iniziali
        self.alertMaxActive = False
        self.alertMinActive = False
        self.lastAlertTime = None

        self.alert_signal.connect(self.show_alert)      # Funzionalità solo per MacOS

        self.x_counter = 0
        self.update_counter = 0

    def toggle_alert_max(self, state):
        """
        Attiva o disattiva gli alert per il superamento del massimo
        """
        self.alertMaxActive = (state == 2)

    def toggle_alert_min(self, state):
        """
        Attiva o disattiva gli alert per il superamento del minimo
        """
        self.alertMinActive = (state == 2)

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

        if self.alertMaxActive and value > self.plot.max_threshold:
            self.show_alert(f"Valore sopra soglia: {value:.2f} > {self.plot.max_threshold:.2f}")

        if self.alertMinActive and value < self.plot.min_threshold:
            self.show_alert(f"Valore sotto soglia: {value:.2f} < {self.plot.min_threshold:.2f}")

        self.update_counter += 1

        if self.update_counter % 2 == 0:
            self.plot.update_plot()

    def show_alert(self, message):
        """
        Mostra un messaggio di alert con una finestra di dialogo
        """
        if self.alert_box and self.alert_box.isVisible():
            self.alert_box.setText(message)

        else:
            self.alert_box = QMessageBox()
            self.alert_box.setIcon(QMessageBox.Warning)
            self.alert_box.setWindowTitle("Alert valore fuori soglia")
            self.alert_box.setText(message)

            self.alert_box.setWindowModality(Qt.NonModal)  # Permette interazione con la UI sottostante
            self.alert_box.setAttribute(Qt.WA_DeleteOnClose)  # Chiude e libera la memoria quando

            # Connetto il segnale di chiusura alla funzione che resetta self.alert_box
            self.alert_box.finished.connect(self.reset_alert_box)

            self.alert_box.show()  # Usa show() per NON bloccare la UI
            self.alert_box.raise_()  # Porta la finestra in primo piano
            self.alert_box.activateWindow()  # Assicura che riceva il

    def reset_alert_box(self):
        """
        Resetta la variabile self.alert_box quando l'alert viene chiuso
        """
        self.alert_box = None

    def show(self):
        """
        Mostra l'interfaccia utente
        """

        self.ui.show()
