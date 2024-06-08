from typing import Any
from elasticsearch import Elasticsearch
from utils import handle_error


class Elastic:
    def __init__(self, elastic_endpoint: str):
        self.elastic: Elasticsearch = Elasticsearch(elastic_endpoint)

    async def search(self, index: str) -> dict | None:
        try:
            return self.elastic.search(index=index)
        except Exception as e:
            handle_error(e, __file__, self.search.__name__)

    async def index_documents(self, index: str, documents: list[dict[str, Any]]) -> bool:
        try:
            for documents in documents:
                self.elastic.index(index=index, document=documents)
            return True
        except Exception as e:
            handle_error(e, __file__, self.index_documents.__name__)
            return False

    async def index_document(self, index: str, document: dict[str, Any]) -> object | None:
        try:
            return self.elastic.index(index=index, document=document)
        except Exception as e:
            handle_error(e, __file__, self.index_documents.__name__)
            return None

    async def delete_index(self, index: str) -> object | None:
        try:
            return self.elastic.indices.delete(index=index)
        except Exception as e:
            handle_error(e, __file__, self.delete_index.__name__)
            return None
