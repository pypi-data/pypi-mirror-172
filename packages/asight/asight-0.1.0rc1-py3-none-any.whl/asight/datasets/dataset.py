"""
dataset module
"""
import logging
import os

from config.config import Config

logger = logging.getLogger()


class Dataset:
    """
    dataset base class
    """
    _SHORT_ARG_NAME = ""
    _ARG_NAME = ""
    _HELP_MSG = ""

    def __init__(self, arg, _data: dict) -> None:
        config = Config()
        self._arg = os.path.abspath(os.path.join(config.get_work_path(), arg))
        logger.debug("init %s with %s", self.__class__.__name__, self._arg)

    @classmethod
    def get_key(cls):
        """
        get key of dataset
        :return: key
        """
        return cls.__module__.rsplit('.', maxsplit=1)[-1]

    def get_data_path(self):
        """
        get dataset path
        :return: path
        """
        return self._arg

    @classmethod
    def register(cls, datasets, parser):
        """
        register dataset to datasets
        :param datasets: datasets
        :param parser: arg parser
        :return:
        """
        key = cls.get_key()

        parser.add_argument(
            cls._SHORT_ARG_NAME, cls._ARG_NAME, dest=key, metavar="", help=cls._HELP_MSG, required=False
        )
        datasets[key] = cls


def register(_datasets, _parser):
    """
    register dataset to datasets
    :param datasets: datasets
    :param parser: arg parser
    """
