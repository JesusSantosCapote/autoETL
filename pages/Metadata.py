import streamlit as st
import os
from utils.load_graphs import load_graph, load_graph_list
import networkx as nx
from matplotlib import pyplot as plt


st.markdown("# Join Graphs")
st.sidebar.markdown("# Metadata")

join_graphs_path = os.path.join(os.getcwd(), 'data', 'join_graphs')
join_trees_path = os.path.join(os.getcwd(), 'data', 'join_trees')

if 'conn_info' not in st.session_state.keys():
    st.error("No connection to any database has been established yet", icon="🚨")

else:
    selected_db = st.session_state.conn_info['dbname']

    join_graph = load_graph(selected_db)

    fig = plt.figure()
    pos = nx.planar_layout(join_graph)
    nx.draw(join_graph ,pos, with_labels=True, node_color=range(len(join_graph.nodes)), node_size=800, cmap=plt.cm.Oranges)

    st.pyplot(fig)

    st.markdown("# Database Metadata")

    metadata_path = os.path.join(os.getcwd(), 'data', 'schemas', f'{selected_db}')
    with open(os.path.join(metadata_path, f'{selected_db}_metadata.txt'), 'r') as file:
        st.code(file.read())

    t = st.toggle("Show Join Trees")

    if t:
        st.markdown("# Join Trees")

        join_trees = load_graph_list(selected_db)


        for tree in join_trees:
            fig2 = plt.figure()

            pos = nx.planar_layout(tree)
            nx.draw(join_graph ,pos, with_labels=True, node_color=range(len(join_graph.nodes)), node_size=800, cmap=plt.cm.Oranges)

            st.pyplot(fig2)