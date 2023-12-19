from sugiyama import *
from tools.graph import graphLevelNet
from tools.readCSV import read_csv
from tools.count_crossings import count_crossings
from tools.writeCSV import *
import os


if __name__ == '__main__':

    inPath = 'outputs/200/'  # 原始路径
    outPath = inPath + 'test_png_sug/'  # 输出路径
    os.makedirs(outPath, exist_ok=True)
    files = os.listdir(inPath + 'test_csv/')
    files.sort(key=lambda x: int(x.split('_')[0]))
    for file in files:
        print(file)

        filename = file.split('.')[0]  # filename = 20_6_3
        N = int(filename.split('_')[0])
        #if N > 12 or N < 11:
            #continue

        # 读取csv中的数据     G中存储的是字典结构的图数据，L0表示初始时每层的节点顺序
        in_path_csv = inPath + 'test_csv/' + file
        G, L0 = read_csv(in_path_csv)

        # 绘制原图
        G = convertGridToCart(G, L0)
        # in_path_png = inPath + 'test_png/' + filename
        # graphLevelNet(G, in_path_png, showfig=False)


        # 交叉最小化     L表示交叉最小化后每层的节点顺序
        L = twoLevelCrossMin(G, L0)

        # 绘制交叉最小化后的图
        G = convertGridToCart(G, L)

        Ga = dict2nxg(G)
        crossing_num = count_crossings(Ga)

        out_path_png = outPath + filename
        graphLevelNet0(G, out_path_png, crossing_num, showfig=True)

        # 将计算出的图写入csv
        # out_path_csv = outPath + 'csv/' + file
        # write_dict_to_csv(G, out_path_csv)

