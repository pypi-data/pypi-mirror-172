"""
check mte2 bound optimization
"""
import logging
from typing import List

from common.profiling.summary import OpInfo
from optimizer.operator_checker.operator_checker import OperatorChecker
from result.record_item import Suggestion

logger = logging.getLogger()


class Mte2BoundChecker(OperatorChecker):
    """
    mte2 bound checker
    """
    _CHECKER = "mte2 bound"
    _PROBLEM = "mte2 bound"
    _description = "mte2 ratio is more than 80%"
    _SUGGESTION = [Suggestion("optimize operator by AOE with job_type 1", True)]
    _ITEMS = [
        "op_name", "op_type", "task_type", "task_duration", "mte2_ratio", "block_dim", "input_shapes",
        "input_data_types", "input_formats", "output_shapes", "output_data_types", "output_formats"
    ]

    _op_list: List[OpInfo] = []

    def _check_data(self, data):
        if not self._check_summary(data):
            return False
        summary = data.summary
        op_info = summary.op_list[0]
        if not op_info.has_attr("mte2_ratio"):
            logger.warning(self.SKIP_CHECK_MSG, self._CHECKER, "mte2_ratio in op summary")
            return False
        return True

    def _check_operator(self, op_info) -> bool:
        if op_info.task_type == "AI_CPU":
            return False
        ratio = self.get_ratio(op_info, "mte2_ratio")
        if not ratio:
            return False
        if ratio > 0.8:
            return True
        return False


def register(checker):
    """
    register mte2 bound checker to operator checker
    :param checker: checker
    """
    checker[Mte2BoundChecker] = Mte2BoundChecker()
