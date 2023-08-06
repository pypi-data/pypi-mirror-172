"""
asight config
"""
import os
from configparser import ConfigParser

from util.singleton import singleton


@singleton
class Config:
    """
    config
    """

    _CONFIG_DIR_NAME = "config"
    _CONFIG_FILE_NAME = "config.ini"
    _config = ConfigParser(allow_no_value=True)
    _work_path = os.path.abspath("")  # pwd
    _root_path = os.path.abspath(os.path.join(__file__, "../../"))  # asight/
    _config.read(os.path.join(_root_path, _CONFIG_DIR_NAME, _CONFIG_FILE_NAME))

    def __init__(self) -> None:
        # LOG
        self._console_logging_level = self._config.get("LOG", "console_logging_level").upper()
        # outputs
        self.analysis_result_file = self._normalize_path(self._config.get("OUTPUT", "analysis_result_file"))

    def get_console_log_level(self) -> str:
        """
        get console log level
        :return: console log level
        """
        return self._console_logging_level

    @classmethod
    def _normalize_path(cls, file) -> str:
        if not file.startswith("/"):
            file = os.path.join(cls._work_path, file)
        return os.path.abspath(file)

    @classmethod
    def get_work_path(cls) -> str:
        """
        get work path
        :return: work path
        """
        return cls._work_path

    @classmethod
    def get_root_path(cls) -> str:
        """
        get root path
        :return: root path
        """
        return cls._root_path

    def set_config(self, key, value) -> None:
        """
        set config value
        :param key: config key
        :param value: config value
        """
        setattr(self, key, value)

    def get_config(self, key) -> str:
        """
        get value of config
        :param key: config key
        :return: config value
        """
        try:
            return getattr(self, key)
        except AttributeError:
            return ""
