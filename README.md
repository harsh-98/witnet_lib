## Witnet Library
This library is light client implementation for witnet node, capable  of directly interacting with witnet node. ( See [Witnet.io](https://witnet.io/) for more information )

### Features

- Allows sending proto messages to witnet node.
- Performs handshake with witnet node.
- Iterates over the nodes in witnet network in a DAG(directed acyclic graph) fashion

### How to use
Performing handshake with witnet node.
```python
from witnet_lib.witnet_client import WitnetClient
from witnet_lib.utils import AttrDict

# Setting config
config = AttrDict()
config.update({
    "genesis_sec": 1592996400,
    "magic": 36162,
    "sender_addr": "127.0.0.1:21341",
    "time_per_epoch": 45,
})

client = WitnetClient(config)
client.handshake("127.0.0.1:21337")
client.close()
```

Listening to messages from witnet node.
```python
#After performing handshake with node.
msg = client.tcp_handler.receive_witnet_msg() # this returns serialized message from node
parsed_msg = client.msg_handler.parse_msg(msg) # we need to parse the message
print(parsed_msg)
print(parsed_msg.kind)
```

The connection is of `keep alive` type, so messages are continually sent from witnet node. To listen for all messages:
```python
while True:
    msg = client.tcp_handler.receive_witnet_msg() # this returns serialized message from node
    parsed_msg = client.msg_handler.parse_msg(msg)
    print(parsed_msg)
``` 

Sending message to witnet node.
```python
#After performing handshake with node.
cmd = client.msg_handler.version_cmd("127.0.0.1:21337") # this returns a version message
print(cmd)
msg = client.msg_handler.serialize(cmd)# this returns serialized messsage ready to be sent to node
client.tcp_handler.send(msg)
msg_from_node = client.tcp_handler.receive_witnet_msg() # this returns only one whole message from node
msg_from_node_with_msg_len = client.tcp_handler.receive(30) # this returns x bytes from connection stream
```

Mapping all nodes in the network (DAG fashion)
```python
from witnet_lib import utils
from witnet_lib.map_nodes  import MapNodes
config = utils.AttrDict()
config.update({
    "genesis_sec": 1592996400,
    "magic": 36162,
    "sender_addr": "127.0.0.1:21341",
    "time_per_epoch": 45,
})

mapper = MapNodes(config, ["127.0.0.1:21337"]) # provide initialisation peers
all_nodes = mapper.start_mapping_workers(3) # number of connections allowed to be created in parallel
print(all_nodes)
```