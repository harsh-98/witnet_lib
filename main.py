from witnet_lib.map_nodes import MapNodes
from witnet_lib import utils

if __name__ == "__main__":
    config = utils.AttrDict({
        "genesis_sec": 159555600,
        "magic": 3029,
        "sender_addr": "127.0.0.1:21341",
        "time_per_epoch": 45,
    })
    mapper = MapNodes(config, ["127.0.0.1:21337"])
    all_nodes, active_nodes = mapper.start_mapping_workers(3)
    print(all_nodes)
    with open("active.json",'w') as f:
        json.dump(active_nodes, f)
    with open('all_nodes.json', 'w') as f:
        json.dump(list(all_nodes), f)
