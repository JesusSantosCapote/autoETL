import networkx as nx
from networkx.readwrite.graphml import generate_graphml, parse_graphml
import os
import pickle

_path = os.path.join(os.getcwd(), 'data')

def save_graph(graph, db_name):
    path = os.path.join(_path, 'join_graphs', f'{db_name}_join_graph.data')
    with open(path, 'wb') as file:
        pickle.dump(graph, file)



def save_graph_list(graph_list, db_name):
    pickle_string = ''
    path = os.path.join(_path, 'join_trees', f'{db_name}_join_trees.data')
    with open(path, 'wb') as file:
        pickle.dump(graph_list, file)
        