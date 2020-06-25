from witnet_lib.witnet_client import WitnetClient
from witnet_lib.logger import log
from queue import Queue
import threading




class MapNodes():
    def __init__(self, config, peer_addrs):
        self.peer_addrs = peer_addrs
        self.config = config

        # https://www.geeksforgeeks.org/queue-in-python/
        self.queue = Queue(maxsize=0)
        for peer_addr in peer_addrs: 
            self.queue.put(peer_addr)
        self.visited_nodes = set()

        # https://www.educative.io/edpresso/what-are-locks-in-python
        self.queue_lock = threading.Lock()
        self.set_lock = threading.Lock()

    def worker(self, worker_num):
        log.info(f"Starting worker {worker_num}")

        while True:
            try:
                # https://stackoverflow.com/questions/21320621/python-queue-block-timeout-does-not-timeout-any-idea-why
                peer = self.queue.get(block=True, timeout=5)
            except:
                return

            log.info(f"worker {worker_num}: peer {peer}")
            if peer in self.visited_nodes:
                continue
            # create client
            client = WitnetClient(self.config)
            try:
                client.handshake(peer)
                peers = client.get_peers()
                client.close()
            except:
                peers = []
            log.info(peers)

            # queue lock
            self.queue_lock.acquire()
            print(f"Acquiring queue lock: worker {worker_num}")
            for p in peers:
                if p not in self.visited_nodes:
                    self.queue.put(p)
            self.queue_lock.release()

            # set lock
            self.set_lock.acquire()
            print(f"Acquiring set lock: worker {worker_num}")
            self.visited_nodes.add(peer)
            self.set_lock.release()

    def start_mapping_workers(self, num):
        threads = []
        for i in  range(num):
            threads.append ( threading.Thread(target=self.worker, args=(i, ) ) )
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        return self.visited_nodes