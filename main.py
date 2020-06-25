from witnet_lib import map_nodes, utils

if __name__ == "__main__":
    config = utils.AttrDict()
    config.update({
        "genesis_sec": 1590055200,
        "magic": 45507,
        "sender_addr": "127.0.0.1:21341",
        "time_per_epoch": 45,
    })
    all_nodes = map_nodes.start_mapping_workers(config, 3)
    print(all_nodes)