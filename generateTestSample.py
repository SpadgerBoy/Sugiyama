import math, os
import random
import networkx as nx
from tools.writeCSV import write_dict_to_csv
from sugiyama import convertGridToCart
from tools.graphLib import graph2dict
import pygraphviz as pgv

'''生成测试图，并记录到csv文件中'''


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


# 随机生成边，可能是非连通图
def generate_graph(L, nodes_per_layer, epsilon):
    G = nx.DiGraph()
    node_id = 0
    for i in range(L):
        for j in range(nodes_per_layer[i]):
            G.add_node(node_id)
            node_id += 1

    for i in range(L-1):
        current_layer_nodes = list(range(sum(nodes_per_layer[:i]), sum(nodes_per_layer[:i + 1])))
        next_layer_nodes = list(range(sum(nodes_per_layer[:i + 1]), sum(nodes_per_layer[:i + 2])))
        for node in current_layer_nodes:
            max = len(next_layer_nodes)//2
            if max >= 2:
                random_number = random.random()
                if random_number > epsilon:
                    out_degree = random.randint(1, 2)
                else:
                    out_degree = random.randint(2, max)
            else:
                out_degree = random.randint(1, len(next_layer_nodes))
            out_edges = random.sample(next_layer_nodes, out_degree)
            # G.add_edges_from([(node, next_node) for next_node in out_edges])
            for next_node in out_edges:
                G.add_edges_from([(node, next_node)])

    return G


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
    pre_node = 0        # 记录第i层前节点总数
    L0 = []             # L0 记录每层中各个节点的序号
    for i in range(L - 1):
        current_layer_nodes = list(range(sum(nodes_per_layer[:i]), sum(nodes_per_layer[:i + 1])))
        next_layer_nodes = list(range(sum(nodes_per_layer[:i + 1]), sum(nodes_per_layer[:i + 2])))

        L0.append(current_layer_nodes)
        if i == L-2:
            L0.append(next_layer_nodes)

        for j, current_node in enumerate(current_layer_nodes):
            # 随机选择要连接的下一层节点
            if nodes_per_layer[i + 1] > 3:
                # out_degree = random.randint(1, 5)
                out_degree = random.randint(1, 2)
            else:
                # out_degree = random.randint(1, len(next_layer_nodes))
                out_degree = 1
            connected_nodes = random.sample(range(pre_node + nodes_per_layer[i], pre_node + nodes_per_layer[i] + nodes_per_layer[i + 1]), out_degree)
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


def pgvg(N, filename):
    G = pgv.AGraph(directed=True)
    for node in N.nodes():
        G.add_node(node, fontsize=10, width=0.3, fontcolor='#000000', shape='circle', style='filled', fillcolor='#00ff00')
    for edge in N.edges():
       G.add_edge(edge, color='red', penwidth=1)

    G.layout(prog='dot')

    G.draw(filename, prog="dot")

    return G


if __name__ == '__main__':
    num_connected_graph = 0
    # N 为节点总数， L为层次数量
    for i in range(1000):
        for N in range(17, 18, 1):
            if N < 15:
                L = 0
            elif N ==16:
                L = 4
            elif N ==17:
                L = 5

            '''
            elif 20 < N < 40:
                L = random.randint(4, 6)
            elif 40 <= N < 60:
                L = random.randint(6, 8)
            elif 60 <= N < 100:
                L = random.randint(6, 10)
            elif 100 <= N < 150:
                L = random.randint(8, 16)
            elif 150 <= N < 300:
                L = random.randint(12, 18)
            elif 300 <= N < 450:
                L = random.randint(16, 24)
            elif 450 <= N < 550:
                L = random.randint(18, 30)'''
            # 随机分层
            layers = random_layer_assignment(N, L)      # N = 20, L = 5: layers = [5,4,5,3,3]
            # 生成连通图G
            G, L0 = generate_connected_graph(N, L, layers)      # G是图，L0 = [[0,1,2,3,4], [5,6,7,8], [9,10,11,12,13], [14,15,16], [17,18,19]]

            if num_connected_graph == 15:
                break

            # 如果G不是连通图, 跳过
            if G is None:
                continue
            num_connected_graph += 1
            '''png_dir = 'outputs/train_png/'
            os.makedirs(png_dir, exist_ok=True)
            pgvg(G, png_dir + f'{N}_{L}_{i}.png')'''

            # 将图结构转换为字典结构
            G0 = graph2dict(G.edges(), L0)          # G0 = { 0：{'level': 1, 'in':[], 'out':[]}, ......}

            # 计算坐标，并将坐标加入G0
            G0 = convertGridToCart(G0, L0)               # G0 = { 0：{'level': 1, 'in':[], 'out':[], 'pos':[] }, ......}

            # 写入csv
            csv_dir = 'outputs/train_csv0/'
            os.makedirs(csv_dir, exist_ok=True)
            write_dict_to_csv(G0, csv_dir + f'{N}_{L}_{num_connected_graph}.csv')


