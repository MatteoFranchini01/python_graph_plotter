import pyqtgraph as pg

import numpy as np

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene

class LivePlotWidget:

    def __init__(self, graphics_view: QGraphicsView, model):
        """
        Inizializza il grafico e lo integra nella QGraphicsView.
        """

        self.model = model

        self.graphics_view = graphics_view

        self.scene = QGraphicsScene()

        self.graphics_view.setScene(self.scene)

        # Creiamo il widget di PyQtGraph
        self.plot_widget = pg.PlotWidget()

        self.scene.addWidget(self.plot_widget)

        # Inizializza dati del grafico
        self.full_data_x = np.array([])  # Dati completi

        self.full_data_y = np.array([])

        self.max_visible_points = 100  # Numero massimo di punti visibili alla volta

        # Linea del grafico
        self.curve = self.plot_widget.plot([], [], pen="y")

        # Configuriamo interazioni
        self.plot_widget.setMouseEnabled(x=True, y=True)  # Zoom e pan liberi

        self.plot_widget.setLimits(xMin=0)  # Evita di andare a sinistra di 0

        # Manteniamo il riferimento alla vista corrente
        self.view_range = [0, self.max_visible_points]

    def update_plot(self):
        """
        Aggiunge un nuovo valore e aggiorna il grafico senza perdere i dati.
        """
        x_data, y_data = self.model.get_data()

        self.curve.setData(x_data, y_data)

        if len(x_data) > 100:
            self.plot_widget.setXRange(x_data[-100], x_data[-1], padding=0)

