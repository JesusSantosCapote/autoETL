#from query_generator.maximal_join_trees import maximal_join_trees_generator
from networkx import DiGraph
from copy import deepcopy
from collections import deque
#from logger import logger
from itertools import combinations
#TODO fix imports
def get_parents(tree:DiGraph, root):
    parents = {}
    visited = {node:False for node in tree.nodes}
    visited[root] = True
    queue = deque()
    queue.append(root)
    parents[root] = None

    while queue:
        current = queue.popleft()
        for node in tree.neighbors(current):
            if not visited[node]:
                visited[node] = True
                queue.append(node)
                parents[node] = current

    return parents


def get_answer_edges(list_attr_tables, parents):
    answer_edges = []
    for table, _ in list_attr_tables:
        current_parent = table
        try:
            next_parent = parents[table]
        except KeyError:
            #logger.error(f'Table: {table} not defined in database')
            pass

        while next_parent:
            temp = current_parent
            current_parent = parents[temp]
            edge = (current_parent, temp)
            if edge not in answer_edges:
                answer_edges.append(edge)
            next_parent = parents[current_parent]

    return answer_edges

def get_joins(tree:DiGraph, lca, list_attr_tables):
    parents = get_parents(tree, lca)
    answer_edges = get_answer_edges(list_attr_tables, parents)
    answer_sub_tree = tree.edge_subgraph(answer_edges)

    joins = []
    def join_visit(actual_join, table):
        global joins
        if len(actual_join) == 2 * len(answer_sub_tree.nodes()) - 1:
            joins.append(actual_join)
        
        else:
            for child in answer_sub_tree.neighbors(table):
                conditions = answer_sub_tree[table][child]['conditions']
                for i in range(1, len(conditions)+1):
                    for join_cond in combinations(conditions, i):
                        actual_join = actual_join + [join_cond[0]]
                        join_visit(actual_join, child)
    
    join_visit([], lca)

    return joins


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

    common_acestors = list(ancestors_dict.items())[0][1]
    for node, acestors in ancestors_dict.items():
        common_acestors = acestors.intersection(common_acestors)

    common_acestors = list(common_acestors)
    lower_common_acestor = common_acestors[0]

    for acestor in common_acestors:
        if graph.nodes[acestor]['height'] > graph.nodes[lower_common_acestor]['height']:
            lower_common_acestor = acestor

    return lower_common_acestor


def get_answer_trees(join_trees, list_attr):
    valid_join_trees = []
    visited_attrs = 0
    for tree in join_trees:
        for table, attr in list_attr: 
            if table in tree.nodes.keys():
                visited_attrs += 1
        
        if visited_attrs == len(list_attr):
            valid_join_trees.append(tree)
        
        visited_attrs = 0
    return valid_join_trees


def compute_joins(join_trees: list[DiGraph], list_attr) -> str:
    valid_join_trees = get_answer_trees(join_trees, list_attr)
    all_joins = []
    for tree in valid_join_trees:
        lca = lower_common_acestor(tree, list_attr)
        joins = get_joins(tree, lca, list_attr)
        all_joins.extend(joins)

    print(all_joins)


