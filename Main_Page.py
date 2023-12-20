import streamlit as st
import json
import os
from crawler.postgresSql_crawler import PostgreSqlCrawler
from data_catalog.handler import DataCatalogHandler
from query_generator.maximal_join_trees import maximal_join_trees_generator

conn_path = os.path.join(os.getcwd(), 'data', 'connections')

crawlers_for_sgbd = {'PostgreSQL': PostgreSqlCrawler}
st.markdown("# Connections")
st.sidebar.markdown("# Connections").title('AutoETL')

st.sidebar.markdown("## Delete Stored Connection")
del_options = os.listdir(conn_path)
del_select = st.sidebar.selectbox("Select one connection to delete", del_options)
delete_btn = st.sidebar.button("Delete", type='primary')


st.markdown("### Stablish connection")
select_options = []
for conn in os.listdir(conn_path):
    s_option = conn[0:-5]
    select_options.append(s_option)

selected_conn = st.selectbox("Select DB for connect", select_options)

with open(os.path.join(conn_path, f'{selected_conn}.json'), 'r') as file:
    conn_info = json.load(file)

re_compute = st.toggle("Recompute data")

schemas_path = os.path.join(os.getcwd(), 'data', 'schemas')

crawlers_for_sgbd = {
    'PostgreSQL': PostgreSqlCrawler(conn_info['dbname'], conn_info['user'], conn_info['password'], conn_info['host'], conn_info['port'])
}

if st.button("Connect"):
    st.session_state.conn_info = conn_info
    make_computation = False
    if conn_info['dbname'] not in os.listdir(schemas_path):
        make_computation = True
        st.info("No data has yet been calculated for this database. We will do the calculation now.")

    else:
        if re_compute:
            make_computation = True

    if make_computation:
        #Crawler things
        crawler = crawlers_for_sgbd[conn_info['sgbd']]
        crawler.explore_db()
        crawler.export_metadata_to_file()

        #Data Catalog things
        with open(os.path.join(schemas_path, f"{conn_info['dbname']}", f"{conn_info['dbname']}_schema.json"), 'r') as file:
            db_schema_dict = json.load(file)

        handler = DataCatalogHandler(db_schema_dict, conn_info['dbname'], 'neo4j', 'datacatalog', 'bolt://data_catalog:7687')
        handler.create_data_catalog()
        handler.export_join_graph()

        maximal_join_trees_generator(handler.join_graph)


with st.form("my_form"):
    st.write("New Connections")
    sgbd = st.selectbox("SGBD", ["PostgreSQL"])
    db = st.text_input("Database name", key='db')
    user = st.text_input("User", key='user')
    password = st.text_input("Password", key='pass')
    host = st.text_input("Host", key='host')
    port = st.text_input("Port", key='port')

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        if not sgbd or not db or not user or not password or not host or not port:
            st.error('All fields in the form must contain a value', icon="🚨")
        else:
            conn_dict = {'sgbd': sgbd, 'dbname': db, 'user': user, 'password': password, 'host': host, 'port': port}
            conn_path_save = os.path.join(conn_path, f'{db}.json')
            with open(conn_path_save, 'w') as file:
                json.dump(conn_dict, file, indent=4)




