import socket
from datetime import datetime
from witnet_lib.logger import log
from witnet_lib.utils import resolve_url
import random
import threading
import time


class TCPSocket:

    def __init__(self, node_addr):
        self.node_addr = node_addr

    def connect(self):
        host, port = resolve_url(self.node_addr)
        log.info("Connecting to %s:%s", host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, msg):
        log.debug("Sending [>] %s", msg)
        try:
            self.sock.send(msg)
            return True
        except Exception as err:
            log.error("Failed in sending to %s %s", self.node_addr, err)
            return False

    def receive(self, length=4096):
        if self.sock.fileno() == -1:
            return b'', False
        msg = self.sock.recv(length)
        log.debug("Receiving [<] %s", msg)
        return msg, True

    def receive_witnet_msg(self):
        # first four bytes are the length of the actual proto msg
        length, reced = self.receive(4)
        if not reced:
            return b'', False
        total_len = int.from_bytes(length, byteorder='big')

        reced_len = 0
        total_msg = b''
        # receive total msg
        while reced_len < total_len:
            msg, reced = self.receive(total_len-reced_len)
            if not reced:
                return total_msg, False
            total_msg += msg
            reced_len = len(total_msg)
        return total_msg, True

    def close(self):
        self.sock.close()
