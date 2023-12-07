
from langchain.document_loaders import (TextLoader, 
        UnstructuredMarkdownLoader,
        UnstructuredPDFLoader, UnstructuredWordDocumentLoader,
        JSONLoader, AirbyteJSONLoader, UnstructuredHTMLLoader, 
        UnstructuredPowerPointLoader, PythonLoader)

from .AlitaCSVLoader import AlitaCSVLoader
from .AlitaExcelLoader import AlitaExcelLoader

loaders_map = {
    '.txt': {
        'class': TextLoader,
        'kwargs': {
            'autodetect_encoding': True
        }
    },
    '.md': {
        'class': UnstructuredMarkdownLoader,
        'kwargs': {}
    },
    '.csv': {
        'class': AlitaCSVLoader,
        'kwargs': {
            'encoding': 'utf-8',
            'raw_content': False
        }
    },
    '.xlsx': {
        'class': AlitaExcelLoader,
        'kwargs': { 
            'raw_content': False
        }
    },
    '.xls': {
        'class': AlitaExcelLoader,
        'kwargs': {
            'raw_content': False
        }
    },
    '.pdf': {
        'class': UnstructuredPDFLoader,
        'kwargs': {}
    },
    '.docx': {
        'class': UnstructuredWordDocumentLoader,
        'kwargs': {}
    },
    '.json': {
        'class': TextLoader,
        'kwargs': {}
    },
    '.jsonl': {
        'class': AirbyteJSONLoader,
        'kwargs': {}
    },
    '.htm': {
        'class': UnstructuredHTMLLoader,
        'kwargs': {}
    },
    '.html': {
        'class': UnstructuredHTMLLoader,
        'kwargs': {}
    },
    '.ppt': {
        'class': UnstructuredPowerPointLoader,
        'kwargs': {}
    },
    '.pptx': {
        'class': UnstructuredPowerPointLoader,
        'kwargs': {}
    },
    '.py': {
        'class': PythonLoader,
        'kwargs': {}
    }
}