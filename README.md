## Witnet Library
This library is light client implementation for witnet node, capacible  of directly interacting with witnet node.

### Features

- Allows to send proto messages to witnet node.
- Performs handshake with witnet node.
- Iterate over the nodes in witnet network in a DAG(directed acyclic graph)

### How to use
Performing handshake with witnet node.
```python
from witnet_lib.witnet_client import WitnetClient
client = WitnetClient()
client.handshake("127.0.0.1:21337")
client.close()
```

Listening to messages from witnet node.
```python
#After performing handshake with node.
msg = client.tcp_handler.receive_witnet_msg() # this returns serialized message from node
parsed_msg = client.msg_handler.parse_msg(msg) # we need to parse the message
print(prased_msg.kind)
print(parsed_msg.kind)
```

Sending message to witnet node.
```python
#After performing handshake with node.
cmd = client.msg_handler.version_cmd() # this returns a version message
print(cmd)
msg = client.msg_handler.serialize(cmd)# this returns serialized messsage ready to be sent to node
client.tcp_handler.send(msg)
msg_from_node = client.tcp_handler.receive_witnet_msg() # this returns only one whole message from node
msg_from_node_with_msg_len = client.tcp_handler.receive(30) # this returns x bytes from connection stream
```

Mapping all nodes in the network (DAG fashion)
```python
from witnet_lib import map_nodes
peers = map_nodes.start_mapping_workers(3) # number of connections allowed to be created in parallel
print(peers)
```