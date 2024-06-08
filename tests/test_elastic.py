from typing import Any
import pytest
from model.elastic import Elastic
from utils.configuration import get_elastic_config


class TestElastic:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.elastic: Elastic = Elastic(get_elastic_config())

    @pytest.mark.asyncio
    async def test_search(self):
        index: str = "files"
        results: dict | None = await self.elastic.search(index)
        print(dict(results))
        assert results is not None

    @pytest.mark.asyncio
    async def test_index_document(self):
        index: str = "emails"
        document: dict[str, Any] = {'source': 'https://test', 'email_value': '03012736@test.es'}
        results = self.elastic.index_documents(index, document)
        print(results)
        assert results is not None

    def test_delete_index(self):
        index: str = "emails"
        results = self.elastic.delete_index(index)
        print(results)
        assert results is not None
