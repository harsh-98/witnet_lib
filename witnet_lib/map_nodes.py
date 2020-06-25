from witnet_lib.witnet_client import WitnetClient
from witnet_lib.logger import log
from queue import Queue
import threading

# https://www.geeksforgeeks.org/queue-in-python/
queue = Queue(maxsize=0) 
queue.put("127.0.0.1:21337")
visited_nodes = set()


# https://www.educative.io/edpresso/what-are-locks-in-python
queue_lock = threading.Lock()
set_lock = threading.Lock()
def worker(config, worker_num):
    log.info(f"Starting worker {worker_num}")

    while True:
        try:
            # https://stackoverflow.com/questions/21320621/python-queue-block-timeout-does-not-timeout-any-idea-why
            peer = queue.get(block=True, timeout=5)
        except:
            return

        log.info(f"worker {worker_num}: peer {peer}")
        if peer in visited_nodes:
            continue
        # create client
        client = WitnetClient(config)
        try:
            client.handshake(peer)
            peers = client.get_peers()
            client.close()
        except:
            peers = []
        log.info(peers)

        # queue lock
        queue_lock.acquire()
        print(f"Acquiring queue lock: worker {worker_num}")
        for p in peers:
            if p not in visited_nodes:
                queue.put(p)
        queue_lock.release()

        # set lock
        set_lock.acquire()
        print(f"Acquiring set lock: worker {worker_num}")
        visited_nodes.add(peer)
        set_lock.release()



def start_mapping_workers(config, num):
    threads = []
    for i in  range(num):
        threads.append ( threading.Thread(target=worker, args=(config,i, ) ) )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    return visited_nodes