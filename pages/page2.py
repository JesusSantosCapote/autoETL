import streamlit as st
import os
from utils.load_graphs import load_graph, load_graph_list
import networkx
from matplotlib import pyplot as plt

st.markdown("# Join Graphs")
st.sidebar.markdown("# Join Graphs")

join_graphs_path = os.path.join(os.getcwd(), 'data', 'join_graphs')
join_trees_path = os.path.join(os.getcwd(), 'data', 'join_trees')

selected_db = st.session_state.conn_info['dbname']

join_graph = load_graph(selected_db)

networkx.draw(join_graph)
plt.draw()
