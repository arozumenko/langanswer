import json
import streamlit as st
from interfaces.llm_processor import get_embeddings, get_model, get_vectorstore
from langchain.schema import HumanMessage, SystemMessage
from app import main
from config import (ai_model, ai_model_params, embedding_model, embedding_model_params, vectorstore, 
                    vectorstore_params, weights, kw_plan, kw_args, splitter_name, splitter_params, 
                    guidance_message, collections, document_processing_prompt, chunk_processing_prompt)

def rerank_documents(documents, weights):
    """ Rerank documents """
    _documents = []
    for (document, score) in documents:
        _documents.append({
            "page_content": document.page_content,
            "metadata": document.metadata,
            "score": score*weights[document.metadata['type']]
        })
    return sorted(_documents, key=lambda x: x["score"], reverse=True)

def merge_results(vs, documents, top_k):
    results = {}
    for doc in documents:
        if doc['metadata']['source'] not in results.keys():
            results[doc['metadata']['source']] = {'page_content': '', 'metadata': { 'source' : doc['metadata']['source'] }}
            docs = vs.similarity_search('', filter={'source': doc["metadata"]['source']})
            for d in docs:
                if d.metadata['type'] == 'data':
                    results[doc['metadata']['source']]['page_content'] += d.page_content + '\n\n'
                elif d.metadata['type'] == 'document_summary':
                    results[doc['metadata']['source']]['page_content'] = d.page_content + '\n\n' + results[doc['metadata']['source']]['page_content']
        
        if len(results.keys()) >= top_k:
            break

    return list(results.values())

def generateResponse(input, top_k=5):
    embedding = get_embeddings(embedding_model, embedding_model_params)
    vectorstore_params['collection_name'] = st.session_state["collection"]
    vs = get_vectorstore(vectorstore, vectorstore_params, embedding_func=embedding)
    ai = get_model(ai_model, ai_model_params)
    docs = vs.similarity_search_with_score(input, filter={'library': 'demothing'})
    docs = rerank_documents(docs, weights)
    references = []
    context = guidance_message
    messages = []
    docs = merge_results(vs, docs, top_k)
    for doc in docs[:top_k]:
        context += f'{doc["page_content"]}\n\n'
        references.append(doc["metadata"]["source"])
    messages.append(SystemMessage(content=context))
    messages.append(HumanMessage(content=input))
    response_text = ai(messages).content

    return {
        "response": response_text,
        "references": references
    }

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
            print(st.session_state["collection"])
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

    response = generateResponse(prompt, top_k=10)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message = response['response'] + '\n\n' + 'References: ' + '\n\n' 
        
        for ref in response['references']:
            message += f':gray[{ref}]\n\n'
        st.markdown(message)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})