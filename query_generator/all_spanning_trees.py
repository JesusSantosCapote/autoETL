import networkx
from networkx import DiGraph
from copy import deepcopy

#The algorithm follows the same notation of the original paper from Gabow and Myers
def gabow_myers(graph:DiGraph, root):
    root_edges = graph.edges(root)
    F = []
    for edge in root_edges:
        F.append(edge)

    T = DiGraph()
    L = DiGraph()
    spanning_trees = []

    def grow():
        if len(T.nodes()) == len(graph.nodes()):
            L = deepcopy(T)
            spanning_trees.append(L)

        else:
            FF = []
            e = F.pop()
            v = e[1]
            T.add_edge(*e)

            for edge in graph.edges(v): #edges from v
                F.append(edge)

            for edge in deepcopy(F):
                if edge[1] == v and T.has_node(edge[0]):
                    F.remove(edge)
                
            grow()

            for edge in deepcopy(F):
                if edge[0] == v and not T.has_node(edge[1]):
                    F.remove(edge)
