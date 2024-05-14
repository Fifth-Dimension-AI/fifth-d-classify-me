import streamlit as st
import os
import pandas as pd
import json

import sys
sys.path.append('../')

from app import evaluate_v2
from utils import utils

with st.sidebar:
    st.title('🤗💬 LLM JSON Classifier')
    st.markdown('''
    ## About
    This app is an LLM-powered JSON Classifier built using:
    - [Streamlit](https://streamlit.io/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model (GPT-3.5-Turbo-1106)

    ''')

def iterate_test_cases(file_path):
    # Add your logic here
    pass

# Get list of files in a directory
def get_files_in_directory(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

st.title('Test Case Iterator')

uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        st.success("JSON file uploaded successfully!")
        utils.write_json_to_directory(data, 'temp')
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")

# If file is selected, display button
if uploaded_file:
    # file_path = [os.path.join(directory, selected_file)]
    
    expander_sidebar = st.sidebar.expander('**Mapping of Classes**',expanded=True)
    with expander_sidebar:
        classes, options, queries = utils.load_json_file(data)[1:]
        df_classes = pd.DataFrame(classes)
        st.write(df_classes.sort_values('class_id').set_index('class_id'))

    expander_main = st.expander('**View JSON**', expanded=False)
    with expander_main:

        st.divider()
        col1,col2 = st.columns(2)
        with col1:
            st.write(f"Multilabel: {options.get('multilabel',)}")
        with col2:
            st.write(f"Show Reasoning: {options.get('reasoning', False)}")
        st.divider()
        st.write('Queries:')
        st.write(queries)


    if st.button('🤖 Classify'):
        with st.spinner('Classifying JSON...'):
            avg_acc, results = evaluate_v2.iterate_test_cases(test_case_paths=['./temp/temp.json'],return_results=True)
            
        st.write(results)
        st.write(f"Average accuracy: {avg_acc * 100:.2f}%")

        download_md = utils.convert_df_to_link(results)
        st.markdown(download_md,unsafe_allow_html=True)

        if st.button('Reset Page'):
            st.caching.clear_cache()
            # write a function that deletes ./temp/temp.json
