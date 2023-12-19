import csv


'''读取csv文件，将其转换为dict格式G，并记录每层的节点L'''


def read_csv(path):

    file = path.split('/')[-1]
    N = int(file.split('_')[0])
    L_n = int(file.split('_')[1])
    # print(N, L_n)

    f = open(path, 'r')
    reader = csv.reader(f)

    G = {}
    L0 = [[] for i in range(L_n)]

    i = 0
    for row in reader:
        if i > 0:
            node = int(row[0])
            level = int(row[1])
            G[node] = {'pos': eval(row[2]), 'in': eval(row[3]), 'out': eval(row[4]), 'level': level}
            # eval()函数将字符串转换为列表格式
            L0[level-1].append(node)
        i += 1

    return G, L0


if __name__ == '__main__':
    read_csv("input/csv/20_4_7.csv")