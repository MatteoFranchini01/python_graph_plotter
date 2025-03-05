from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QFile


class UiLoader:

    @staticmethod
    def load_ui(ui_file: str) -> QWidget:
        """
        Carica un file .ui e restituisce il widget root
        """
        loader = QUiLoader()

        file = QFile(ui_file)

        if not file.open(QFile.ReadOnly):
            raise FileNotFoundError(f"Impossibile aprire il file UI: {ui_file}")

        widget = loader.load(file)

        file.close()

        if not widget:
            raise ValueError(f"Errore nel caricamento del file UI: {ui_file}")

        return widget
