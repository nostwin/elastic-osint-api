from typing import Any
import requests
from utils import get_vt_config, handle_error, handle_info


class Analyzer:
    def __init__(self, api_key: str):
        self.api_key: str = api_key

    async def analyze_ip(self, ip: str) -> dict[str, Any] | None:
        try:
            url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
            headers = {
                'x-apikey': self.api_key
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return self._process_data(response.json().get('data').get('attributes'), ip)
            else:
                handle_info(f"Status code: {response.status_code}", __file__, self._process_data.__name__)
                return None

        except Exception as e:
            handle_error(e, __file__, self.analyze_ip.__name__)
            return None

    def _process_data(self, data: dict[Any, Any], source: str) -> dict[str, Any]:
        try:
            fields: list[str] = ['reputation', 'continent', 'last_analysis_stats', 'as_owner', 'country', 'whois']
            processed_data = {key: value for key, value in data.items() if value is not None and key in fields}
            processed_data['source'] = source
            processed_data['whois'] = processed_data['whois'].split('\n')

            return processed_data

        except Exception as e:
            handle_error(e, __file__, self._process_data.__name__)

