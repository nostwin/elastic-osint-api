import os
from typing import Any
import PyPDF2
import requests
from PyPDF2 import PdfReader
from requests import Response
from utils.common import handle_error, handle_info
from constants import PDF_TEMP_PATH


class Extractor:

    @staticmethod
    async def extract_metadata_from_online_pdf(url: str) -> dict[str, Any] | None:
        try:
            metadata: dict[str, Any]
            response: Response = requests.get(url)

            if response.status_code == 200:
                with open(PDF_TEMP_PATH, "wb") as f:
                    f.write(response.content)

                with open(PDF_TEMP_PATH, "rb") as f:
                    pdf_reader: PdfReader = PyPDF2.PdfReader(f)
                    metadata = pdf_reader.metadata

                return Extractor._process_data(metadata, url)

            else:
                handle_info(f"{response.status_code}: {response.text}", __file__, Extractor.extract_metadata_from_online_pdf.__name__)
                return None

        except Exception as e:
            handle_error(e, __file__, Extractor.extract_metadata_from_online_pdf.__name__)
            return None

    @staticmethod
    def _process_data(data: dict[str, Any], source: str) -> dict[str, Any]:
        try:
            processed_data = {key.lstrip('/'): value for key, value in data.items() if value is not None}
            processed_data['file_name'] = os.path.basename(source)
            processed_data['source'] = source

            return processed_data

        except Exception as e:
            handle_error(e, __file__, Extractor._process_data.__name__)
