import streamlit as st
import os
from utils.load_graphs import load_graph, load_graph_list
import networkx as nx
from matplotlib import pyplot as plt


st.markdown("# Join Graphs")
st.sidebar.markdown("# Join Graphs")

join_graphs_path = os.path.join(os.getcwd(), 'data', 'join_graphs')
join_trees_path = os.path.join(os.getcwd(), 'data', 'join_trees')

selected_db = st.session_state.conn_info['dbname']

join_graph = load_graph(selected_db)

fig = plt.figure(frameon=True)
pos = nx.planar_layout(join_graph)
nx.draw(join_graph ,pos, with_labels=True, node_color=range(len(join_graph.nodes)), node_size=800, cmap=plt.cm.Oranges)
st.write(fig)

