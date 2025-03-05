import random

from PySide6.QtCore import QTimer
# from PySide6.QtWigets import QGraphicsView

import PySide6.QtWidgets

from src.uiLoader import UiLoader
from src.graph.plotWidget import LivePlotWidget

from src.uiLoader import UiLoader


class MainController:

    def __init__(self):
        self.ui = UiLoader.load_ui("ui/mainwindow.ui")

        self.graphics_view = self.ui.findChild(PySide6.QtWidgets.QGraphicsView, "graphicsView")

        self.plot = LivePlotWidget(self.graphics_view)

        self.current_value = 0

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_data)

        self.timer.start(100)

    def update_data(self):
        """
        Simula un aggiornamento della variabile e aggiorna il grafico
        """
        self.current_value += random.uniform(-1, 1)

        self.plot.update_plot(self.current_value)

    def show(self):
        """
        Mostra l'interfaccia utente
        """

        self.ui.show()
