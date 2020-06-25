from witnet_lib.logger import log
from witnet_lib.proto_lib.witnet_msg import WitnetMsgHandler
from witnet_lib.tcp_handler import TCPSocket

class WitnetClient():
    
    def __init__(self,config):
        self.config = config
        self.msg_handler = WitnetMsgHandler(self.config)

    def handshake(self, peer_addr):
        # connect to peer 
        self.tcp_handler = TCPSocket("connect")
        self.tcp_handler.connect(peer_addr)

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

    def get_peers(self):
        # send get peer request to node
        get_peers_cmd = self.msg_handler.get_peers_cmd()
        get_peers_msg = self.msg_handler.serialize(get_peers_cmd)
        self.tcp_handler.send(get_peers_msg)

        while True:
            msg = self.tcp_handler.receive_witnet_msg()
            parsed_msg = self.msg_handler.parse_msg(msg)
            peers = self.msg_handler.parse_peers(parsed_msg)
            if len(peers) > 0 :
                return peers
    def close(self):
        self.tcp_handler.close()
