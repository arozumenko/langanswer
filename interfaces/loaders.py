"""
Function of this beautiful file is to load data from different sources and transform them to texttual format
It implements interface for default Langchain loaders and custom loaders that uses langchain base loader class
"""

from langchain.document_loaders import __all__ as loaders

from document_loaders.AlitaCSVLoader import AlitaCSVLoader
from document_loaders.AlitaExcelLoader import AlitaExcelLoader
from document_loaders.AlitaDirectoryLoader import AlitaDirectoryLoader


ex_classes = {
    'DirectoryLoader': AlitaDirectoryLoader,
    'CSVLoader': AlitaCSVLoader,
    'ExcelLoader': AlitaExcelLoader
}

class LoaderInterface:
    def __init__(self, loader_name, **kwargs):    
        self.loader = LoaderInterface.get_loader_cls(loader_name)(**kwargs)
    
    @staticmethod
    def get_loader_cls(loader_name):
        if loader_name in ex_classes:
            loader = ex_classes[loader_name]
        elif loader_name in loaders:
            loader = getattr(
                __import__("langchain.document_loaders", fromlist=[loader_name]), loader_name
            )
        else:
            loader = getattr(
                __import__("langchain.document_loaders", fromlist=[loader_name]), 'TextLoader'
            )
        return loader

    def load(self, *args, **kwargs):
        return self.loader.load(*args, **kwargs)

    def load_and_split(self, *args, **kwargs):
        return self.loader.load_and_split(*args, **kwargs)
    
    def lazy_load(self, *args, **kwargs):
        return self.loader.lazy_load(*args, **kwargs)



def get_data(loader, load_params):
    if not load_params:
        load_params = {}
    try:
        doc_loader = loader.lazy_load(**load_params)
    except (NotImplementedError, TypeError):
        doc_loader = loader.load(**load_params)
    for _ in doc_loader:
        yield _        
    return


def loader(loader_name, loader_params, load_params):
    if loader_params.get('loader_cls'):
        loader_cls = LoaderInterface.get_loader_cls(loader_params.get('loader_cls'))
        loader_params['loader_cls'] = loader_cls   

    loader = LoaderInterface(loader_name, **loader_params)
    for document in get_data(loader, load_params):
        yield document