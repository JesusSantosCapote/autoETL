import streamlit as st
import os

st.markdown("# Experiments (Beta Only)")

experiments_path = os.path.join(os.getcwd(), 'experiments')
available_exp = os.listdir(experiments_path)

exp = st.selectbox('Pick Experiment', available_exp)

pipeline_file = os.path.join(experiments_path, exp, 'pipeline.py')

execute = st.button('Execute Pipeline', type='primary')

with open(pipeline_file, 'r') as file:
    code = file.read()

st.markdown('### Pipeline Code')

st.code(code, language='python')

if execute:
    try:
        os.system(f'python {pipeline_file}')
    except Exception as e:
        st.error(e, icon="🚨")
