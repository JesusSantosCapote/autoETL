import streamlit as st
from  orchestrator import Orchestrator
import os
import zipfile

st.markdown('# Query Generator')

c1, c2 = st.columns([3, 0.75])

st.sidebar.markdown("## Load Script")
uploaded_file = st.sidebar.file_uploader("")

def join_to_str(join):
    join_str = ''
    for i in range(0, len(join), 2):
            if i == 0:
                join_str = join_str + join[i]
            else:
                conditions = ''
                for cond, index in zip(join[i-1], range(len(join[i-1]))):
                    conditions = conditions + f'{cond[0]} = {cond[1]}'
                    if index != len(join[i-1]) - 1:
                        conditions = conditions + ' AND '
                join_str = join_str + f' JOIN {join[i]} ON ' + conditions
    
    return join_str

script = ''
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    name = uploaded_file.name

    # To convert to a string based IO:
    script = str(bytes_data, 'utf-8')

    with open(os.path.join(os.getcwd(), 'data', 'scripts', name), 'w') as file:
        file.write(script)

saved_scripts = os.listdir(os.path.join(os.getcwd(), 'data', 'scripts'))

script_to_run = st.selectbox("Pick a script", saved_scripts)

if script_to_run:
    with open(os.path.join(os.getcwd(), 'data', 'scripts', script_to_run), 'r') as file:
        code = file.read()

    if 'conn_info' not in st.session_state.keys():
        st.error("No connection to any database has been established yet", icon="🚨")

    else:
        orch = Orchestrator(st.session_state.conn_info['dbname'])
        orch.parse_code(code)
        if not orch.code_is_good:
            error = ''
            with open(os.path.join(os.getcwd(), 'dsl_log.log')) as file:
                error = file.read()    
            st.error(error, icon="🚨")

        else:
            all_joins = orch.compute_joins()
            select_boxes = []
            for dimension, joins in all_joins:
                joins_str = ''

                for join, index in zip(joins, range(1, len(joins) + 1)):
                    joins_str = joins_str + f'{index}: {join_to_str(join)}\n'

                st.markdown(f"#### Joins for {dimension.name}")
                st.text(joins_str)
                selected_join = st.selectbox(f"Pick a Join for {dimension.name}", range(1, len(joins) + 1))
                select_boxes.append(selected_join - 1)

            dw = st.text_input("Target Data warehouse name")
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                code_gen = st.button("Generate Querys", type='primary')
            
            with c2:
                load_querys = st.button("Load Querys")

            if code_gen:
                if not dw:
                    st.error("Empty Data Warehouse name not allowed", icon="🚨")

                # with c3:
                #     st.download_button()
                
                else:
                    selected_joins = []
                    for dim_joins_tuple, selected in zip(all_joins, select_boxes):
                        selected_joins.append(dim_joins_tuple[1][selected])

                    orch.generate_querys(selected_joins, dw)

                    query_path = os.path.join(os.getcwd(), 'data', 'querys', f"{st.session_state.conn_info['dbname']}_{dw}_querys")
                    querys_files = os.listdir(query_path)

                    for query_file_name in querys_files:
                        with open(os.path.join(query_path, query_file_name), 'r') as file:
                            st.subheader(query_file_name)
                            st.code(file.read(), 'sql', True)


