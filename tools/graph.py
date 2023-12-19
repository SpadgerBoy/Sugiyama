import networkx as nx
import matplotlib.pyplot as plt

"""绘制层次图"""
# 通过字典绘图
def graphLevelNet0(G0, file_name, crossing_num, showfig=True):

    G = nx.Graph()

    pos = {}
    for node in G0:
        pos[node] = G0[node]['pos']
        for out in G0[node]['out']:
            G.add_edge(node, out)

    # 根据节点数量设置画布大小、线的粗细、
    if len(G0) < 60:
        node_size = 200
        width = 3
        font_size = 10
        title_size = 20
        plt.figure(figsize=(10, 8))
        suffix = '.png'
    elif 60 <= len(G0) < 100:
        node_size = 200
        width = 3
        font_size = 10
        title_size = 40
        plt.figure(figsize=(20, 16))
        suffix = '.png'
    elif 100 <= len(G0) < 150:
        node_size = 200
        width = 3
        font_size = 10
        title_size = 80
        plt.figure(figsize=(40, 32))
        suffix = '.png'
    elif 150 <= len(G0) <= 200:
        node_size = 200
        width = 3
        font_size = 10
        title_size = 100
        plt.figure(figsize=(60, 48))
        suffix = '.png'
    else:
        node_size = 200
        width = 3
        font_size = 10
        title_size = 120
        plt.figure(figsize=(80, 64))
        suffix = '.png'

    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='#00ff00')
    nx.draw_networkx_edges(G, pos, width=width, edge_color='red')
    nx.draw_networkx_labels(G, pos, font_size=font_size)
    plt.title(f"Number of crossing: {crossing_num}", fontsize=title_size)

    plt.savefig(f'{file_name}{suffix}')
    plt.close()
    if showfig:
        plt.show()


def graphLevelNet(G0, file_name, showfig=True):

    G = nx.Graph()

    # print(L)       #[[1], [4, 3], ['V0J', 2, '9OX', 8, 'CE6', 'H1A'], ['3U7', 6, 7, 9], ['9NI', 10, 11], [5, 12]]
    pos = {}
    for node in G0:
        pos[node] = G0[node]['pos']
        for out in G0[node]['out']:
            G.add_edge(node, out)

    # 根据节点数量设置画布大小、线的粗细、
    if len(G0) < 60:
        node_size = 200
        width = 3
        font_size = 10
        plt.figure(figsize=(10, 8))
        suffix = '.png'
    elif 60 <= len(G0) < 100:
        node_size = 200
        width = 3
        font_size = 10
        plt.figure(figsize=(20, 16))
        suffix = '.png'
    else:
        node_size = 40
        width = 2
        font_size = 4
        plt.figure(figsize=(80, 64))
        suffix = '.svg'

    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='#00ff00')
    nx.draw_networkx_edges(G, pos, width=width, edge_color='red')
    nx.draw_networkx_labels(G, pos, font_size=font_size)
    plt.savefig(f'{file_name}{suffix}')
    plt.close()
    if showfig:
        plt.show()


# 通过图绘图

def graphLevelNetG(G, file_name, showfig=True):

    N = nx.Graph()

    # print(L)       #[[1], [4, 3], ['V0J', 2, '9OX', 8, 'CE6', 'H1A'], ['3U7', 6, 7, 9], ['9NI', 10, 11], [5, 12]]
    pos = {}
    for node in G:
        pos[node] = node.attr['pos']
    print(pos)
    N.add_edges_from(G.edges())

    # 根据节点数量设置画布大小、线的粗细、
    if len(G) < 60:
        node_size = 200
        width = 3
        font_size = 10
        plt.figure(figsize=(10, 8))
        suffix = '.png'
    elif 60 <= len(G) < 100:
        node_size = 200
        width = 3
        font_size = 10
        plt.figure(figsize=(20, 16))
        suffix = '.png'
    else:
        node_size = 40
        width = 2
        font_size = 4
        plt.figure(figsize=(80, 64))
        suffix = '.svg'

    nx.draw_networkx_nodes(N, pos, node_size=node_size, node_color='#00ff00')
    nx.draw_networkx_edges(N, pos, width=width, edge_color='red')
    nx.draw_networkx_labels(N, pos, font_size=font_size)
    plt.savefig(f'{file_name}{suffix}')
    plt.close()
    if showfig:
        plt.show()


if __name__ == '__main__':
    pass
