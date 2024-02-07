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
import streamlit_authenticator as stauth

from analysta_index.interfaces.llm_processor import generateResponse
from analysta_index.indexer import main
from config import (ai_model, ai_model_params, embedding_model, embedding_model_params, vectorstore,
                    vectorstore_params, weights, kw_plan, kw_args, splitter_name, splitter_params,
                    guidance_message, context_message, collections,
                    document_processing_prompt, chunk_processing_prompt)
from json import dumps

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Initialize chat history
if "collection" not in st.session_state:
    st.session_state["collection"] = ''

if 'data_loader_params' not in st.session_state:
    st.session_state['data_loader_params'] = dumps({
        "path": "./data",
        "use_multithreading": False,
        "loader_cls": "TextLoader",
        "table_raw_content": True,
        "docs_page_split": True
        }, indent=2)

if 'loader_params' not in st.session_state:
    st.session_state['loader_params'] = '{}'

def change_default_values():
    pass

authenticator.login()

if st.session_state["authentication_status"]:

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.sidebar:
        st.title("Data bot")
        st.write(f'Welcome *{st.session_state["name"]}*')
        # add button to clear chat history
        authenticator.logout()
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
            contextTest = st.text_area("Conversation context", value=context_message, height=250)
            guidanceTest = st.text_area("Pre-retrieval message", value=guidance_message, height=150)
            if st.button("Clear chat"):
                st.session_state["messages"] = []
        with tab2:
            dataLoader = st.selectbox(
                "Select data loader",
                ('DirectoryLoader', 'ConfluenceLoader', 'GitLoader', 'ExcelLoader', 'CSVLoader'),
                index=None,
                on_change=change_default_values
                )

            loaderParams = st.text_area("Loader params", value=st.session_state['data_loader_params'], height=300)
            loadParams = st.text_area("Load params", value=st.session_state['loader_params'])
            collectionName = st.selectbox(
                "Collection:",
                collections,
                index=None,
                placeholder="Select where to add docs ... ",
            )
            if st.button("Load data"):
                with st.spinner('Wait for it...'):
                    vectorstore_params["collection_name"] = collectionName
                    main(dataset='data', library=collectionName,
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
    if st.session_state["authentication_status"]:
        if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = generateResponse(
                prompt, guidance_message, context_message, collection=st.session_state["collection"], top_k=10,
                ai_model=ai_model, ai_model_params=ai_model_params,
                embedding_model=embedding_model, embedding_model_params=embedding_model_params,
                vectorstore=vectorstore, vectorstore_params=vectorstore_params,
                weights=weights,
            )
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message = response['response'] + '\n\n' + 'References: ' + '\n\n'

                for ref in response['references']:
                    message += f':gray[{ref}]\n\n'
                st.markdown(message)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
