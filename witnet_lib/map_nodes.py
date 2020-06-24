from witnet_client import Witnet_Client
from logger import log
from queue import Queue

# https://www.geeksforgeeks.org/queue-in-python/
queue = Queue(maxsize=0) 
queue.put("127.0.0.1:21337")
visited_nodes = set()
client = Witnet_Client()

while not queue.empty():
    peer = queue.get()
    if peer in visited_nodes:
        continue
    try:
        peers = client.get_peers(peer)
    except:
        peers = []
    log.info(peers)
    for p in peers:
        if p not in visited_nodes:
            queue.put(p)
    visited_nodes.add(peer)
print(visited_nodes)