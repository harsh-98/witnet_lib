from witnet_lib import map_nodes

if __name__ == "__main__":
    all_nodes = map_nodes.start_mapping_workers(3)
    print(all_nodes)