import os

BASE_PATH: str = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR_PATH: str = os.path.join(BASE_PATH, "config")
CONFIG_FILE_PATH: str = os.path.join(CONFIG_DIR_PATH, "settings.conf")
LOG_DIR_PATH: str = os.path.join(BASE_PATH, "logs")
LOG_FILE_PATH: str = os.path.join(LOG_DIR_PATH, "app.log")
TMP_DIR_PATH: str = os.path.join(BASE_PATH, "tmp")
PDF_TEMP_PATH: str = os.path.join(TMP_DIR_PATH, "temp_pdf.pdf")
EXTRACTOR_EXAMPLE: str = "https://s1.q4cdn.com/806093406/files/doc_downloads/test.pdf"
ANALYZER_EXAMPLE: str = "8.8.8.8"
SCRAPPER_EXAMPLE: str = "https://www.webscraper.io/contact"
