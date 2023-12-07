

from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from typing import List, Optional, Iterator
from charset_normalizer import from_path
from csv import DictReader
from json import dumps
from .AlitaTableLoader import AlitaTableLoader
from typing import Any

class AlitaCSVLoader(AlitaTableLoader):
    def __init__(self,
                 file_path: str,
                 encoding: Optional[str] = 'utf-8',
                 autodetect_encoding: bool = True,
                 json_documents: bool = True,
                 raw_content: bool = False,
                 columns: Optional[List[str]] = None):
        super().__init__(file_path=file_path, json_documents=json_documents, columns=columns, raw_content=raw_content)
        self.encoding = encoding
        self.autodetect_encoding = autodetect_encoding
        if autodetect_encoding:
            self.encoding = from_path(self.file_path).best().encoding
    
    def read_lazy(self) -> Iterator[dict]:
        with open(self.file_path, 'r', encoding=self.encoding) as fd:
            if self.raw_content:
                yield fd.read()
                return
            for row in DictReader(fd):
                yield row

    def read(self) -> Any:
        with open(self.file_path, 'r', encoding=self.encoding) as fd:
            if self.raw_content:
                return [fd.read()]
            return list(DictReader(fd))

