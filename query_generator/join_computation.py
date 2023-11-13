#from query_generator.maximal_join_trees import maximal_join_trees_generator
from networkx import DiGraph
from copy import deepcopy
from collections import deque

def get_join(tree:DiGraph, lca, list_attr_tables):
    parents = {}
    visited = {node:False for node in tree.nodes}
    visited[lca] = True
    queue = deque()
    queue.append(lca)
    parents[lca] = None

    while queue:
        current = queue.popleft()
        for node in tree.neighbors(current):
            if not visited[node]:
                visited[node] = True
                queue.append(node)
                parents[node] = current

    answer_edges = []
    for table, _ in list_attr_tables:
        pass

    tree.edge_subgraph()
                



def lower_common_acestor(graph:DiGraph, nodes_set):
    visited = set()
    ancestors_dict = {}

    def dfs_visit(graph:DiGraph, node):
        visited.add(node)
        for acestor in graph.predecessors(node):
            if acestor not in visited:
                dfs_visit(graph, acestor)
    
    for node, _ in nodes_set:
        visited.clear()
        dfs_visit(graph, node)
        ancestors_dict[node] = deepcopy(visited)

    common_acestors = ancestors_dict.items()[0][1]
    for node, acestors in ancestors_dict.items():
        common_acestors = acestors.intersection(common_acestors)

    common_acestors = list(common_acestors)
    lower_common_acestor = common_acestors[0]

    for acestor in common_acestors:
        if graph.nodes[acestor]['height'] > graph.nodes[lower_common_acestor]['height']:
            lower_common_acestor = acestor

    return lower_common_acestor


def compute_join(join_trees: list[DiGraph], list_attr) -> str:
    valid_join_trees = []
    visited_attrs = 0
    for tree in join_trees:
        for table, attr in list_attr: #TODO: Check in other place if all the attr are in the table declared
            if table in tree.nodes.keys():
                visited_attrs += 1
        
        if visited_attrs == len(list_attr):
            valid_join_trees.append(tree)
        
        visited_attrs = 0

    for tree in valid_join_trees:
        lca = lower_common_acestor(tree, list_attr)

        
tpc_h = DiGraph()
tpc_h.add_node('part', attrs=['partkey', 'name', 'brand'])
tpc_h.add_node('supplier', attrs=['supkey', 'name', 'nationkey'])
tpc_h.add_node('partsupp', attrs=['partkey', 'supkey', 'qty'])
tpc_h.add_node('customer', attrs=['custkey', 'name', 'address', 'nationkey'])
tpc_h.add_node('orders', attrs=['orderkey', 'custkey', 'status', 'totalprice'])
tpc_h.add_node('lineitem', attrs=['orderkey', 'partkey', 'supkey', 'linenumber', 'status', 'qty'])
tpc_h.add_node('nation', attrs=['nationkey', 'name', 'regionkey', 'comment'])
tpc_h.add_node('region', attrs=['regionkey', 'name', 'comment'])

edges = [
    ('lineitem', 'part', {'condition': [('partkey', 'partkey')], 'weight':1}),
    ('lineitem', 'partsupp', {'condition': [('partkey', 'partkey'), ('supkey', 'supkey')], 'weight':1}),
    ('lineitem', 'supplier', {'condition': [('supkey', 'supkey')], 'weight':1}),
    ('lineitem', 'order', {'condition':[('orderkey', 'orderkey')], 'weight':1}),
    ('partsupp', 'part', {'condition': [('partkey', 'partkey')], 'weight':1}),
    ('partsupp', 'supplier', {'condition': [('supkey', 'supkey')], 'weight':1}),
    ('supplier', 'nation', {'condition': [('nationkey', 'nationkey')], 'weight':1}),
    ('nation', 'region', {'condition': [('regionkey', 'regionkey')], 'weight':1}),
    ('orders', 'customer', {'condition': [('custkey', 'custkey')], 'weight':1}),
    ('customer', 'nation', {'condition': [('nationkey', 'nationkey')], 'weight':1})
]

tpc_h.add_edges_from(edges)

print(tpc_h.nodes.data())
print(tpc_h.edges.data())