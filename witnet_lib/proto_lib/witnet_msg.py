from datetime import datetime
import random
from witnet_lib.proto_lib import witnet_pb2
from witnet_lib.logger import log

def byte_ip(addr):
    ip, port = addr.split(":")
    port = int(port)
    ip = [int(i) for i in ip.split(".")]
    # print(hex(port))
    port =  list(bytes.fromhex(hex(port)[2:]))
    l = ip+port
    return bytes(l)

class WitnetMsgHandler():
    def __init__(self, config):
        self.magic = config.magic
        self.genesis_sec = config.genesis_sec
        self.sender_addr = config.sender_addr
        self.time_per_epoch = config.time_per_epoch
    def version_cmd(self, receiver_addr):
        now = datetime.now()
        utc_sec = now.strftime('%s')
        utc_sec = int(utc_sec)
        
        rece_addr_msg = witnet_pb2.Address()

        rece_addr_msg.address = byte_ip(self.sender_addr)
        send_addr_msg = witnet_pb2.Address()
        send_addr_msg.address = byte_ip(receiver_addr)
        version = witnet_pb2.Version()
        version.sender_address.CopyFrom(send_addr_msg)
        version.receiver_address.CopyFrom(rece_addr_msg)
        version.version = 1 
        version.capabilities = 1
        version.user_agent = b"full-node-desktop-edition".decode('utf-8')
        version.timestamp = utc_sec
        version.last_epoch = int((utc_sec - self.genesis_sec)/self.time_per_epoch) -1
        version.nonce = random.randint(10000000,100000000000000000) 
        
        cmd = witnet_pb2.Message.Command()
        cmd.Version.CopyFrom(version)
        return cmd
    
    def verack_cmd(self):
        verack = witnet_pb2.Verack()
        cmd = witnet_pb2.Message.Command()
        cmd.Verack.CopyFrom(verack)
        return cmd

    def get_peers_cmd(self):
        get_peers = witnet_pb2.GetPeers()
        cmd = witnet_pb2.Message.Command()
        cmd.GetPeers.CopyFrom(get_peers)
        return cmd

    def serialize(self, cmd):
        msg = witnet_pb2.Message()
        msg.magic = self.magic
        msg.kind.CopyFrom(cmd)
        serialized = msg.SerializeToString()
        bytes_len = len(serialized)
        length = bytes_len.to_bytes(4, byteorder='big')
        msg = length + serialized
        return msg

    def parse_msg(self, rece_bytes):
        msg = witnet_pb2.Message()
        msg.ParseFromString(rece_bytes)
        log.debug(msg)
        return msg
    
    def parse_peers(self, msg):
        peers = []
        if msg.kind.HasField("Peers"):
            for peer in msg.kind.Peers.peers:
                addr = peer.address
                ip, port = addr[:4], addr[4:]
                # from bytes convert to ip and port
                # data transferred over network in big endian
                ip = '.'.join([str(byt) for byt in ip])
                port = int.from_bytes(port, byteorder='big')

                peers.append(f"{ip}:{port}")
        
        return peers
        
        
