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

from os import environ
from dotenv import load_dotenv

load_dotenv('./.env')

embedding_model='AzureOpenAIEmbeddings'
embedding_model_params={
    "deployment": environ.get("EMBEDDINGS_DEPLOYMENT", ""),
    "model": environ.get("EMBEDDINGS_MODEL", ""),
    "openai_api_version": environ.get("OPENAI_API_VERSION", "2023-03-15-preview"),
    "azure_endpoint": environ.get("AZURE_ENDPOINT", ""),
    "openai_api_type": "azure",
    "openai_api_key": environ.get("OPENAI_API_KEY", ""),
}

ai_model='AzureChatOpenAI'
ai_model_params={
    "model_name": environ.get("MODEL_NAME", ""),
    "deployment_name": environ.get("DEPLOYMENT_NAME", ""),
    "openai_api_version": environ.get("OPENAI_API_VERSION", "2023-03-15-preview"),
    "azure_endpoint": environ.get("AZURE_ENDPOINT", ""),
    "openai_api_key": environ.get("OPENAI_API_KEY", ""),
    "max_tokens": int(environ.get("MAX_TOKEN", "512")), 
    "temperature": 0.8, 
    "top_p": 0.4, 
    "max_retries": 2
}

vectorstore='Chroma'
vectorstore_params={
    'collection_name': 'test_collection',
    'persist_directory': './chroma'
}

weights = {
    'keywords': 0.2,
    'document_summary': 0.5,
    'data': 0.3
}

kw_plan='Bert'
kw_args={'kw_strategy': 'max_sum'}
splitter_name='chunks'  # sentences, paragraphs, lines, chunks
splitter_params={
    'chunk_size': 1000,
    'chunk_overlap': 100,
    'autodetect_language': True,
    'kw_for_chunks': True,
}

document_processing_prompt = None
chunk_processing_prompt = None

guidance_message = """
    Use following documents as a source for answering the question:
"""

collections = ['test_collection']