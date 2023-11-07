import streamlit as st
import requests
import pandas as pd

# Streamlit page configurations
st.title("Question Answering System")
st.subheader("Interact with your question-answering system")
        
# Customized Button and User Input
user_question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if user_question:
        # Make API request to get answer based on user question
        response = requests.post("http://localhost:5000/search", json={"question": user_question})
        data = response.json()

        # Check if 'passages' key is in the response
        if 'passages' in data:
            passages = data['passages']
            for passage in passages:
                st.write(f"**Passage:** {passage['_source']['Passage']}")
                st.write(f"**Relevance Score:** {passage['_score']}")
                st.write('---')
        else:
            st.write('No relevant passages found for the given question.')
            
# File Upload
st.subheader("Upload Documents for Indexing")
uploaded_file = st.file_uploader("Upload a CSV file for indexing", type=["csv"])
if uploaded_file:
    # Upload file to the server
    files = {'file': uploaded_file}
    upload_response = requests.post("http://localhost:5000/upload", files=files)
    
    # Display upload status
    if upload_response.status_code == 200:
        st.success("Documents successfully uploaded and indexed!")
    else:
        st.error("Error occurred while uploading the file. Please try again.")

# Elasticsearch Status
st.subheader("Elasticsearch Status")
es_status = requests.get("http://localhost:9200")
if es_status.status_code == 200:
    st.success("Elasticsearch is running!")
else:
    st.error("Elasticsearch is not running. Please check the Elasticsearch server.")

# Custom Font and Color
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f0f0;
        padding: 20px;
    }
    .stButton>button {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
