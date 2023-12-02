import networkx as nx
from networkx.readwrite.graphml import parse_graphml
import os
import logger
import pickle

_path = os.path.join(os.getcwd(), 'data')

def load_graph(db_name):
    saved_graphs = os.listdir(os.path.join(_path, 'join_graphs'))
    graph_name = ''
    for graph in saved_graphs:
        if graph.startswith(db_name):
            graph_name = graph

    if not graph_name:
        logger.error(f'Join graph not found for {db_name} database')
    else:
        path = os.path.join(_path, 'join_graphs', graph_name)
        with open(path, 'rb') as file:
            loaded_graph = pickle.load(file)

        return loaded_graph


def load_graph_list(db_name):
    saved_graphs = os.listdir(os.path.join(_path, 'join_trees'))
    graph_list_name = ''
    for graph in saved_graphs:
        if graph.startswith(db_name):
            graph_list_name = graph

    if not graph_list_name:
        logger.error(f'Join trees not found for {db_name} database')
    else:
        path = os.path.join(_path, 'join_trees', graph_list_name)
        with open(path, 'rb') as file:
            graph_list = pickle.load(file)

        return graph_list