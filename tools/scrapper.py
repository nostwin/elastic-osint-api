from typing import Any
import requests
from bs4 import BeautifulSoup
import re
from utils import handle_error


class Scrapper:

    @staticmethod
    async def scrape_emails(url: str) -> list[dict[str, Any]]:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
                text: str = soup.get_text()
                emails: list[str] = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}", text)
                return Scrapper._process_data(emails, url)
            else:
                print("Failed to retrieve webpage:", response.status_code)

        except Exception as e:
            handle_error(e, __file__, Scrapper.scrape_emails.__name__)

    @staticmethod
    def _process_data(data: list[str], source: str) -> list[dict[str, Any]]:
        try:
            processed_data: list[dict[str, Any]] = []
            for item in data:
                data_dict: dict[str, Any] = {'source': source, 'email_value': item}
                processed_data.append(data_dict)

            return processed_data

        except Exception as e:
            handle_error(e, __file__, Scrapper._process_data.__name__)
