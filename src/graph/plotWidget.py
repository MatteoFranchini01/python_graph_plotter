import pyqtgraph as pg

import numpy as np

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import QObject, Signal

class LivePlotWidget(QObject):
    toggle_min = Signal(bool)
    toggle_max = Signal(bool)
    update_min_value = Signal(float)
    update_max_value = Signal(float)

    def __init__(self, graphics_view: QGraphicsView, model):
        """
        Inizializza il grafico e lo integra nella QGraphicsView.
        """
        super().__init__()

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

        # Scatter plot per i punti con colore variabile
        self.scatter = pg.ScatterPlotItem(size=7, pen=pg.mkPen(None))
        self.plot_widget.addItem(self.scatter)

        # Connetto gli eventi hover e click ai metodi
        self.scatter.sigHovered.connect(self.show_tooltip)  #TODO: per ora questo non funziona
        self.scatter.sigClicked.connect(self.show_tooltip)

        # Linee orizzontali interattive
        self.min_line = pg.InfiniteLine(angle=0, movable=True, pen="r", label="Min", labelOpts={"position":0.1})
        self.max_line = pg.InfiniteLine(angle=0, movable=True, pen="g", label="Max", labelOpts={"position":0.9})

        self.plot_widget.addItem(self.min_line)
        self.plot_widget.addItem(self.max_line)

        # Linee orizzontali inizialmente disabilitate
        self.min_line.setVisible(False)
        self.max_line.setVisible(False)

        # Connessione degli eventi delle linee orizzontali
        self.min_line.sigDragged.connect(self.min_line_moved)
        self.max_line.sigDragged.connect(self.max_line_moved)

        # Manteniamo il riferimento alla vista corrente
        self.view_range = [0, self.max_visible_points]

        # Soglie iniziali
        self.min_threshold = -1000
        self.max_threshold = 1000

    def update_plot(self):
        """
        Aggiunge un nuovo valore e aggiorna il grafico senza perdere i dati.
        """
        x_data, y_data = self.model.get_data()

        self.curve.setData(x_data, y_data)

        # Determina i colori in base alle soglie
        colors = []
        for y in y_data:
            if y < self.min_threshold or y > self.max_threshold:
                colors.append(pg.mkBrush("r"))

            else:
                colors.append(pg.mkBrush("y"))

        spots = [{'pos': (x, y), 'brush': colors[i], 'size': 7} for i, (x, y) in enumerate(zip(x_data, y_data))]
        self.scatter.setData(spots)

        if len(x_data) > 100:
            self.plot_widget.setXRange(x_data[-100], x_data[-1], padding=0)

    def show_tooltip(self, scatter, points):
        """
        Mostra il valore del punto quando il mouse passa sopra
        """
        if points:
            point = points[0]

            x, y = point.pos()

            self.plot_widget.setToolTip(f"X: {x:.2f}, Y: {y:.2f}")

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

    def max_line_moved(self):
        """
        Quando la linea del massimo viene trascinata, aggiorna la UI
        """
        self.update_max_value.emit(self.max_line.value())

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

