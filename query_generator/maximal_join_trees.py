from all_spanning_trees import networkX_all_spanning_trees
from networkx import DiGraph, set_node_attributes
from networkx.algorithms.components import strongly_connected_components
from collections import deque


def set_height(graph:DiGraph, root):
    visited = {node:False for node in graph.nodes}
    visited[root] = True
    queue = deque()
    queue.append(root)
    graph.nodes[root]['heigth'] = 0

    while queue:
        current = queue.popleft()
        for node in graph.neighbors(current):
            if not visited[node]:
                visited[node] = True
                queue.append(node)
                graph.nodes[node]['heigth'] = graph.nodes[current]['heigth'] + 1


def find_reachable(graph:DiGraph, source):
    visited = {node:False for node in graph.nodes}
    reached_nodes = []
    reached_nodes.append(source)
    visited[source] = True
    queue = deque()
    queue.append(source)

    while queue:
        current = queue.popleft()
        for node in graph.neighbors(current):
            if not visited[node]:
                visited[node] = True
                queue.append(node)
                reached_nodes.append(node)
    
    return graph.subgraph(reached_nodes)


def in_edge_from_outside(graph:DiGraph, node, scc):
    for n in graph.nodes:
        if n not in scc:
            if graph.has_edge(n, node):
                return True
            
    return False


def maximal_join_trees_generator(join_graph:DiGraph):
    result = []
    scc_iterator = strongly_connected_components(join_graph)
    reachable_graphs = []

    for scc in scc_iterator:
        scc = list(scc)
        if len(scc) == 1 and join_graph.in_degree(scc[0]) == 0:
            reachable = find_reachable(join_graph, scc[0])
            reachable_graphs.append((reachable, scc[0]))

        else:
            for node in scc:
                if not in_edge_from_outside(join_graph, node, scc):
                    reachable = find_reachable(join_graph, node)
                    reachable_graphs.append((reachable, node))

    for graph, root in reachable_graphs:
        max_join_trees = networkX_all_spanning_trees(graph)

        for join_tree in max_join_trees:
            if join_tree.in_degree(root) == 0:
                join_tree.graph['root'] = root
                set_height(join_tree, root)
                result.append(join_tree)

    return result



g = DiGraph()
edges = [(1,2), (2,4), (4,3), (3,2), (5,4), (5,6), (5,7), (9,7), (7,8)]

g.add_edges_from(edges, weight=1)


# print(in_edge_from_outside(g, 2, [2, 3, 4]))
# print(find_reachable(g, 2))

for i in maximal_join_trees_generator(g):
    print(i.nodes.data())
    print(i.pred)
    print(i.graph['root'])

