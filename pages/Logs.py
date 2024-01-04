import streamlit as st
import os

dsl_logs = os.path.join(os.getcwd(), 'dsl_log.log')
logs = os.path.join(os.getcwd(), 'logs.log')

st.markdown("# Logs")

st.markdown("### DSL Logs")

with open(dsl_logs) as file:
    dsl_errors = file.read()

st.code(dsl_errors)


st.markdown("### App Logs")

with open(logs) as file:
    logs = file.read()

st.code(logs)