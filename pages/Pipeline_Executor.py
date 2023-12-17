import streamlit as st
import os

st.markdown("# Pipelines")

st.sidebar.markdown("# Upload pipeline file")

pipeline = st.sidebar.file_uploader("")

if pipeline:
    bytes_data = pipeline.getvalue()
    name = pipeline.name

    # To convert to a string based IO:
    script = str(bytes_data, 'utf-8')

    with open(os.path.join(os.getcwd(), 'data', 'pipelines', name), 'w') as file:
        file.write(script)

