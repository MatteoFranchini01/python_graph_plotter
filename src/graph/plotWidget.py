import pyqtgraph as pg

import numpy as np

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene

class LivePlotWidget:

    def __init__(self, graphics_view: QGraphicsView):
        """Inizializza il grafico e lo integra nella QGraphicsView."""

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

    def update_plot(self, new_value):
        """Aggiunge un nuovo valore e aggiorna il grafico senza perdere i dati."""

        # Aggiungiamo il nuovo valore ai dati completi
        if len(self.full_data_x) == 0:
            self.full_data_x = np.array([0])

            self.full_data_y = np.array([new_value])

        else:
            self.full_data_x = np.append(self.full_data_x, self.full_data_x[-1] + 1)

            self.full_data_y = np.append(self.full_data_y, new_value)

        # Manteniamo la finestra visibile, senza cancellare i dati
        self.view_range = [self.full_data_x[-1] - self.max_visible_points, self.full_data_x[-1]]

        # Evitiamo di andare in negativo
        if self.view_range[0] < 0:
            self.view_range[0] = 0

        # Aggiorniamo il grafico con tutti i dati ma mostrando solo la finestra visibile
        self.curve.setData(self.full_data_x, self.full_data_y)

        self.plot_widget.setXRange(*self.view_range, padding=0)
