"""
check operator optimization
"""
import logging
from typing import List

from common.profiling.summary import OpInfo
from datasets.profiling_dataset import ProfilingDataset
from result.record import OptimizeRecord
from result.record_item import OptimizeItem, StatisticsItem, Suggestion

MIN_TASK_DURATION = 20

logger = logging.getLogger()


class OperatorChecker:
    """
    operator checker
    """
    _MIN_TASK_DURATION = 20  # min task duration 20us
    _MIN_TOTAL_DURATION_RATIO = 1.0
    _CHECKER = str()
    _PROBLEM = str()
    _description = str()
    _SUGGESTION: List[Suggestion] = []
    _ITEMS: List[str] = []
    SKIP_CHECK_MSG = "Skip %s checker because of not containing %s"
    _op_list: List[OpInfo] = []

    def __init__(self) -> None:
        self._op_list: List[OpInfo] = []

    def _check_summary(self, data: ProfilingDataset):
        if not hasattr(data, "summary"):
            logger.warning(self.SKIP_CHECK_MSG, self._CHECKER, "op summary")
            return False
        return True

    def _check_data(self, _data):
        return True

    def _check_operator(self, _op_info):
        return False

    def check(self, profiling_data: ProfilingDataset) -> bool:
        """
        check if any operator need optimize
        :param profiling_data: profiling datasest
        :return: true or false
        """
        if not self._check_data(profiling_data):
            return False
        summary = profiling_data.summary
        total_task_duration = 0.0
        max_task_duration = 0.0
        for op_info in summary.op_list:
            if not self._check_operator(op_info):
                continue
            task_duration = float(op_info.task_duration)
            total_task_duration += task_duration
            max_task_duration = max(max_task_duration, task_duration)
            self._op_list.append(op_info)
        if max_task_duration > self._MIN_TASK_DURATION:
            return True
        if total_task_duration > summary.get_total_task_duration() * self._MIN_TOTAL_DURATION_RATIO:
            return True
        return False

    def _get_income(self, _op_info: OpInfo) -> float:
        return 0

    def make_record(self, profiling_data: ProfilingDataset) -> OptimizeRecord:
        """
        make record for what and how to optimize
        :param profiling_data: profiling data
        :return: optimize record
        """
        task_duration_list = [float(op_info.get_attr("task_duration")) for op_info in self._op_list]
        total_cost_time = sum(task_duration_list)
        total_task_duration = profiling_data.summary.get_total_task_duration()
        count = len(task_duration_list)
        income = self._get_incomes(self._op_list)
        op_type_list = self._get_op_type_list(self._op_list)
        statistics_item = StatisticsItem(total_task_duration, total_cost_time, count, income)
        optimization_item = OptimizeItem(self._PROBLEM, self._description, op_type_list, self._SUGGESTION)
        return OptimizeRecord(optimization_item, statistics_item)

    def _get_op_type_list(self, op_list: list):
        op_type_list = []
        for op_info in op_list:
            if op_info.op_type not in op_type_list:
                op_type_list.append(op_info.op_type)
        return op_type_list

    def _get_incomes(self, op_list: list) -> float:
        incomes = 0.0
        for op_info in op_list:
            income = self._get_income(op_info)
            setattr(op_info, "income", round(income, 2))
            incomes += income
        return incomes

    @classmethod
    def get_name(cls):
        """
        get name of checker
        :return: checker name
        """
        return cls._PROBLEM

    def get_details(self) -> list:
        """
        get details of operator to be optimized
        :return: detail list
        """
        op_list = self._op_list
        if not op_list:
            return []
        details = []
        attrs = [attr for attr in self._ITEMS if op_list[0].has_attr(attr)]
        details.append(attrs)
        op_list = sorted(op_list, key=lambda x: float(x.get_attr("task_duration")), reverse=True)
        for op_info in op_list:
            content = [op_info.get_attr(attr) for attr in attrs]
            details.append(content)
        return details

    @staticmethod
    def get_ratio(op_info: OpInfo, attr: str) -> float:
        """
        get value of attr which type is ratio
        :param op_info: information of operator
        :param attr: attr name
        :return: ratio of attr value
        """
        if not op_info.has_attr(attr):
            return 0
        value = op_info.get_attr(attr)
        if not value or value == "N/A":
            return 0
        return float(value)


def register(_checker):
    """
    register checker to operator checker
    :param checker: checker
    """
