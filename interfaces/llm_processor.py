import os

from langchain.chains import LLMChain 
from llms.alita import AlitaLLM  # pylint: disable=E0401
from langchain.llms import __getattr__ as get_llm, __all__ as llms  # pylint: disable=E0401
from langchain.chat_models import __all__ as chat_models  # pylint: disable=E0401

from langchain.embeddings import __all__ as embeddings  # pylint: disable=E0401

from langchain.vectorstores import __all__ as vectorstores  # pylint: disable=E0401
from langchain.vectorstores import __getattr__ as get_vectorstore_cls  # pylint: disable=E0401

from tools import log  # pylint: disable=E0401

from langchain.prompts import PromptTemplate  # pylint: disable=E0401


def get_model(model_type: str, model_params: dict):
    """ Get LLM or ChatLLM """
    if model_type is None:
        return None
    if model_type in llms:
        return get_llm(model_type)(**model_params)
    elif model_type == "Alita":
        return AlitaLLM(**model_params)
    elif model_type in chat_models:
        model = getattr(__import__("langchain.chat_models", fromlist=[model_type]), model_type)
        return model(**model_params)
    raise RuntimeError(f"Unknown model type: {model_type}")


def get_embeddings(embeddings_model: str, embeddings_params: dict):
    """ Get *Embeddings """
    if embeddings_model is None:
        return None
    if embeddings_model in embeddings:
        model = getattr(__import__("langchain.embeddings", fromlist=[embeddings_model]), embeddings_model)
        return model(**embeddings_params)
    raise RuntimeError(f"Unknown Embedding type: {embeddings_model}")


def summarize(llmodel, document, summorization_prompt, metadata_key='document_summary'):
    if llmodel is None:
        return document
    content_length = len(document.page_content)
    # TODO: Magic number need to be removed
    if content_length < 1000:
        return document
    file_summary = summorization_prompt
    file_summary_prompt = PromptTemplate.from_template(file_summary, template_format='jinja2')
    llm = LLMChain(
        llm=llmodel,
        prompt=file_summary_prompt,
        verbose=True,
    )
    log.info(f"Generating summary for: {document.metadata['source']}\n Content length: {content_length}")
    try:
        result = llm.predict(content=document.page_content)
    except:  # pylint: disable=W0702
        log.exception("Failed to generate summary")
        raise
    document.metadata[metadata_key] = result
    return document


def get_vectorstore(vectorstore_type, vectorstore_params, embedding_func=None):
    """ Get vector store obj """
    if vectorstore_type is None:
        return None
    if vectorstore_type in vectorstores:
        if embedding_func:
            vectorstore_params['embedding_function'] = embedding_func
        return get_vectorstore_cls(vectorstore_type)(**vectorstore_params)
    raise RuntimeError(f"Unknown VectorStore type: {vectorstore_type}")

def add_documents(vectorstore, documents):
    """ Add documents to vectorstore """
    if vectorstore is None:
        return None
    texts = []
    metadata = []
    for document in documents:
        texts.append(document.page_content)
        metadata.append(document.metadata)
    vectorstore.add_texts(texts, metadatas=metadata)

