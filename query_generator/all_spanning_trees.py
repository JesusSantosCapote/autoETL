import networkx
from networkx import DiGraph
from networkx import ArborescenceIterator

def networkX_all_spanning_trees(graph:DiGraph) -> list[DiGraph]:
    result = []
    for tree in ArborescenceIterator(graph):
        result.append(tree)

    return result
