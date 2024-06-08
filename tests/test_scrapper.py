from typing import List, Dict, Any, Coroutine
import pytest
from tools import Scrapper


class TestScrapper:

    @pytest.mark.asyncio
    async def test_scrape_emails(self):
        url: str = 'https://s1.q4cdn.com/806093406/files/doc_downloads/test.pdf'
        result: list[dict[str, Any]] = await Scrapper.scrape_emails(url)
        print(result)

        assert result is not None
