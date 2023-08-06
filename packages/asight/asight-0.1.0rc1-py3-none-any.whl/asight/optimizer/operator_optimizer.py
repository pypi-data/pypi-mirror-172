"""
operator optimizer module
"""
from datasets.profiling_dataset import ProfilingDataset
from optimizer.optimizer import Optimizer
from result.result import DetailRecord, OptimizeResult, Result
from util.common import load_module


class OperatorOptimizer(Optimizer):
    """
    operator optimizer
    """

    def __init__(self) -> None:
        self.checker = load_module("optimizer/operator_checker")
        self.result = None

    @Optimizer.check_data((ProfilingDataset.get_key(), ))
    def optimize(self, data) -> Result:
        """
        optimize operator
        :param data: input datasets
        :return: result
        """
        self.result = OptimizeResult()
        profiling_data = data[ProfilingDataset.get_key()]
        self._check(profiling_data)
        return self.result

    def _check(self, profiling_data):
        for _, checker in self.checker.items():
            if checker.check(profiling_data):
                record = checker.make_record(profiling_data)
                self.result.add(record)
                details = checker.get_details()
                if not details:
                    continue
                for detail in details:
                    self.result.add_detail(checker.get_name(), DetailRecord(detail))


def register(optimizers):
    """
    register operator optimizer to optimizers
    :param optimizer: optimizer
    """
    optimizers[OperatorOptimizer] = OperatorOptimizer()
