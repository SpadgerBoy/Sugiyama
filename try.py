from tools.graph import *
from tools.graphLib import *
import networkx as nx
import matplotlib.pyplot as plt
E = [(1, 3), (1, 4), (2, 6), (3, 2), (3, 7), (3, 8), (4, 5), (4, 6), (4, 8), (4, 9), (6, 10), (7, 10), (7, 11), (8, 7),
     (9, 11), (10, 12), (11, 12)]
pos1 = {1:(77.5, 0), 2:(177.5, 100), 3:(122.5, 50), 4:(45, 50), 5:(35, 100), 6:(160, 150), 7:(95, 150), 8:(85, 100), 9:(0, 150), 10:(150, 200), 11:(2.5, 200), 12:(87.5, 250)}
G0 = graphFromEdges(E)
'''G = nx.Graph()
for i, o in E:
    G.add_edge(i, o)

nx.draw_networkx_nodes(G, pos1, node_size=200, node_color='#00ff00')
nx.draw_networkx_edges(G, pos1, width=3, edge_color='red')
nx.draw_networkx_labels(G, pos1, font_size=10)
plt.savefig(f'Network-Simplex.png')
plt.close()
plt.show()'''

'''layout = nx.nx_pydot.graphviz_layout(G0, prog='neato')
plt.figure(figsize=(6, 4))
nx.draw(G0, pos=layout, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)
plt.title('Graph Layout')
plt.show()'''


import copy
import itertools
import random
import string
import math
from tools.graph import *
from tools.graphLib import *
from itertools import permutations

def toIndex(A, B):
    for a in A:
        if a in B:
            yield B.index(a)


def costMatrix(N, L1, L2):
    M = [ [ 0 for _ in L1 ] for _ in L1 ]

    for ((ui, u), (vi, v)) in itertools.combinations(enumerate(L1), 2):
        print(1, (ui, u), (vi, v))
        Eu = toIndex(N[u]['out'] + N[u]['in'], L2)   # get indices for edges from and to level 2
        Ev = toIndex(N[v]['out'] + N[v]['in'], L2)   # get indices for edges from and to level 2

        for uc_i, vc_i in itertools.product(Eu, Ev):
            print(3, uc_i, vc_i)
            if uc_i > vc_i:     # (s, d) if destination of u edge is further than destination of v edge:
                # in case u left to v, it's a crossing
                M[ui][vi] += 1
            if uc_i < vc_i:
                # in case v left to u, it's a crossing
                M[vi][ui] += 1

    return M


def crossSort(A, M):
    if len(A) < 2:
        return A
    
    p = math.floor(len(A) / 2)
    L = crossSort(A[:p], M)
    R = crossSort(A[p:], M)

    S = []
    li = ri = 0
    crossing_num = 0
    while li < len(L) and ri < len(R):
        l = L[li]
        r = R[ri]
        print("l:", l, "r:", r)

        if(M[l][r] <= M[r][l]):
            crossing_num += M[l][r]
            S += [l]    
            li += 1
        else:
            crossing_num += M[r][l]
            S += [r]
            ri += 1

    S += L[li:]
    S += R[ri:]

    return S


if __name__ == '__main__':
    G = {
        0: {'in': [], 'out': [3, 4]},
        1: {'in': [], 'out': [3]},
        2: {'in': [], 'out': [4]},
        3: {'in': [0, 1], 'out': []},
        4: {'in': [0, 2], 'out': []},
    }
    l1 = [0, 1, 2]
    l2 = [3, 4]

    B0 = l1
    T = l2

    permutations_lst = permutations(B0)

    for B in permutations_lst:
        M = costMatrix(G, T, B)
        print(M)
        T_i = crossSort(range(len(T)),M)  # not B = T, but B = sorted T => B = recMinCross(T, M), use as base for next iteration
        print(T_i)
        new_T = [T[i] for i in T_i]

        R = [B] + [new_T]  # append permutation with least crosses
        print('R:',R)




