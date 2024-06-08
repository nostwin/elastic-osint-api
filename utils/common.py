from utils import logger


def handle_error(ex: Exception, file_name: str, function_name) -> None:
    print(f"{file_name} - {function_name}: {ex}")
    logger.error(f"{file_name} - {function_name}: {ex}")


def handle_info(file_name: str, function_name: str, message: str) -> None:
    print(f"{file_name} - {function_name}: {message}")
    logger.info(f"{file_name} - {function_name}: {message}")
