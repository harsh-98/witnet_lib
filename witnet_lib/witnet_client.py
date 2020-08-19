from witnet_lib.logger import log
from witnet_lib.proto_lib.witnet_msg import WitnetMsgHandler
from witnet_lib.tcp_handler import TCPSocket
# from witnet_lib.rpc_handler import RPC


class WitnetClient():

    def __init__(self, config):
        # Handle if persistent is not passed
        try:
            _ = config.persistent
        except Exception as err:
            #  log.error(err)
            config.persistent = False

        self.config = config
        self.persistent = config.persistent
        self.msg_handler = WitnetMsgHandler(self.config)
        # TODO
        # self.rpc_handler = RPC(config.rpc_addr)

    def handshake(self, peer_addr):
        # connect to peer
        self.peer_addr = peer_addr
        self.tcp_handler = TCPSocket(peer_addr)
        self.tcp_handler.connect()

        # TODO with testnet 0.9.2 consensus algorithm will be upgraded to support superblock and block checkpoint
        # self.rpc_handler.connect()
        # last_block = self.rpc_handler.get_blockchain()[0]
        # version_cmd = self.msg_handler.version_cmd(peer_addr, last_block)

        # send version to node
        version_cmd = self.msg_handler.version_cmd(peer_addr)
        version_msg = self.msg_handler.serialize(version_cmd)
        self.tcp_handler.send(version_msg)

        # receive verack from node
        self.tcp_handler.receive_witnet_msg()
        # receive version from node
        self.tcp_handler.receive_witnet_msg()

        # send verack to node
        verack_cmd = self.msg_handler.verack_cmd()
        verack_msg = self.msg_handler.serialize(verack_cmd)
        self.tcp_handler.send(verack_msg)

    def send_msg(self, msg):
        succeed = self.tcp_handler.send(msg)
        if not succeed and self.persistent:
            self.handshake(self.peer_addr)
            self.tcp_handler.send(msg)

    def receive_msg(self):
        """support persistent connection
        if message is not received retry once more if persistent connection is True

        Returns:
            bytes: returns whatever bytes are received, even if incomplete
        """
        msg, reced = self.tcp_handler.receive_witnet_msg()
        if not reced and self.persistent:
            self.handshake(self.peer_addr)
            msg, reced = self.tcp_handler.receive_witnet_msg()
        return msg

    def get_peers(self):
        # send get peer request to node
        get_peers_cmd = self.msg_handler.get_peers_cmd()
        get_peers_msg = self.msg_handler.serialize(get_peers_cmd)
        self.tcp_handler.send(get_peers_msg)
        i = 0
        while i < 10:
            msg = self.receive_msg()
            parsed_msg = self.msg_handler.parse_msg(msg)
            peers = self.msg_handler.parse_peers(parsed_msg)
            if len(peers) > 0:
                return peers
            i += 1
        return []

    def close(self):
        if not self.is_closed():
            self.tcp_handler.close()

    def is_closed(self):
        return self.tcp_handler.is_closed()
