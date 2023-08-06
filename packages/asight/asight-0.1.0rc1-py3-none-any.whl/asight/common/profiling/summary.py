"""
summary
"""
import csv
import logging
from typing import List

from common.profiling.profiling_info import get_last_file_by_step
from util.common import format_excel_title, get_file_from_directory

logger = logging.getLogger()


class OpInfo:
    """
    op info
    """
    _attr_pre_fix_list = ["", "aic_"]

    def add_attr(self, key: str, value: str):
        """
        add attr to op info
        :param key: op info key
        :param value: op info value
        :return: None
        """
        if hasattr(self, key):
            return
        setattr(self, key, value)

    def has_attr(self, key: str):
        """
        check if op info has attr key
        :param key: attr key
        :return: true or false
        """
        for prefix in self._attr_pre_fix_list:
            attr = prefix + key
            if hasattr(self, attr):
                return True
        return False

    def get_attr(self, key):
        """
        get attr value by key
        :param key: attr key
        :return: attr value
        """
        for prefix in self._attr_pre_fix_list:
            attr = prefix + key
            if hasattr(self, attr):
                return getattr(self, attr)
        return 0

    def get_attrs(self) -> dict:
        """
        get attr list
        :return: attr list
        """
        return self.__dict__


class Summary:
    """
    op summary
    """

    def __init__(self, path: str) -> None:
        self._path = path
        self.op_list: List[OpInfo] = []
        self._total_task_duration = 0.0
        self._total_task_wait_time = 0.0

    def parse_data(self) -> bool:
        """
        parse op summary info
        :return: true or false
        """

        file_list = get_file_from_directory(self._path, lambda x: (x.startswith("op_summary_")) and x.endswith(".csv"))
        if not file_list:
            logger.warning("Cannot find op_summary_*.csv under %s", self._path)
            return False
        file = get_last_file_by_step(file_list)
        if len(file_list) > 1:
            logger.info("Multiple copies of summary data were found, use %s", file)
        return self._parse(file)

    @staticmethod
    def _check_summary_file_format(op_summary: list):
        if not op_summary:
            logger.error("Op summary file is empty")
            return False
        idx = 0
        col = 0
        for row in op_summary:
            idx += 1
            if idx == 1:
                col = len(row)
                continue
            if len(row) != col:
                logger.error("Line %s of op summary file does not have the same len with oher lines", idx)
                return False
        return True

    def _parse(self, summary_file: str):
        logger.debug("Parse file %s", summary_file)
        op_summary_data = []
        with open(summary_file, encoding="utf-8") as op_summary_file:
            try:
                op_summary = csv.reader(op_summary_file)
            except OSError as error:
                logger.error("Read op summary file failed : %s", error)
                return False
            for row in op_summary:
                op_summary_data.append(row)
            if not self._check_summary_file_format(op_summary_data):
                logger.error("Invalid op summary file : %s", op_summary_file)
                return False
            title_dict: dict[int, str] = {}
            for idx, title in enumerate(op_summary_data[0]):
                title_dict[idx] = format_excel_title(title)
            for op_data in op_summary_data[1:]:
                op_info = OpInfo()
                for idx, value in enumerate(op_data):
                    key = title_dict.get(idx)
                    if key:
                        op_info.add_attr(key, value)
                self.op_list.append(op_info)
                self._total_task_duration += float(op_info.get_attr("task_duration"))
                self._total_task_wait_time += float(op_info.get_attr("task_wait_time"))
        if not self.op_list:
            logger.error("No valid op info in %s", summary_file)
            return False
        return True

    def get_total_task_duration(self):
        """
        get total task duration of all operators
        :return:
        """
        return self._total_task_duration
