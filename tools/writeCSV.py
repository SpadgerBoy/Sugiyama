import csv
import os


def write_graph_to_csv(N, L, G, nodes_per_layer, tag):
    in_node_list = [ [] for i in range(N)]
    out_node_list = [ [] for i in range(N)]
    for (node, out_node) in G.edges():
        in_node_list[out_node].append(node+1)
        out_node_list[node].append(out_node+1)

    if not os.path.exists('csv'):
        os.mkdir('csv')
    file_path = f'csv/{N}_{L}_{tag}.csv'
    f = open(file_path, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['node', 'level', 'in', 'out'])
    node_index = 0
    for i in range(L):
        if i > 0:
            node_index += nodes_per_layer[i-1]
        for j in range(nodes_per_layer[i]):
            node = node_index+j
            writer.writerow([node+1, i+1, in_node_list[node], out_node_list[node]])
    f.close()


def write_dict_to_csv(G, file_path):

    f = open(file_path, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['node', 'level', 'pos', 'in', 'out'])

    for i, node in enumerate(G):
        # print(node)
        writer.writerow([i, G[i]['level'], G[i]['pos'], G[i]['in'], G[i]['out']])

    f.close()


if __name__ == '__main__':
    pass