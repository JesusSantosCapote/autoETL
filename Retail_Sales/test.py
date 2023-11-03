import networkx
from networkx import ArborescenceIterator
from networkx import DiGraph

G = DiGraph()

e = [(1,2), (1,3), (1,4), (1,5), (3,2), (3,4), (4,6), (5,7), (7,6), (6,8)]

for edge in e:
    G.add_edge(*edge, weight=1)

print(G.edges)

l = []
for graph in ArborescenceIterator(G):
    print(graph)

