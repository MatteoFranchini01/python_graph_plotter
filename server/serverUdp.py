import socket
import time
import random

class UDPServer:
    def __init__(self, host="127.0.0.1", port=5005):
        self.host = host

        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.counter = 0

    def start(self):
        """
        Invia dati casuali ogni 100ms
        """
        print(f"Server in ascolto su {self.host}:{self.port}")

        while self.counter < 500:
            value = random.uniform(-10, 10)

            message = f"{value}"

            self.sock.sendto(message.encode(), (self.host, self.port))

            time.sleep(0.1)

            self.counter += 1

            print(f"SERVER: counter {self.counter}")
