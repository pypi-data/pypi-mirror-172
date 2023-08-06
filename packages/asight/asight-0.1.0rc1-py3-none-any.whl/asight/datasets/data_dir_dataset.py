"""
data directory dataset
"""
import logging

from datasets.dataset import Dataset

logger = logging.getLogger()


class DataDirDataset(Dataset):
    """
    data directory dataset
    """
    _SHORT_ARG_NAME = "-d"
    _ARG_NAME = "--data_dir"
    _HELP_MSG = "directory of all data."

    def __init__(self, arg, data: dict, datasets: dict) -> None:
        super().__init__(arg, data)
        for key in datasets:
            if key != self.get_key():
                datasets[key](arg, data, datasets)


def register(datasets, parser):
    """
    register data dir dataset to datasets
    :param datasets: datasets
    :param parser: arg parser
    """
    DataDirDataset.register(datasets, parser)
