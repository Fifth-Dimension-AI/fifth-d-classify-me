'''
requirements.txt file contents:

langchain==0.0.154
PyPDF2==3.0.1
python-dotenv==1.0.0
streamlit==1.18.1
faiss-cpu==1.7.4
streamlit-extras
'''

import io
from io import BytesIO
import base64

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

import os
import pickle
from dotenv import dotenv_values, load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader

def show_pdf(uploaded_file):
    # with open(file_path,"rb") as f:
    with io.BytesIO() as buffer:
        buffer.write(uploaded_file.read())
        buffer.seek(0)
        base64_pdf = base64.b64encode(buffer.read()).decode('utf-8')

        # pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# Sidebar filters
def get_page():
    page = st.sidebar.text_input(label='PDF Page') 
    if str(page).strip() not in ['all','']:
        try:
            page = int(page)
            page = page - 1
        except:
            st.write('Enter a page number (starting from 1), or "all"')
    return str(page)

def save_uploaded_file(uploaded_file, folder_path):
    file_path = os.path.join(folder_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File saved successfully!")
    return file_path

@st.cache_data(show_spinner=False)
def load_pdf(read_method,file_path,extract_images):
    if 'azure' in read_method.lower():
        endpoint = dotenv_values().get('AZURE_DOC_INTELLIGENCE_ENDPOINT')
        key = dotenv_values().get('AZURE_DOC_INTELLIGENCE_API_KEY')
        loader = AzureAIDocumentIntelligenceLoader(
            api_endpoint=endpoint, api_key=key, file_path=file_path, api_model="prebuilt-layout"
        )

        documents = loader.load()
    else:

        loader = PyPDFLoader(file_path,extract_images=extract_images)
        pages = loader.load_and_split()

        os.environ['OPENAI_API_KEY'] = dotenv_values().get('OPENAI_API_KEY')

        faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
    
    return loader


# Sidebar contents
with st.sidebar:
    st.title('🤗💬 LLM Chat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model (GPT-3.5-Turbo)

    ''')

    # st.write('Made with ❤️ by [Prompt Engineer](https://youtube.com/@engineerprompt)')

load_dotenv()

def main():
    st.title("Chat with PDF 💬")

    read_method = st.sidebar.selectbox('Load Method',['OpenAI','Azure Doc Intelligence'],index =None,placeholder="Choose an option")
    extract_images = st.sidebar.checkbox('Extract Images?')

    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    # st.write(pdf)
    if pdf is not None:

        file_path = save_uploaded_file(pdf,'temp/')
        show_pdf(pdf)

        if read_method:
            if st.checkbox('Read PDF'):
                with st.spinner('Reading PDF...'):
                    loader = load_pdf(read_method,file_path,extract_images)

                query = st.text_input("Ask questions about your PDF file:")
                # st.write(query)
                
                if query:
                    if st.button('Ask!'):
                        with st.spinner('Thinking...'):
                        # docs = VectorStore.similarity_search(query=query, k=5)
                        # docs = faiss_index.similarity_search(query, k=5)
                            llm = OpenAI()
                            chain = load_qa_chain(llm,verbose=True)
                            response = chain.run(input_documents=loader.load(), question=query)
                        st.write(response)

if __name__ == '__main__':
    main()