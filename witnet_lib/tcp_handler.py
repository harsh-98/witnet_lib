import socket
from datetime import datetime
from witnet_lib.logger import log
import random
import threading
import time

class TCPSocket:
    sock_type = "connect"
    def __init__(self,sock_type="connect"):
               self.sock_type = sock_type
    def connect(self, node_addr):
        host , port = node_addr.split(":")
        port = int(port)
        if self.sock_type == "connect":
            log.info(f"Connecting to {host}:{port}")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

    def send(self, msg):
            log.debug(f"Sending [>] {msg}")
            self.sock.send(msg)

    def receive(self, length=4096):
        msg = self.sock.recv(length)
        log.debug(f"Receiving [<] {msg}")
        return msg
    def receive_witnet_msg(self):
        length = self.receive(4)
        rece_len = int.from_bytes(length, byteorder='big')
        return self.receive(rece_len)

    def close(self):
        self.sock.close()

    def listen(self, port):
        if self.sock_type == "listen":
            self.sock = socket.socket()
            self.sock.bind(('', port)) 
            self.sock.listen(5)
            log.info(f"Listening at {port}")