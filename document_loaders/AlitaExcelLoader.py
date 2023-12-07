

from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from typing import List, Optional, Iterator
from charset_normalizer import from_path
import pandas as pd
from json import dumps, loads

try:
    from document_loaders.AlitaTableLoader import AlitaTableLoader
except:
    from AlitaTableLoader import AlitaTableLoader

class AlitaExcelLoader(AlitaTableLoader):
    def read(self):
        df = pd.read_excel(self.file_path, sheet_name=None)
        docs = []
        for key in df.keys():
            if self.raw_content:
                docs.append(df[key].to_string())
            else:
                for record in loads(df[key].to_json(orient='records')):
                    docs.append(record)
        return docs

    def read_lazy(self) -> Iterator[dict]:
        df = pd.read_excel(self.file_path, sheet_name=None)
        for key in df.keys():
            if self.raw_content:
                yield df[key].to_string()
            else:
                for record in loads(df[key].to_json(orient='records')):
                    yield record
        return


if __name__ == '__main__':
    loader = AlitaExcelLoader('/Users/arozumenko/Development/embeddins_next/data/Code Quality/NA Rate Card 2022 v1.1 (1).xlsx')
    print(loader.load())
    for _ in loader.lazy_load():
        print(_)
        print('------------------')