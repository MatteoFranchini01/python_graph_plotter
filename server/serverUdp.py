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

import socket
import time
import random
import threading

class UDPServer:
    def __init__(self, host="127.0.0.1", tcp_port=6000, udp_port=5005):
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port

        self.variables = ["Temperatura", "Pressione", "Umidità", "Velocità", "Altitudine"]

        self.selected_variable = None

    def handle_client(self, conn):
        """
        Invia la lista delle variabili al client via TCP
        """
        variables_str = ",".join(self.variables)
        conn.sendall(variables_str.encode())

        while True:
            try:
                data = conn.recv(1024)

                if not data:
                    break

                command = data.decode().strip()

                if command in self.variables:
                    self.selected_variable = command

                    print(f"Variabile selezionata: {self.selected_variable}")

                elif command == "STOP_UDP":
                    print("Flusso UDP fermato dal client")
                    self.selected_variable = None

            except Exception as e:
                print(f"Errore TCP: {e}")
                break

    def start_tcp_server(self):
        """
        Avvia il server TCP per comunicare con il client
        """
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind((self.host, self.tcp_port))
        tcp_sock.listen(1)

        print(f"Server TCP in ascolto su {self.host}:{self.tcp_port}")

        conn, _ = tcp_sock.accept()

        print("Client connesso")

        self.handle_client(conn)

    def start_udp_server(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            if self.selected_variable:
                value = random.uniform(-10, 10)

                message = f"{self.selected_variable}:{value}"

                udp_sock.sendto(message.encode(), (self.host, self.udp_port))

            time.sleep(0.1)

    def start(self):
        threading.Thread(target=self.start_tcp_server, daemon=True).start()
        threading.Thread(target=self.start_udp_server, daemon=True).start()
