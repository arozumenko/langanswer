# Copyright (c) 2023 Artem Rozumenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import streamlit as st
from interfaces.llm_processor import generateResponse
from indexer import main
from config import (ai_model, ai_model_params, embedding_model, embedding_model_params, vectorstore, 
                    vectorstore_params, weights, kw_plan, kw_args, splitter_name, splitter_params, 
                    guidance_message, collections, document_processing_prompt, chunk_processing_prompt)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Initialize chat history
if "collection" not in st.session_state:
    st.session_state["collection"] = ''


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.title("Data bot")
    # add button to clear chat history
    tab1, tab2 = st.tabs(["Select Dataset", "Create / Update Dataset"])
    with tab1:
        option = st.selectbox(
            "Select collection to use:",
            collections,
            index=None,
            placeholder="Select collection of data ... ",
            )
        if option != st.session_state["collection"]:
            st.session_state["messages"] = []
            st.session_state["collection"] = option
            # print(st.session_state["collection"])
        if st.button("Clear chat"):
            st.session_state["messages"] = []

    with tab2:
        dataLoader = st.selectbox(
            "Select data loader",
            ('DirectoryLoader', 'ConfluenceLoader'),
            index=None
            )
        loaderParams = st.text_area("Loader params", value='{"path": "./data", "use_multithreading": false, "loader_cls": "TextLoader", "table_raw_content": true, "docs_page_split": false}')
        loadParams = st.text_area("Load params", value='{}')
        collectionName = st.text_input("Collection name", value='test_collection')
        if st.button("Load data"):
            with st.spinner('Wait for it...'):
                vectorstore_params["collection_name"] = collectionName
                main(dataset='data', library='demothing',
                    loader_name=dataLoader,
                    loader_params=json.loads(loaderParams),
                    load_params=json.loads(loadParams),
                    ## defaults from config.py
                    document_processing_prompt=document_processing_prompt,
                    chunk_processing_prompt=chunk_processing_prompt,
                    vectorstore=vectorstore,
                    vectorstore_params=vectorstore_params,
                    embedding_model=embedding_model,
                    embedding_model_params=embedding_model_params,
                    ai_model=ai_model,
                    ai_model_params=ai_model_params,
                    kw_plan=kw_plan,
                    kw_args=kw_args,
                    splitter_name=splitter_name,
                    splitter_params=splitter_params,
                    )
            st.success('Done!')
            
            
# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = generateResponse(prompt, collection=st.session_state["collection"], top_k=10)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message = response['response'] + '\n\n' + 'References: ' + '\n\n' 
        
        for ref in response['references']:
            message += f':gray[{ref}]\n\n'
        st.markdown(message)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})