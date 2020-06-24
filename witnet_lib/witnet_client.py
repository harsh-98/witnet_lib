from logger import log
from proto_lib.witnet_msg import Witnet_Msg
from tcp_handler import TCPSocket
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class Witnet_Client():
    
    def __init__(self):
        self.config = AttrDict()
        self.config.update({
            "genesis_sec": 1590055200,
            "magic": 45507,
            "sender_addr": "127.0.0.1:21341",
        })
        self.msg_handler = Witnet_Msg(self.config)

    def get_peers(self, peer_addr):
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

        # send get peer request to node
        get_peers_cmd = self.msg_handler.get_peers_cmd()
        get_peers_msg = self.msg_handler.serialize(get_peers_cmd)
        self.tcp_handler.send(get_peers_msg)

        while True:
            msg = self.tcp_handler.receive_witnet_msg()
            parsed_msg = self.msg_handler.parse_msg(msg)
            peers = self.msg_handler.parse_peers(parsed_msg)
            if len(peers) > 0 :
                self.tcp_handler.close()
                return peers

