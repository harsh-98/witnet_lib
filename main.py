from witnet_lib.map_nodes import MapNodes
from witnet_lib import utils

if __name__ == "__main__":
    config = utils.AttrDict()
    config.update({
        "genesis_sec": 1592996400,
        "magic": 36162,
        "sender_addr": "127.0.0.1:21341",
        "time_per_epoch": 45,
    })
    mapper = MapNodes(config, ["127.0.0.1:21337"])
    all_nodes, active_nodes = mapper.start_mapping_workers(3)
    print(all_nodes)
    print("Acitve nodes:", active_nodes)