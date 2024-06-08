from configparser import ConfigParser
from typing import Any
from utils import logger
from constants import CONFIG_FILE_PATH


def get_vt_config() -> str:
    try:
        config: ConfigParser = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        api_key: str = config['VT'].get("api_key")
        return api_key
    except Exception as e:
        print(f"{__file__} - {get_vt_config.__name__}: {e}")
        logger.info(f"{__file__} - {get_vt_config.__name__}: {e}")


def get_elastic_config() -> dict[str, Any]:
    try:
        config: ConfigParser = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        api_host: str = config['Elastic'].get("api_host")
        enabled: bool = config['Elastic'].get("enabled")
        return {"api_host": api_host, "enabled": enabled}
    except Exception as e:
        print(f"{__file__} - {get_elastic_config.__name__}: {e}")
        logger.info(f"{__file__} - {get_elastic_config.__name__}: {e}")
