"""
profiling directory dataset
"""
import logging

from common.profiling.profiling_info import ProfilingInfo
from common.profiling.summary import Summary
from common.profiling.task_time import TaskTime
from datasets.dataset import Dataset

logger = logging.getLogger()


class ProfilingDataset(Dataset):
    """
    profiling directory dataset
    """
    _SHORT_ARG_NAME = "-p"
    _ARG_NAME = "--profiling_dir"
    _HELP_MSG = "directory of profiling output files."

    def __init__(self, arg, data: dict, _datasets: dict) -> None:
        super().__init__(arg, data)
        self.profiling_dir = self._arg
        if self._parse():
            data[self.get_key()] = self

    def _parse(self):
        result = False
        info = ProfilingInfo(self.profiling_dir)
        if info.parse_data():
            self.info = info
        summary = Summary(self.profiling_dir)
        if summary.parse_data():
            result = True
            self.summary = summary
        task_time = TaskTime(self.profiling_dir)
        if task_time.parse_data():
            result = True
            self.task_time = task_time
        return result


def register(datasets, parser):
    """
    register profiling dir dataset to datasets
    :param datasets: datasets
    :param parser: arg parser
    """
    ProfilingDataset.register(datasets, parser)
