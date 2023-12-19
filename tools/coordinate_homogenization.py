import networkx as nx


# 获取每层的节点名称
def get_node_level_list(H):
    max_level = 0
    for node in H.nodes(data=True):
        node_id, attr = node
        # print(node_id, attr)
        if max_level < attr['level']:
            max_level = attr['level']

    level_nodes = [[] for _ in range(max_level)]
    for node in H.nodes(data=True):
        node_id, attr = node
        # print(node_id, attr)
        level_nodes[attr['level'] - 1].append(node_id)
    # print(level_nodes)

    new_level_nodes = []
    for li in range(len(level_nodes)):
        x_li = {}
        for n in level_nodes[li]:
            # print(H.nodes()[n]['x'])
            x_li.update({n: H.nodes()[n]['pos'][0]})
        x_li = dict(sorted(x_li.items(), key=lambda x: x[1]))
        # print(x_li)
        new_level_nodes.append([key for key in x_li])
    # print(new_level_nodes)

    return new_level_nodes


# 坐标均匀化
def coordinate_homogenization(G, level):
    pos_dict = {}
    # get each level max width and overall max width
    maxW = max([len(l) for l in level])  #maxW = len( max(level, key = lambda l: len(l)) )

    xstep = 1. / maxW # abstand zwischen den spalten

    ystep = 1. / len(level)

    # get coord in datastructure
    y = ystep / 2.
    for l in level: # for each level l in level
        x = xstep/2. +  (maxW - len(l)) / (maxW*2.)  # start pos and centering + padding and centering

        for n in l: # for each node key in l
            pos_dict.update({n: (x, y)})       # levels in grid coordinates
            x += xstep
        y += ystep

    nx.set_node_attributes(G, pos_dict, 'pos')
    return G


if __name__ == '__main__':
    graph_path = "../graph_data/level40/level_15_4_5.graphml"
    G = nx.read_graphml(graph_path)

    # 将节点标签转换为整数，保留原始标签作为节点属性
    H = nx.convert_node_labels_to_integers(G)
    nodes_level = get_node_level_list(H)
    new_H = coordinate_homogenization(H, nodes_level)