"""
check block dim optimization
"""
import logging
from typing import List

from common.profiling.summary import OpInfo
from config.config import Config
from optimizer.operator_checker.operator_checker import OperatorChecker
from result.record_item import Suggestion

config = Config()
logger = logging.getLogger()


class BlockDimChecker(OperatorChecker):
    """
    block dim checker
    """
    _CHECKER = "block dim"
    _PROBLEM = "block dim"
    _description = "some operator does not make full use of {} cores"
    _SUGGESTION: List[Suggestion] = [
        Suggestion("optimize operator by AOE with job_type 2", True),
        Suggestion("optimize operator implementation")
    ]
    _ITEMS = [
        "op_name", "op_type", "task_duration", "income", "block_dim", "input_shapes", "input_data_types",
        "input_formats", "output_shapes", "output_data_types", "output_formats"
    ]

    _op_list: List[OpInfo] = []

    def _check_data(self, data):
        if not self._check_summary(data):
            return False
        if not config.get_config("ai_core_num"):
            logger.warning(self.SKIP_CHECK_MSG, self._CHECKER, "aicore core num in info.json.0 file")
            return False
        summary = data.summary
        op_info = summary.op_list[0]
        if not hasattr(op_info, "block_dim"):
            logger.warning(self.SKIP_CHECK_MSG, self._CHECKER, "block dim in op summary")
            return False
        self._description = self._description.format(config.get_config("ai_core_num"))
        return True

    def _check_operator(self, op_info) -> bool:
        if op_info.task_type == "AI_CPU":
            return False
        if int(op_info.block_dim) % config.get_config("ai_core_num") == 0:
            return False
        return True

    def _get_income(self, op_info: OpInfo) -> float:
        block_dim = int(op_info.get_attr("block_dim"))
        task_duration = float(op_info.get_attr("task_duration"))

        expect_block_dim = (block_dim // config.get_config("ai_core_num") + 1) * config.get_config("ai_core_num")
        if expect_block_dim == 0:
            return 0
        expect_block_duration = task_duration * block_dim / expect_block_dim
        income = task_duration - expect_block_duration
        return income


def register(checker):
    """
    register block dim checker to operator checker
    :param checker: checker
    """
    checker[BlockDimChecker] = BlockDimChecker()
