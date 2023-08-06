"""
log module
"""
import logging

from config.config import Config


def init_logger() -> logging.Logger:
    """
    init logger
    """
    logging.logThreads = False
    logging.logMultiprocessing = False
    logging.logProcesses = False

    level_mapping = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    class LevelFilter(logging.Filter):
        """
        level filter, filer only log with level out
        """

        # pylint:disable=too-few-public-methods
        def filter(self, record):
            if record.levelno == 60:
                return False
            return True

    config = Config()
    console_log_level = level_mapping.get(config.get_console_log_level(), logging.INFO)
    console_handle = logging.StreamHandler()
    console_handle.setLevel(console_log_level)
    console_handle.addFilter(LevelFilter())
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s]%(message)s")
    console_handle.setFormatter(formatter)

    # add log level out
    logging.addLevelName(60, 'OUT')
    logger = logging.getLogger()
    setattr(logger, 'out', lambda *args: logger.log(60, *args))
    output_handle = logging.StreamHandler()
    output_handle.setLevel("OUT")
    formatter = logging.Formatter("%(message)s")
    output_handle.setFormatter(formatter)

    logger.setLevel("DEBUG")
    logger.handlers = []
    if not logger.handlers:
        logger.addHandler(console_handle)
        logger.addHandler(output_handle)
    else:
        logger.info(logger.handlers)
    logger.debug("The logger of analysis have initialized successfully.")
    return logger
