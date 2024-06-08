import logging
from logging import Logger
from constants import LOG_DIR_PATH, LOG_FILE_PATH
import os

if not os.path.exists(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH)

log_format: str = '%(asctime)s :: %(levelname)s :: %(message)s'
logging.basicConfig(level=logging.INFO, filename=LOG_FILE_PATH, filemode="a", format=log_format)
logger: Logger = logging.getLogger(__name__)




