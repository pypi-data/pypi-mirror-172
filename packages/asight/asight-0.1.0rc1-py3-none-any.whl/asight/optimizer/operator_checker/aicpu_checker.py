"""
check aicpu operator optimization
"""
import logging
from typing import List

from common.profiling.summary import OpInfo
from common.profiling.task_time import TaskTime
from optimizer.operator_checker.operator_checker import OperatorChecker
from result.record_item import Suggestion

logger = logging.getLogger()


class AicpuChecker(OperatorChecker):
    """
    aicpu checker
    """
    _MIN_TASK_DURATION = 1000  # min task duration 1000us
    _MIN_TOTAL_DURATION_RATIO = 0.2
    _CHECKER = "aicpu operator"
    _PROBLEM = "aicpu operator"
    _description = "too many aicpu operators"
    _SUGGESTION: List[Suggestion] = [
        Suggestion("optimize data preprocess"),
        Suggestion("merge small kernel to super kernel"),
        Suggestion("modify model, eg:change int64 -> fp16"),
        Suggestion("modify code to avoid aicpu operator", True),
        Suggestion("optimize performance of aicpu operartor")
    ]
    _ITEMS = [
        "op_name", "op_type", "input_shapes", "input_data_types", "input_formats", "output_shapes", "output_data_types",
        "output_formats"
    ]
    _op_list: List[OpInfo] = []

    def _check_data(self, data):
        if not hasattr(data, "task_time"):
            logger.warning(self.SKIP_CHECK_MSG, self._CHECKER, "task time")
            return False
        if not self._check_summary(data):
            return False
        return True

    def check(self, profiling_data) -> bool:
        """
        check if any operator need optimize
        :param profiling_data: profiling datasest
        :return: true or false
        """
        if not self._check_data(profiling_data):
            return False
        block_aicpu_list = self._get_block_aicpu_list(profiling_data.task_time)
        block_aicpu_name_list = [block_aicpu.get_name() for block_aicpu in block_aicpu_list]
        total_task_duration = 0.0
        max_task_duration = 0.0
        for op_info in profiling_data.summary.op_list:
            if self._check_operator(op_info) and op_info.op_name in block_aicpu_name_list:
                self._op_list.append(op_info)
                task_duration = float(op_info.task_duration)
                total_task_duration += task_duration
                max_task_duration = max(max_task_duration, task_duration)
        if max_task_duration > self._MIN_TASK_DURATION:
            return True
        if total_task_duration > profiling_data.summary.get_total_task_duration() * self._MIN_TOTAL_DURATION_RATIO:
            return True
        return False

    def _check_operator(self, op_info) -> bool:
        if op_info.task_type != "AI_CPU":
            return False
        return True

    @classmethod
    def _get_block_aicpu_list(cls, task_time: TaskTime) -> list:
        aicpu_tasks = task_time.get_aicpu_tasks()
        aicore_tasks = task_time.get_aicore_tasks()
        block_aicpu_tasks = []
        idx = 0
        aicore_task_num = len(aicore_tasks)
        for i, aicpu_task in enumerate(aicpu_tasks):
            # find first aicore task end after aicpu_task start
            while idx < aicore_task_num and \
                    aicore_tasks[idx].get_starttime() + aicore_tasks[idx].get_dur() < aicpu_task.get_starttime():
                idx = idx + 1
            if idx == aicore_task_num:  # all aicpu task left start after aicore tasks
                block_aicpu_tasks.extend(aicpu_tasks[i:len(aicpu_tasks)])
                break
            # if aicore task start before aicpu task end, not blocking
            if aicore_tasks[idx].get_starttime() < aicpu_task.get_starttime() + aicpu_task.get_dur():
                continue
            block_aicpu_tasks.append(aicpu_task)
        task_list = block_aicpu_tasks + aicore_tasks
        task_list.sort(key=lambda x: x.get_starttime())
        return block_aicpu_tasks


def register(checker):
    """
    register aicpu checker to operator checker
    :param checker: checker
    """
    checker[AicpuChecker] = AicpuChecker()
