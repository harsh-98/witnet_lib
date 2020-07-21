import socket
import random
from witnet_lib.logger import log
from witnet_lib.utils import resolve_url


class TCPSocket:

    def __init__(self, node_addr, timeout=0):
        self.sock_id = random.randint(10, 1000)
        self.node_addr = node_addr
        self.timeout = timeout

    def connect(self):
        host, port = resolve_url(self.node_addr)
        log.info("Connecting to %s:%s", host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.timeout:
            self.sock.settimeout(self.timeout)
        try:
            self.sock.connect((host, port))
        except OSError as err:
            log.fatal("Disconnect %s", err)

    def send(self, msg):
        """for sending byte msg

        Args:
            msg (bytes): message in bytes

        Returns:
            bool: whether sent successfully or not
        """
        log.debug("Sending [>] %s", msg)
        try:
            self.sock.send(msg)
            return True
        except Exception as err:
            log.error("Failed in sending to %s %s", self.node_addr, err)
            # close if error, this will prevent close_wait state of socket
            self.close()
            return False

    def receive(self, x=4096):
        """receives x bytes

        Args:
            length (int, optional): number of bytes to receive from connection. Defaults to 4096.

        Returns:
            bytes: message in bytes
            bool: received_or_not
        """
        if self.sock.fileno() == -1:
            return b'', False
        """ 
        connection reset from peer 
        throughs error handle that.
        """
        try:
            msg = self.sock.recv(x)
        except ConnectionResetError as err:
            log.debug("Connection reset while receiving: %s", err)
            self.close()
            return b'', False
        """
        if connection is terminated since socket.close() is not called
        the socket at witnet-net-api side is in close_wait state and
        recv is return b'', so return False  for
         stopping rece_iteratively iterativey calling receive method
        https://stackoverflow.com/questions/16745409/what-does-pythons-socket-recv-return-for-non-blocking-sockets-if-no-data-is-r#:~:text=It%20means%20that%20your%20non,the%20other%20end%20may%20send).
        """
        if len(msg) == 0:
            self.close()
            return b'', False

        log.debug("Receiving [<] %s", msg)
        return msg, True

    def rece_iteratively(self, total_len, _print=False):
        """for iteratively recieving until `total_len` number of bytes are received

        Args:
            total_len (int): length of message to receive
            _print (bool, optional): [description]. Defaults to False.

        Returns:
            bytes: message in bytes
            bool: received_or_not
        """
        reced_len = 0
        full_msg = b''
        while reced_len < total_len:
            msg, reced = self.receive(total_len-reced_len)
            if _print:
                # TODO redundant print for testing
                print(f"\n Socket: {self.sock_id} lengths",
                      total_len, reced_len)
            if not reced:
                return full_msg, False
            full_msg += msg
            reced_len = len(full_msg)
        return full_msg, True

    def receive_witnet_msg(self):
        """receiving a witnet message
        first 4 bytes denotes the `x` length of the message
        then x number of bytes is the actual message

        Returns:
            bytes: message in bytes
            bool: received_or_not
        """
        # first four bytes are the length of the actual proto msg
        len_bytes, reced = self.rece_iteratively(4)

        # TODO redundant for testing
        # print(f"Length: {self.sock_id}", len_bytes)

        if not reced:
            return b'', False
        msg_len = int.from_bytes(len_bytes, byteorder='big')

        """ 
        check for terminating connection, this is a fall-safe
        shouldn't be called but if the msg_len is wrong, connection should be terminated
        """
        if msg_len > 2**25:
            return b'', False

        # receive total msg
        return self.rece_iteratively(msg_len)

    def close(self):
        if not self.is_closed():
            self.sock.close()

    def is_closed(self):
        return self.sock.fileno() == -1
