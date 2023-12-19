import copy
import itertools
import random
import string
import math
from tools.graph import *
from tools.graphLib import *

# 1. Eliminate cycles
# 2. Assign nodes to levels
# 3. Minimize edge crosses
# 4. Assign nodes to cartesian coordinates
# 5. Restore original cycles

'''
1. Eliminate cycles, build succession with minimal count of backedge.
   (a) Save sources and sinks in two different lists
   (b) Remove source nodes successively and add to source list
   (c) remove sink nodes successively and add to sink list
   (d) chose next candidate according to in- and out-rank of node, rangOut = maxNode( [R_out(v) - R_in(v) for v in G] )
       (e) remove v from Graph and add to source list
'''
def cycleAnalysis(G):
    N = copy.deepcopy(G)    # graph will be altered... copy graph

    # printGraph(N)

    Sl, Sr = [], []     # Sl, Sr in Sugiyama et. al.


    while N:        # while N not empty

        sources = [ n for n in N if len(N[n]['in']) == 0 ]
        sinks = [ n for n in N if len(N[n]['out']) == 0 ]

        # (b)
        if sources:
            Sl += sources

            for n in sources:
                removeNode(N, n)    # remove all sinks

        # (c)
        elif sinks:
            Sr += sinks

            for n in sinks:
                removeNode(N, n)    # remove all sinks

        # (d)
        elif N:
            o = max(N, key = lambda n: len(N[n]['out']) - len(N[n]['in']) )    # get node with maximum rangOut 
            # (e)
            Sl += [ o ]
            removeNode(N, o)

    return Sl + Sr

# invert cyclic edge
def invertBackEdges(G, S):
    N = copy.deepcopy(G)    # graph will be altered... copy graph
    B = []  # backedges
    for i, n in enumerate(S):

        C = N[n]['out'] # children
        for c in C:
            j = S.index(c)
            if j < i:
                B += [ (n, c) ]
    
    twistEdges(N, B)

    return N

'''
2. Assign each node to horizontal Level
   (a) Determine sinks
   (b) Assign them to new level
   (c) Deleate all sinks from graph 
'''
# takes acyclic Graph
def levelAssignment(G):
    N = copy.deepcopy(G)

    L = []      # levels

    while N:    # while N not empty
        # (a)
        sinks = [ n for n in N if len(N[n]['out']) == 0 ]
    
        # (c)
        L += [ sinks ]      # L = []; L += [ ['A', 'B', 'C'] ] =>  L = [ ['A', 'B', 'C'] ]

        # (b)
        for n in sinks:
            removeNode(N, n)

    return [ x for x in reversed(L) ]

'''
  take (a, b) and if there lies a level between them (which they are not connected over):
    take a as from node, 
    create a new node
      connect that new node to a
    connect that new node to b
'''
# for multiple levels in between
def solveMidTransition(N, edge, L):
    (a, b) = edge

    # return the levels that lie between the node

    lfrom = N[a]['level']
    lto = N[b]['level']

    if lto < lfrom:
        step = -1
    else:
        step = 1

    removeEdges(N, [ (a, b) ])   # remove original edge

    u = a   # (u, v)
    for i in range(lfrom + step, lto, step):     # for levels between a and b
        v = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

        N[u]['out'] += [ v ]
        N[v] = {'in': [u], 'out': [], 'level': i, 'between': True }
        L[i] += [ v ]      # add to level
        u = v

    N[v]['out'] += [ b ]     # u is last created node... connect that one to b
    N[b]['in'] += [ u ]     # u is last created node... connect that one to b

    return N, L


def getInBetweenNodes(G, L):
    N = copy.deepcopy(G)

    for i, l in enumerate(L):
        for j in l:
            N[j]['level'] = i       # assign each node a level

    IB = []

    for nLevel, l in enumerate(L):
        for n in l:
            node = N[n]
            for c in node['out']:
                cLevel = N[c]['level']

                dif = math.fabs(cLevel - nLevel);    # if more than two level between 
                if dif > 1:
                    IB += [ (n, c) ]

    for (n, c) in IB:
        solveMidTransition(N, (n, c), L)

    return N, L


def toIndex(A, B):
    for a in A:
        if a in B:
            yield B.index(a)


def costMatrix(N, L1, L2):
    M = [ [ 0 for _ in L1 ] for _ in L1 ]

    for ((ui, u), (vi, v)) in itertools.combinations(enumerate(L1), 2):
        Eu = toIndex(N[u]['out'] + N[u]['in'], L2)   # get indices for edges from and to level 2
        Ev = toIndex(N[v]['out'] + N[v]['in'], L2)   # get indices for edges from and to level 2

        for uc_i, vc_i in itertools.product(Eu, Ev):
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
    while li < len(L) and ri < len(R):
        l = L[li]
        r = R[ri]

        if(M[l][r] <= M[r][l]):
            S += [l]
            li += 1
        else:
            S += [r]
            ri += 1

    S += L[li:]
    S += R[ri:]

    return S


# 两层交叉最小化
def twoLevelCrossMin(N, Levels):
    Lvl = [ x for x in Levels ]    # copy the list, just to make sure..

    R = [ Levels[-1] ]  # take over first entry.. it won't be modified

    B = Lvl.pop()       # 第i层
    while Lvl:
        T = Lvl.pop()   # 第i+1层

        M = costMatrix(N, T, B)
        T_i = crossSort(range(len(T)), M)       # not B = T, but B = sorted T => B = recMinCross(T, M), use as base for next iteration
        B = [ T[i] for i in T_i ]

        R += [ B ] # append permutation with least crosses

    return [ x for x in reversed(R) ]  # because of popping R is reversed


'''
# 两层交叉最小化
def twoLevelCrossMin(N, Levels):
    Lvl = [ x for x in Levels ]    # copy the list, just to make sure..

    R = [ Lvl[0] ]  # take over first entry.. it won't be modified

    for i in range(len(Lvl)):
        if i+1 == len(Lvl):
            continue
        B = Lvl[i]          # 第i层
        T = Lvl[i+1]        # 第i+1层

        M = costMatrix(N, T, B)
        T_i = crossSort(range(len(T)), M)       # not B = T, but B = sorted T => B = recMinCross(T, M), use as base for next iteration
        T = [ T[i] for i in T_i ]

        R += [ T ] # append permutation with least crosses

    return [ x for x in reversed(R) ]  # because of popping R is reversed
'''

# input:
#   nodes = { 'A': [[], [], []] }
#   levelGrid = [ [ [ 'A', 'B', 'C' ] ], .., [ 'X', 'Y', 'Z'] ]
#           'List of lists' or Grid of nodes, containing node keys(of dict)
# 坐标分配
def convertGridToCart(G, level):
    # get each level max width and overall max width
    maxW = max([len(l) for l in level])  #maxW = len( max(level, key = lambda l: len(l)) )

    xstep = 1. / maxW # abstand zwischen den spalten

    ystep = 1. / len(level)

    # get coord in datastructure
    y = ystep / 2.
    for l in level: # for each level l in level
        x = xstep/2. +  (maxW - len(l)) / (maxW*2.)  # start pos and centering + padding and centering

        for n in l: # for each node key in l
            G[n]['pos'] = [x, y]       # levels in grid coordinates
            x += xstep

        y += ystep
    return G




def sugiyama(G):
    # 解循环
    S = cycleAnalysis(G)
    # 再次插入回边
    N = invertBackEdges(G, S)   # invertierte Kanten braucht man nicht speichern, man nimmt einfahc den original graph..
    # 层次分配
    L = levelAssignment(N)
    print('L:', L)
    # 插入虚拟节点
    N, L_b = getInBetweenNodes(G, L)    # no backedges in N
    print('N:1', N)
    print('L:1', L_b)
    # 交叉最小化
    R = twoLevelCrossMin(N, L)

    return N, R


if  __name__=='__main__':
    '''
    #edges = [(1, 3), (1, 4), (2, 6), (3, 2), (3, 7), (3, 8), (4, 5), (4, 6), (4, 8), (4, 9), (6, 10), (7, 10), (7, 11), (8, 7), (9, 11), (10, 12), (11, 12)]
    edges = [ ('A', 'B'), ('A', 'E'), ('B', 'C'), ('C', 'D'), ('D', 'C'), ('A', 'C')]
    #edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (6, 7), (5, 7) ]
    # G = graphFromEdges(edges)

    # S = cycleAnalysis(G)
    # G_inv = invertBackEdges(G, S)   # inverted edges are only for level assignment
    # L = levelAssignment(G_inv)
    # G_inv, L_b = getInBetweenNodes(G_inv, L)

    P = twoLevelCrossMin(G_inv, L)

    print ('original graph')
    printGraph(G)
    print ('graph with helper edges')
    printGraph(G)
    print (L)
    '''
    #E = [ ('A', 'B'), ('A', 'E'), ('B', 'C'), ('E', 'B'), ('C' 'E'), ('C', 'D'), ('D', 'C'), ('A', 'C')]
    #E = [ ('1', '2'), ('1', '4'), ('1','6'), ('1', '3'), ('3', '4'), ('4', '5'), ('5', '2'), ('5', '6')]
    E = [(1, 3), (1, 4), (2, 6), (3, 2), (3, 7), (3, 8), (4, 5), (4, 6), (4, 8), (4, 9), (6, 10), (7, 10), (7, 11), (8, 7), (9, 11), (10, 12), (11, 12)]
    G = graphFromEdges(E)
    print('Original Graph:')
    printGraph(G)
    G0 = G
    G, L = sugiyama(G)

    convertGridToCart(G, L)

    graphLevelNet(G, 'b1', showfig=True)

    #graphLevelNet(N, 'b2', showfig=True)

    # print(L)
    # print('New Graph:')
    #printGraph(N)





