

from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from typing import List, Optional, Iterator
from json import dumps
try:
    from document_loaders.utils import cleanse_data
except:
    from document_loaders.utils import cleanse_data

class AlitaTableLoader(BaseLoader):
    def __init__(self,
                 file_path: str,
                 json_documents: bool = True,
                 raw_content: bool = False,
                 columns: Optional[List[str]] = None):
        
        self.raw_content = raw_content
        self.file_path = file_path
        self.json_documents = json_documents
        self.columns = columns
    
    def read(self, lazy: bool = False):
        raise NotImplementedError("Excel loader is not implemented yet")
    
    def read_lazy(self) -> Iterator[dict]:
        raise NotImplementedError("Excel loader is not implemented yet")

    
    def row_processor(self, row: dict) -> str:
        # TODO: need to verify that document actually has columns
        if self.columns:
            row_slice = (
                str(row[column.strip()].lower())
                for column in self.columns
            )
            return cleanse_data('\n'.join(row_slice))
        else:
            return cleanse_data('\n'.join(str(value) for value in row.values()))

    def load(self) -> List[Document]:
        metadata = {"source": self.file_path}
        docs = []
        for row in self.read():
            if self.raw_content:
                docs.append(Document(page_content=row, metadata=metadata))
                continue
            if self.json_documents:
                print(row)
                metadata['columns'] = list(row.keys())
                metadata['og_data'] = dumps(row)
                docs.append(Document(page_content=self.row_processor(row), metadata=metadata))
            else:
                content = "\t".join([value for value in row.values()])
                docs.append(Document(page_content=content, metadata=metadata))
        return docs
    
    def lazy_load(self) -> Iterator[Document]:
        metadata = {"source": self.file_path}
        data = self.read_lazy()
        for row in data:
            if self.raw_content:
                yield Document(page_content=row, metadata=metadata)
                continue
            if self.json_documents:
                metadata['columns'] = list(row.keys())
                metadata['og_data'] = dumps(row)
                yield Document(page_content=self.row_processor(row), metadata=metadata)
            else:
                content = "\t".join([value for value in data.values()])
                yield Document(page_content=content, metadata=metadata)
        return
