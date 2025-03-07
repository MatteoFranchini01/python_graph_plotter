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
from PySide6.QtWidgets import (
    QGraphicsView, QCheckBox, QDoubleSpinBox, QListView, QAbstractItemView,
    QPushButton, QMessageBox, QGridLayout, QWidget
)
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

from src.uiLoader import UiLoader
from src.graph.plotWidget import LivePlotWidget
from src.model.ModelData import ModelData

class DataReceiver(QObject):
    """
    Segnale per aggiornare il grafico nel thread principale.
    """
    data_received = Signal(str, float)  # Segnale per variabile e valore ricevuto

class MainController(QObject):
    MAX_GRAPHS = 4  # Numero massimo di grafici visualizzabili
    BASE_UDP_PORT = 5005  # Porta di base per la comunicazione UDP

    alert_signal = Signal(str)  # Segnale per gli alert su MacOS

    def __init__(self):
        super().__init__()

        self.ui = UiLoader.load_ui("ui/mainwindow.ui")

        # Riferimenti agli elementi dell'interfaccia utente
        self.graphics_container = self.ui.findChild(QWidget, "graphicsContainer")
        self.listView = self.ui.findChild(QListView, "listView")
        self.stopRegBtn = self.ui.findChild(QPushButton, "stopRegButton")

        # Layout per i grafici in griglia
        self.layout = QGridLayout()
        self.graphics_container.setLayout(self.layout)

        self.model = ModelData()
        self.plots = {}  # Dizionario per tenere traccia dei grafici attivi
        self.selected_variables = {}  # Variabili selezionate e relative socket/thread

        # Configurazione della QListView come lista con checkbox
        self.listView.setSelectionMode(QAbstractItemView.NoSelection)
        self.listView.clicked.connect(self.on_variable_selected)

        # Connessione al server TCP per ottenere la lista delle variabili
        self.host = "127.0.0.1"
        self.tcp_port = 6000

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((self.host, self.tcp_port))

        self.receive_variable_list()

        self.alert_box = None  # Variabile per l'alert attuale
        self.alert_signal.connect(self.show_alert)

    def listen_udp(self, variable_name, port):
        """
        Avvia un thread UDP per ogni variabile selezionata, su una porta differente.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ✅ Evita errori di indirizzo in uso
        sock.bind((self.host, port))  # Assegna una porta unica per ogni variabile

        print(f"✅ Thread UDP avviato per {variable_name} sulla porta {port}")  # DEBUG

        while variable_name in self.selected_variables:
            try:
                data, _ = sock.recvfrom(1024)
                message = data.decode().strip()
                parts = message.split(":")
                if len(parts) == 2:
                    var_name, value_str = parts
                    value = float(value_str)

                    print(f"📥 Ricevuto: {var_name} = {value}")  # DEBUG

                    if var_name in self.selected_variables:
                        # Aggiunge il dato al modello
                        x_value = len(self.model.get_data(var_name)[0])  # Conta i punti attuali
                        self.model.add_data(var_name, x_value, value)  # ✅ Salva nel modello

                        print(f"💾 Dato salvato nel modello: {var_name} (X={x_value}, Y={value})")  # DEBUG

                        # Emetti il segnale per aggiornare il grafico
                        self.selected_variables[var_name]["receiver"].data_received.emit(var_name, value)
            except Exception as e:
                print(f"⚠️ Errore ricezione UDP {variable_name}: {e}")

    def receive_variable_list(self):
        """
        Riceve la lista delle variabili dal server e la popola nella QListView.
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
        Quando l'utente seleziona una variabile, avvia un nuovo thread UDP e invia la richiesta al server.
        """
        item = self.variable_model.itemFromIndex(index)
        if item.isCheckable():
            checked = item.checkState() == Qt.Checked
            selected_variable = item.text()

            if checked:
                if len(self.selected_variables) >= self.MAX_GRAPHS:
                    self.show_alert("⚠️ Massimo 4 variabili selezionabili! Deseleziona una variabile per aggiungerne un'altra.")
                    item.setCheckState(Qt.Unchecked)
                    return

                # Invia la richiesta al server per iniziare a inviare dati per questa variabile
                print(f"📤 Inviando al server: {selected_variable}")  # DEBUG
                self.tcp_sock.sendall(selected_variable.encode())

                # Assegna una porta UDP unica
                port = self.BASE_UDP_PORT + len(self.selected_variables)

                self.selected_variables[selected_variable] = {
                    "thread": threading.Thread(target=self.listen_udp, args=(selected_variable, port), daemon=True),
                    "receiver": DataReceiver(),
                    "port": port
                }
                self.selected_variables[selected_variable]["thread"].start()
                self.selected_variables[selected_variable]["receiver"].data_received.connect(self.on_data_received)

                self.add_graph(selected_variable)

            else:
                print(f"🛑 Stop invio dati per: {selected_variable}")  # DEBUG
                self.tcp_sock.sendall(f"STOP:{selected_variable}".encode())

                self.remove_graph(selected_variable)
                if selected_variable in self.selected_variables:
                    del self.selected_variables[selected_variable]

            self.update_layout()


    def add_graph(self, variable_name):
        """
        Aggiunge un nuovo grafico per la variabile selezionata.
        """
        plot_widget = LivePlotWidget(QGraphicsView(), self.model)
        self.plots[variable_name] = plot_widget
        self.layout.addWidget(plot_widget.graphics_view)

    def remove_graph(self, variable_name):
        """
        Rimuove il grafico quando una variabile viene deselezionata e chiude la connessione UDP.
        """
        if variable_name in self.plots:
            plot_widget = self.plots.pop(variable_name)
            self.layout.removeWidget(plot_widget.graphics_view)
            plot_widget.graphics_view.deleteLater()

        # Chiudi il thread UDP
        if variable_name in self.selected_variables:
            self.selected_variables[variable_name]["thread"] = None  # ✅ Termina il thread
            del self.selected_variables[variable_name]


    def update_layout(self):
        """
        Aggiorna la distribuzione dei grafici in base alle variabili selezionate.
        """
        row_col_map = {1: (1, 1), 2: (1, 2), 3: (2, 2), 4: (2, 2)}
        num_vars = len(self.selected_variables)
        rows, cols = row_col_map.get(num_vars, (1, 1))

        for i, (var, plot) in enumerate(self.plots.items()):
            self.layout.addWidget(plot.graphics_view, i // cols, i % cols)

    def on_data_received(self, variable_name, value):
        """
        Gestisce il dato ricevuto e aggiorna il modello e il grafico corrispondente.
        """
        print(f"📡 Segnale ricevuto per {variable_name}: {value}")  # DEBUG

        if variable_name in self.plots:
            x_value = len(self.model.get_data(variable_name)[0])  # Conta quanti punti ha già
            self.model.add_data(variable_name, x_value, value)  # Aggiunge il dato al modello
            print(f"📊 Aggiornamento grafico per {variable_name}")  # DEBUG
            self.plots[variable_name].update_plot(variable_name)  # Aggiorna solo il grafico corretto
        else:
            print(f"⚠️ Variabile {variable_name} ricevuta ma non trovata nei grafici.")

    def show_alert(self, message):
        """
        Mostra un avviso se si superano le 4 variabili selezionate.
        """
        if self.alert_box and self.alert_box.isVisible():
            self.alert_box.setText(message)
        else:
            self.alert_box = QMessageBox()
            self.alert_box.setIcon(QMessageBox.Warning)
            self.alert_box.setWindowTitle("Limite Grafici")
            self.alert_box.setText(message)
            self.alert_box.setWindowModality(Qt.NonModal)
            self.alert_box.setAttribute(Qt.WA_DeleteOnClose)
            self.alert_box.finished.connect(self.reset_alert_box)
            self.alert_box.show()
            self.alert_box.raise_()
            self.alert_box.activateWindow()

    def reset_alert_box(self):
        """
        Resetta la variabile alert_box quando l'alert viene chiuso.
        """
        self.alert_box = None

    def show(self):
        """
        Mostra l'interfaccia utente
        """

        self.ui.show()
