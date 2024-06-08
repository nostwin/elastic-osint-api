from typing import Any
import pytest
from tools import Extractor


class TestExtractor:

    @pytest.mark.asyncio
    async def test_extract_metadata_from_online_pdf(self):
        url: str = 'https://s1.q4cdn.com/806093406/files/doc_downloads/test.pdf'
        result = Extractor.extract_metadata_from_online_pdf(url)
        print(result)

        assert result is not None
