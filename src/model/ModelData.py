"""
===============================================================================
 Project:      Python Graph Plotter
 File:         modelData.py
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

class ModelData:
    def __init__(self):
        """Inizializza un dizionario per memorizzare i dati di ogni variabile"""
        self.data = {}  # Dizionario con struttura: {"Temperatura": {"x": [...], "y": [...]}, ...}

    def add_data(self, variable_name, x_value, y_value):
        """Aggiunge un nuovo dato alla variabile specificata"""
        if variable_name not in self.data:
            self.data[variable_name] = {"x": [], "y": []}

        self.data[variable_name]["x"].append(x_value)
        self.data[variable_name]["y"].append(y_value)

    def get_data(self, variable_name):
        """Restituisce i dati per la variabile specificata"""
        if variable_name in self.data:
            return self.data[variable_name]["x"], self.data[variable_name]["y"]
        return [], []

    def clear_data(self, variable_name):
        """Cancella i dati di una variabile specifica"""
        if variable_name in self.data:
            self.data[variable_name] = {"x": [], "y": []}

