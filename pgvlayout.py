import math, os
import random,csv
import networkx as nx
from tools.writeCSV import write_dict_to_csv
from sugiyama import convertGridToCart, twoLevelCrossMin
from tools.graphLib import graph2dict, dict2pgvg, dict2nxg
from tools.graph import graphLevelNet0, graphLevelNet
from tools.count_crossings import count_crossings
from tools.readCSV import read_csv
import pygraphviz as pgv
import win32file as wfile
import matplotlib.pyplot as plt
from tools.coordinate_homogenization import coordinate_homogenization, get_node_level_list


# 通过节点数N确定层数L的范围
def get_L(N):
    L_list = []
    if N <= 15:
        L_list = [3, 4]
    elif 15 < N <= 20:
        L_list = [4, 5]
    elif 20 < N <= 25:
        L_list = [i for i in range(5, 6)]
    elif 25 < N <= 30:
        L_list = [i for i in range(6, 8)]
    elif 30 < N <= 55:
        L_list = [i for i in range(6, 9)]
    elif 55 <= N <= 60:
        L_list = [i for i in range(9, 13)]
    elif 60 < N <= 80:
        L_list = [i for i in range(12, 15)]
    elif 80 < N <= 100:
        L_list = [i for i in range(10, 16)]
    elif 100 < N <= 160:
        L_list = [i for i in range(12, 16)]
    elif 160 < N <= 200:
        L_list = [i for i in range(15, 21)]
    elif 200 < N <= 250:
        L_list = [i for i in range(18, 22)]
    elif 250 < N <= 400:
        L_list = [i for i in range(20, 26)]
    elif 400 < N <= 600:
        L_list = [i for i in range(25, 36)]

    return L_list


# 节点分层
def random_layer_assignment(N, L):  # N节点总数，L层数

    a = math.floor(N / (2 * L))
    b = math.floor(N / (0.8 * L))
    # print(f'range:{a}~{b}')

    layers = []
    remaining_nodes = N

    for i in range(L - 1):
        max_nodes = min(remaining_nodes - (L - i - 1) * a, b)
        nodes_in_layer = random.randint(a, max_nodes)
        layers.append(nodes_in_layer)
        remaining_nodes -= nodes_in_layer

    if remaining_nodes > b:
        layers.append(b)
        div = (remaining_nodes - b) // (L)
        mod = (remaining_nodes - b) % (L)
        for i in range(L):
            layers[i] += div
        for i in range(mod):
            layers[i] += 1
    else:
        layers.append(remaining_nodes)

    num = 0
    for i in layers:
        num += i
    if num == N:
        return layers
    else:
        raise ValueError("Cannot satisfy the given constraints.")


# 随机生成边，并检测其是否为连通图，如果是则返回
def generate_connected_graph(N, L, nodes_per_layer):
    G = nx.DiGraph()

    node_id = 0
    for i in range(L):
        for j in range(nodes_per_layer[i]):
            G.add_node(node_id)
            node_id += 1

    # 创建连接矩阵
    connections = [[False] * N for _ in range(N)]

    # 连接相邻层的节点
    pre_node = 0  # 记录第i层前节点总数
    L0 = []  # L0 记录每层中各个节点的序号
    for i in range(L - 1):
        current_layer_nodes = list(range(sum(nodes_per_layer[:i]), sum(nodes_per_layer[:i + 1])))
        next_layer_nodes = list(range(sum(nodes_per_layer[:i + 1]), sum(nodes_per_layer[:i + 2])))

        L0.append(current_layer_nodes)
        if i == L - 2:
            L0.append(next_layer_nodes)

        for j, current_node in enumerate(current_layer_nodes):
            # 随机选择要连接的下一层节点
            if nodes_per_layer[i + 1] > 3:
                out_degree = random.randint(1, 2)
            else:
                # out_degree = random.randint(1, len(next_layer_nodes))
                out_degree = 1
            connected_nodes = random.sample(
                range(pre_node + nodes_per_layer[i], pre_node + nodes_per_layer[i] + nodes_per_layer[i + 1]),
                out_degree)
            # print(current_node, connected_nodes)
            for out_node in connected_nodes:
                G.add_edges_from([(current_node, out_node)])
                # 在连接矩阵中进行标记
                connections[current_node][out_node] = True
                connections[out_node][current_node] = True

        pre_node += nodes_per_layer[i]

    # 检查图的连通性
    visited = [False] * N
    stack = [0]  # 从节点0开始遍历
    visited[0] = True

    while stack:
        current = stack.pop()
        for neighbor in range(N):
            if connections[current][neighbor] and not visited[neighbor]:
                stack.append(neighbor)
                visited[neighbor] = True

    if False in visited:
        return None, None  # 图不连通

    return G, L0


# 完成图布局，与绘图，返回图字典
def pgvg(N, filename):
    G = pgv.AGraph(directed=True)

    G.graph_attr['rankdir'] = 'BT'

    for node in N.nodes():
        G.add_node(node, fontsize=10, width=0.3, fontcolor='#000000', shape='circle', style='filled',
                   fillcolor='#00ff00')
    for edge in N.edges():
        G.add_edge(edge, color='red', penwidth=1)

    G.layout(prog='dot')

    if filename is not None:
        G.draw(filename, prog="dot")

    return G


# 将布局好的图的坐标记录到对应的字典中
def addpos(G, G0):
    graph_attrs = G.graph_attr
    w = float(graph_attrs["bb"].split(',')[2])
    h = float(graph_attrs["bb"].split(',')[3])
    for node in G.nodes():
        attrs = G.get_node(node).attr
        x0 = float(attrs["pos"].split(",")[0])
        y0 = float(attrs["pos"].split(",")[1])
        x = math.floor(x0 / w * 10000) / 10000
        y = math.floor(y0 / h * 10000) / 10000
        # print(node, x, y)
        G0[int(node)]['pos'] = [x, y]
    return G0


def csv2graph(inPath, outPath):
    # inPath = 'outputs/level1/test_csv/'  # 原始路径
    os.makedirs(outPath, exist_ok=True)
    files = os.listdir(inPath)
    files.sort(key=lambda x: int(x.split('_')[0]))
    for file in files:
        print(file)

        filename = file.split('.')[0]  # filename = 20_6_3
        N = int(filename.split('_')[0])
        # if N > 12 or N < 11:
        # continue

        # 读取csv中的数据     G中存储的是字典结构的图数据，L0表示初始时每层的节点顺序
        csv_path = inPath + file
        G, L0 = read_csv(csv_path)

        # 绘制原图
        G = convertGridToCart(G, L0)
        png_path = outPath + filename
        graphLevelNet(G, png_path, showfig=False)


def run(G, L0, NL, output_dir, form='train'):

    N, L, num_connected_graph= NL[0], NL[0], NL[2]
    # 将图结构转换为字典结构
    G0 = graph2dict(G.edges(), L0)  # G0 = { 0：{'level': 1, 'in':[], 'out':[]}, ......}

    if form == 'test':

        # 计算坐标，并将坐标加入G1
        G1 = convertGridToCart(G0, L0)  # G0 = { 0：{'level': 1, 'in':[], 'out':[], 'pos':[] }, ......}

        Ga = dict2nxg(G1)  # 字典转换为图
        crossing_numO = count_crossings(Ga)
        # 画原图
        png_dir = f'{output_dir}/test_png/'
        os.makedirs(png_dir, exist_ok=True)
        graphLevelNet0(G1, png_dir + f'{N}_{L}_{num_connected_graph}', crossing_numO, showfig=False)

        # 写入csv
        csv_dir = f'{output_dir}/test_csv/'
        os.makedirs(csv_dir, exist_ok=True)
        write_dict_to_csv(G1, csv_dir + f'{N}_{L}_{num_connected_graph}.csv')

        # 画sugiyama图
        sug_png_dir = f'{output_dir}/test_png_sugiyama/'
        L = twoLevelCrossMin(G1, L0)
        G_s = convertGridToCart(G1, L)
        Gb = dict2nxg(G_s)
        crossing_numS = count_crossings(Gb)
        graphLevelNet0(G, sug_png_dir + f'{N}_{L}_{num_connected_graph}', crossing_numS, showfig=False)

        # 画pgv图
        pgv_png_dir = f'{output_dir}/test_png_pgv/'
        os.makedirs(pgv_png_dir, exist_ok=True)
        new_G = pgvg(G, None)
        # new_G = pgvg(G, pgv_png_dir + f'{N}_{L}_{num_connected_graph}.png')
        G2 = addpos(new_G, G1)
        Gc = dict2nxg(G2)  # 字典转换为图
        crossing_numP = count_crossings(Gc)

        # 坐标均匀化
        nodes_level = get_node_level_list(Gc)
        Gd = coordinate_homogenization(Gc, nodes_level)

        G3 = G2
        for node in Gd.nodes():
            # print(node, Gb.nodes()[node]['pos'])
            G3[node]['pos'] = Gd.nodes()[node]['pos']
        graphLevelNet0(G3, pgv_png_dir + f'{N}_{L}_{num_connected_graph}', crossing_numP, showfig=False)

        return crossing_numO, crossing_numS, crossing_numP

    if form == 'train':
        png_dir = f'{output_dir}/train_png/'
        os.makedirs(png_dir, exist_ok=True)
        new_G = pgvg(G, png_dir + f'{N}_{L}_{num_connected_graph}.png')

        # 将布局好的图的坐标记录到对应的字典中
        G2 = addpos(new_G, G0)
        # 写入csv
        csv_dir = f'{output_dir}/train_csv/'
        os.makedirs(csv_dir, exist_ok=True)
        write_dict_to_csv(G2, csv_dir + f'{N}_{L}_{num_connected_graph}.csv')


if __name__ == '__main__':

    # csv2graph('./outputs/test1/', './outputs/test1_png/')

    print("OLD max open files: {0:d}".format(wfile._getmaxstdio()))
    wfile._setmaxstdio(8192)  # !!! COMMENT this line to reproduce the crash !!!
    print("NEW max open files: {0:d}".format(wfile._getmaxstdio()))

    # 输出路径
    output_dir = 'outputs/200'
    os.makedirs(output_dir, exist_ok=True)

    f = open(output_dir + '/crossing_num.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['Name', 'Original', 'PGV', 'Sugiyama'])

    # N 为节点总数， L为层次数量
    for N in range(250, 251, 1):

        # 获取分层
        L_list = get_L(N)
        # L_list = [15, 16, 17, 18, 19, 20]
        for L in L_list:

            num_connected_graph = 0
            # 达到数量退出
            while num_connected_graph < 1:

                # 随机分层
                layers = random_layer_assignment(N, L)  # N = 20, L = 5: layers = [5,4,5,3,3]
                # 生成连通图G
                G, L0 = generate_connected_graph(N, L,
                                                 layers)  # G是图，L0 = [[0,1,2,3,4], [5,6,7,8], [9,10,11,12,13], [14,15,16], [17,18,19]]

                # 如果G不是连通图, 跳过
                if G is None:
                    continue

                num_connected_graph += 1
                print(N, L, num_connected_graph)

                crossing_numO, crossing_numS, crossing_numP = run(G, L0, [N, L, num_connected_graph], output_dir, form='test')
                writer.writerow([f'{N}_{L}_{num_connected_graph}', crossing_numO, crossing_numP, crossing_numS])

                # run(G, L0, [N, L, num_connected_graph], output_dir, form='train')
