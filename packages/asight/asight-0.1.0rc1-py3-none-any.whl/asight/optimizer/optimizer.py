"""
optimizer module
"""
import logging
from functools import wraps

from result.result import Result

logger = logging.getLogger()


class Optimizer:
    """
    optimizer base class
    """

    @classmethod
    def check_data(cls, data_list: tuple):
        """
        check if all data in data list is contained
        :param data_list: data list to check
        :return: func ptr if check success
        """

        def decorate(func):

            @wraps(func)
            def wrapper(self, data):
                if data is None:
                    return None
                for data_key in data_list:
                    if data_key not in data:
                        logger.warning("Skip %s because of not containing %s", self.__class__.__name__, data_key)
                        return None
                logger.info("Enable %s with %s", self.__class__.__name__, ",".join(data_list))
                return func(self, data)

            return wrapper

        return decorate

    def optimize(self, data) -> Result:
        """
        optimize
        :param data: input data
        """


def register(_optimizers):
    """
    register optimizer to optimizers
    :param optimizer: optimizer
    """
