from typing import Any

import pytest
from tools import Analyzer
from utils import get_vt_config


class TestAnalyzer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.analyzer: Analyzer = Analyzer(get_vt_config())

    def test_analyze_ip(self):
        ip: str = "8.8.8.8"
        results = self.analyzer.analyze_ip(ip)
        print(results)

        assert results is not None
