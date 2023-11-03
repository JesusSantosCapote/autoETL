import networkx as nx
from networkx.readwrite.graphml import generate_graphml, parse_graphml
import os

path = os.path.join(os.getcwd(), 'jointrees.data')

def save_graph_list(graph_list):
    graphml_string = ''
    with open(path, 'w') as file:
        for graph in graph_list:
            for line in generate_graphml(graph, prettyprint=True, named_key_ids=True):
                graphml_string = graphml_string + line + '\n'
            graphml_string = graphml_string + '$$$\n' #special separator of graphsML graph specifications

        file.write(graphml_string)


def load_graph_list():
    graph_list = []
    with open(path) as file:
        graphml_string = file.read()
        graphml_graphs = graphml_string.split('$$$\n')
        for graph in graphml_graphs:
            if graph != '': #Split left an empty string at the end of the file
                parsed_graph = parse_graphml(graph)
                graph_list.append(parsed_graph)

    return graph_list
