"""
===============================================================================
 Project:      Python Graph Plotter
 File:         plotWidget.py
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

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Signal, QObject, QThread, QTimer

class PlotUpdateThread(QThread):
    """
    Thread per aggiornare il grafico senza bloccare la UI
    """
    update_signal = Signal()

    def __init__(self, interval=50):
        super().__init__()

        self.interval = interval

        self.running = True

    def run(self):
        """
        Esegue l'aggiornamento periodico del grafico
        """
        while self.running:
            self.update_signal.emit()
            self.msleep(self.interval)

    def stop(self):
        """
        Ferma il thread in modo sicuro
        """
        self.running = False

        self.quit()
        self.wait()

class LivePlotWidget(QObject):
    toggle_min = Signal(bool)
    toggle_max = Signal(bool)
    update_min_value = Signal(float)
    update_max_value = Signal(float)

    def __init__(self, graphics_view: QGraphicsView, model, max_visible_points=100):
        """
        Inizializza il grafico e lo integra nella QGraphicsView.
        """
        super().__init__()

        self.model = model
        self.graphics_view = graphics_view
        self.max_visible_points = max_visible_points  # Numero massimo di punti visibili nella finestra

        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Creiamo il widget di PyQtGraph
        self.plot_widget = pg.PlotWidget()
        self.scene.addWidget(self.plot_widget)

        # Linea del grafico
        self.curve = self.plot_widget.plot([], [], pen="y")

        # Configuriamo interazioni
        self.plot_widget.setMouseEnabled(x=True, y=True)  # Zoom e pan liberi
        self.plot_widget.setLimits(xMin=0)  # Evita di andare a sinistra di 0

        # Scatter plot per i punti con colore variabile
        self.scatter = pg.ScatterPlotItem(size=7, pen=pg.mkPen(None))
        self.plot_widget.addItem(self.scatter)

        # Connetto gli eventi hover e click ai metodi
        self.scatter.sigHovered.connect(self.show_tooltip)
        self.scatter.sigClicked.connect(self.show_tooltip)

        # Linee orizzontali interattive
        self.min_line = pg.InfiniteLine(angle=0, movable=True, pen="r", label="Min", labelOpts={"position": 0.1})
        self.max_line = pg.InfiniteLine(angle=0, movable=True, pen="g", label="Max", labelOpts={"position": 0.9})

        self.plot_widget.addItem(self.min_line)
        self.plot_widget.addItem(self.max_line)

        # Linee orizzontali inizialmente disabilitate
        self.min_line.setVisible(False)
        self.max_line.setVisible(False)

        # Connessione degli eventi delle linee orizzontali
        self.min_line.sigDragged.connect(self.min_line_moved)
        self.max_line.sigDragged.connect(self.max_line_moved)

        # Soglie iniziali
        self.min_threshold = -1000
        self.max_threshold = 1000

        # Thread per l'aggiornamento del grafico
        self.update_thread = PlotUpdateThread(interval=50)
        self.update_thread.update_signal.connect(self.update_plot)
        self.update_thread.start()

        # Creo un testo per il valore dei punti
        self.value_label = pg.TextItem("", anchor=(0.5, 1.5), color="w")
        self.plot_widget.addItem(self.value_label)
        self.value_label.setVisible(False)

    def update_plot(self):
        """
        Aggiunge un nuovo valore e aggiorna il grafico senza perdere i dati.
        """
        x_data, y_data = self.model.get_data()

        if not x_data or not y_data:
            return

        y_data = np.array(y_data)
        x_data = np.array(x_data)

        self.curve.setData(x_data, y_data)

        colors = np.full(len(y_data), pg.mkBrush("y"), dtype=object)  # Default: Giallo
        colors[y_data < self.min_threshold] = pg.mkBrush("r")  # Sotto soglia
        colors[y_data > self.max_threshold] = pg.mkBrush("r")  # Sopra soglia

        self.scatter.setData(
            x = x_data,
            y = y_data,
            brush = [pg.mkBrush(c) for c in colors],
            hoverable = True
        )

        # Mantiene la finestra visibile senza cancellare i dati vecchi
        if len(x_data) > self.max_visible_points:
            self.plot_widget.setXRange(x_data[-self.max_visible_points], x_data[-1], padding=0)

    def show_tooltip(self, scatter, points):
        """
        Mostra il valore del punto quando il mouse passa sopra.
        """
        if points is not None and len(points) > 0:
            point = points[0]  # Prendi il primo punto vicino al mouse
            x, y = point.pos()

            # Sposta il label sopra il punto e mostra il valore
            self.value_label.setText(f"📍 {y:.2f}")
            self.value_label.setPos(x, y)
            self.value_label.setVisible(True)  # Mostra il valore

        else:
            self.value_label.setVisible(False)  # Nascondi se non ci sono punti

    # def on_point_clicked(self, scatter, points):
    #     """
    #     Gestisce il click su un punto e stampa il valore.
    #     """
    #     if points:
    #         point = points[0]
    #         x, y = point.pos()
    #         print(f"⚡ Punto cliccato! X: {x:.2f}, Y: {y:.2f}")

    def clear_plot(self):
        """
        Cancella il grafico rimuovendo tutti i dati
        """
        self.curve.setData([], [])
        self.scatter.setData([])

    def min_line_moved(self):
        """
        Quando la linea del minimo viene trascinata, aggiorna la UI
        """
        self.update_min_value.emit(self.min_line.value())
        self.update_plot()

    def max_line_moved(self):
        """
        Quando la linea del massimo viene trascinata, aggiorna la UI
        """
        self.update_max_value.emit(self.max_line.value())
        self.update_plot()

    def toggle_min_visibility(self, enabled):
        """
        Mostra o nasconde la linea del minimo
        """
        self.min_line.setVisible(enabled)

    def toggle_max_visibility(self, enabled):
        """
        Mostra o nasconde la linea del massimo
        """
        self.max_line.setVisible(enabled)

    def set_min_value(self, value):
        """
        Imposta manualmente il valore della linea del minimo
        """
        self.min_threshold = value
        self.min_line.setValue(value)
        self.update_plot()

    def set_max_value(self, value):
        """
        Imposta manualmente il valore della linea del massimo
        """
        self.max_threshold = value
        self.max_line.setValue(value)
        self.update_plot()
