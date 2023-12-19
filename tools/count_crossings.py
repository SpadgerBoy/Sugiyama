import networkx as nx
from shapely.geometry import LineString
import math


# 判断两条边是否相交的函数
def do_edges_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    line1 = LineString([(x1, y1), (x2, y2)])
    line2 = LineString([(x3, y3), (x4, y4)])
    return line1.intersects(line2)


def count_crossings(G):
    crossings = 0
    edges = list(G.edges())

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            edge1 = edges[i]
            edge2 = edges[j]
            u1, v1 = edge1
            u2, v2 = edge2

            # 获取边的起点和终点的坐标
            x1, y1 = G.nodes[u1]['pos']
            x2, y2 = G.nodes[v1]['pos']
            x3, y3 = G.nodes[u2]['pos']
            x4, y4 = G.nodes[v2]['pos']

            # 判断两条边是否相交
            if do_edges_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                crossings += 1

    # 获取每个节点的度
    degrees = G.degree()
    for node, degree in degrees:
        if degree > 1:
            deg = int(math.factorial(degree) / (2 * math.factorial(degree - 2)))
            crossings -= deg

    return crossings


if __name__ == '__main__':
    # 创建一个示例图
    G = nx.Graph()
    G.add_edges_from([(1, 3), (1, 4), (1, 5), (1, 6), (2, 4)])

    # 设置节点的坐标属性
    G.nodes[1]['pos'] = (1, 0)
    G.nodes[2]['pos'] = (2, 0)
    G.nodes[3]['pos'] = (0, 1)
    G.nodes[4]['pos'] = (1, 1)
    G.nodes[5]['pos'] = (2, 1)
    G.nodes[6]['pos'] = (3, 1)

    # 计算边的交叉节点数量
    crossings = count_crossings(G)
    print("边的交叉节点数量:", crossings)