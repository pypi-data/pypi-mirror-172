"""
check operator bound optimization
"""
import logging
from typing import List

from common.profiling.summary import OpInfo
from optimizer.operator_checker.operator_checker import OperatorChecker
from result.record_item import Suggestion

logger = logging.getLogger()


class OperatorBoundChecker(OperatorChecker):
    """
    operator bound checker
    """
    _CHECKER = "operator no bound"
    _PROBLEM = "operator no bound"
    _MIN_TOTAL_DURATION_RATIO = 0.2
    _description = "none of mte, cube, vector, scalar ratio is more than 80%"
    _SUGGESTION: List[Suggestion] = [Suggestion("optimize operator by AOE with job_type 2", True)]
    _ITEMS = [
        "op_name", "op_type", "task_type", "task_duration", "vec_ratio", "mac_ratio", "scalar_ratio", "mte1_ratio",
        "mte2_ratio", "mte3_ratio", "block_dim", "input_shapes", "input_data_types", "input_formats", "output_shapes",
        "output_data_types", "output_formats"
    ]

    _op_list: List[OpInfo] = []

    def _check_data(self, data):
        if not self._check_summary(data):
            return False
        return True

    def _check_operator(self, op_info) -> bool:
        bound_list = ["vec_ratio", "mac_ratio", "scalar_ratio", "mte1_ratio", "mte2_ratio", "mte3_ratio"]
        ratio_list = [self.get_ratio(op_info, attr) for attr in bound_list]
        if not any(ratio_list):
            return False  # no data, skip check
        if any(ratio and ratio > 0.8 for ratio in ratio_list):
            return False
        return True


def register(checker):
    """
    register operator bound checker to operator checker
    :param checker: checker
    """
    checker[OperatorBoundChecker] = OperatorBoundChecker()
