
from sugiyama import *
from tools.graph import graphLevelNet
from tools.readCSV import read_csv
from tools.count_crossings import count_crossings
from tools.writeCSV import *
import os
import pygraphviz as pgv
import win32file as wfile
from pgvlayout import *
from tools.coordinate_homogenization import coordinate_homogenization, get_node_level_list

if __name__ == '__main__':

    form = 'sugiyama'  # or pgv
    inPath = 'outputs/200/'  # 原始路径
    outPath = inPath + 'test_png_' + form + '/'  # 输出路径
    os.makedirs(outPath, exist_ok=True)

    files = os.listdir(inPath + 'test_csv/')
    files.sort(key=lambda x: int(x.split('_')[0]))
    # k = 0

    f = open(inPath + '/crossing_num.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['Name', 'Original', 'Sugiyama'])

    for file in files:
        print(file)

        filename = file.split('.')[0]  # filename = 20_6_3
        N = int(filename.split('_')[0])
        L = int(filename.split('_')[1])
        num_connected_graph = int(filename.split('_')[2])

        # 读取csv中的数据     G中存储的是字典结构的图数据，L0表示初始时每层的节点顺序
        in_path_csv = inPath + 'test_csv/' + file
        G_1, L0 = read_csv(in_path_csv)

        # 原图
        G_2 = convertGridToCart(G_1, L0)
        Ga = dict2nxg(G_2)  # 字典转换为图
        crossing_numO = count_crossings(Ga)
        # 画原图
        png_dir = f'{inPath}/test_png/'
        os.makedirs(png_dir, exist_ok=True)
        graphLevelNet0(G_2, png_dir + f'{N}_{L}_{num_connected_graph}', crossing_numO, showfig=False)

        if form == 'sugiyama':
            # 交叉最小化     L表示交叉最小化后每层的节点顺序
            L0 = twoLevelCrossMin(G_2, L0)

            # 绘制交叉最小化后的图
            G_3 = convertGridToCart(G_2, L0)

            Ga = dict2nxg(G_3)
            crossing_numS = count_crossings(Ga)

            out_path_png = outPath + filename
            graphLevelNet0(G_3, outPath + filename, crossing_numS, showfig=True)

            writer.writerow([f'{N}_{L}_{num_connected_graph}', crossing_numO, crossing_numS])

        elif form == 'pgv':
            G = dict2pgvg(G_2)
            # new_G = pgvg(G, outPath + filename + '.png')
            new_G = pgvg(G, None)

            # 同规格绘图
            G_3 = addpos(new_G, G_2)
            Ga = dict2nxg(G_3)  # 字典转换为图
            crossing_numP = count_crossings(Ga)

            nodes_level = get_node_level_list(Ga)
            Gb = coordinate_homogenization(Ga, nodes_level)

            G_4 = G_3
            for node in Gb.nodes():
                # print(node, Gb.nodes()[node]['pos'])
                G_4[node]['pos'] = Gb.nodes()[node]['pos']
            graphLevelNet0(G_4, outPath + filename, crossing_numP, showfig=False)




