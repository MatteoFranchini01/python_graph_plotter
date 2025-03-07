"""
===============================================================================
 Project:      Python Graph Plotter
 File:         serverUdp.py
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
import random
import time

class UDPServer:
    def __init__(self, host="127.0.0.1", tcp_port=6000, base_udp_port=5005):
        self.host = host
        self.tcp_port = tcp_port
        self.base_udp_port = base_udp_port  # Porta iniziale per la trasmissione UDP
        self.variables = ["Temperatura", "Pressione", "Umidità", "Velocità", "Altitudine"]

        self.selected_variables = {}  # Dizionario per tenere traccia delle variabili selezionate e delle loro porte
        self.tcp_sock = None  # Socket TCP per la comunicazione con il client

    def handle_client(self, conn):
        """
        Invia la lista delle variabili al client via TCP e gestisce le selezioni.
        """
        variables_str = ",".join(self.variables)
        print(f"📡 Inviando lista variabili al client: {variables_str}")  # DEBUG
        conn.sendall(variables_str.encode())

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("⚠️ Connessione TCP chiusa dal client.")
                    break

                command = data.decode().strip()
                print(f"📥 Ricevuto comando dal client: {command}")  # DEBUG

                if command in self.variables:
                    if command in self.selected_variables:
                        print(f"⚠️ {command} è già selezionata.")
                        continue

                    udp_port = self.base_udp_port + len(self.selected_variables)
                    self.selected_variables[command] = udp_port

                    print(f"✅ Variabile selezionata: {command} → Porta UDP {udp_port}")

                    threading.Thread(target=self.start_udp_server, args=(command, udp_port), daemon=True).start()

                elif command == "STOP_UDP":
                    print("🛑 Flusso UDP fermato per tutte le variabili.")
                    self.selected_variables.clear()

                elif command.startswith("STOP:"):
                    variable_to_stop = command.split(":")[1]
                    if variable_to_stop in self.selected_variables:
                        print(f"🛑 Flusso UDP fermato per {variable_to_stop}")
                        del self.selected_variables[variable_to_stop]

            except Exception as e:
                print(f"❌ Errore TCP: {e}")
                break

    def start_tcp_server(self):
        """
        Avvia il server TCP per comunicare con il client.
        """
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind((self.host, self.tcp_port))
        self.tcp_sock.listen(1)

        print(f"📡 Server TCP in ascolto su {self.host}:{self.tcp_port}")

        while True:
            conn, _ = self.tcp_sock.accept()
            print("✅ Client connesso")
            self.handle_client(conn)

    def start_udp_server(self, variable_name, udp_port):
        """
        Invia dati randomici della variabile selezionata al client via UDP.
        """
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"📤 Thread UDP avviato per {variable_name} sulla porta {udp_port}")

        while variable_name in self.selected_variables:
            try:
                value = random.uniform(-10, 10)
                message = f"{variable_name}:{value}"
                udp_sock.sendto(message.encode(), (self.host, udp_port))
                print(f"📨 Inviato {variable_name}: {value} su {udp_port}")  # DEBUG
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Errore invio UDP {variable_name}: {e}")
                break

    def start(self):
        """
        Avvia il server TCP e i thread UDP in parallelo.
        """
        threading.Thread(target=self.start_tcp_server, daemon=True).start()
