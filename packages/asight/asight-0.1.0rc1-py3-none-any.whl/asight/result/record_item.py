"""
item of record
"""
import logging

from util.common import to_percent

logger = logging.getLogger()


class Suggestion:
    """
    optimize suggestion
    """

    def __init__(self, value, release=False) -> None:
        self._str = value
        self._release = release

    def get_str(self):
        """
        get string of suggestion
        :return: str
        """
        return self._str

    def is_release(self):
        """
        is release suggestion or not
        :return: bool
        """
        return self._release


class RecordItem:
    """
    record item base class
    """

    def format(self):
        """
        format item to list
        :return: list
        """

    def format_title(self):
        """
        format title to list
        :return: list
        """


class OptimizeItem(RecordItem):
    """
    optimize item
    """

    def __init__(self, problem: str, description: str, op_type_list: list, suggestion: list) -> None:
        self.problem = problem
        self.description = description
        self.op_type_list = op_type_list
        self.suggestion = suggestion

    def print_release_suggestion(self, description, release_suggestion_list):
        """
        print suggestions that can be applied by user to screen
        """
        logger.out("")
        logger.out("Problem detected:")
        if self.op_type_list:
            op_type = ", ".join(self.op_type_list)
            logger.out(f"    {description}, op type : {op_type}")
        else:
            logger.out(f"    {description}")
        logger.out("Recommonded change:")
        for suggestion in release_suggestion_list:
            logger.out(f"    {suggestion}")

    def format(self):
        """
        format item to list
        :return: list
        """
        release_suggestion_list = []
        debug_suggestion_list = []
        for suggestion in self.suggestion:
            debug_suggestion_list.append(suggestion.get_str())
            if suggestion.is_release():
                release_suggestion_list.append(suggestion.get_str())
        if release_suggestion_list:
            self.print_release_suggestion(self.description, release_suggestion_list)
        for idx, _ in enumerate(debug_suggestion_list):
            debug_suggestion_list[idx] = f"{idx + 1}.{debug_suggestion_list[idx]}"
        return [self.problem, self.description, ("\n").join(debug_suggestion_list)]

    def format_title(self):
        return ["problem", "description", "suggestion"]


class StatisticsItem(RecordItem):
    """
    statistics item
    """

    def __init__(self, total_task_duration, task_duration, count, income=None) -> None:
        self.count = count
        self.total_task_duration = total_task_duration
        self.task_duration = task_duration
        self.task_duration_ratio = task_duration / total_task_duration if total_task_duration != 0 else 0
        if income is not None:
            self.income = income
            self.income_ratio = income / total_task_duration if total_task_duration != 0 else 0
        else:
            self.income = 0
            self.income_ratio = 0

    def format(self):
        """
        format item to list
        :return: list
        """
        return [
            self.count,
            round(self.task_duration, 2),
            to_percent(self.task_duration_ratio),
            round(self.income, 2),
            to_percent(self.income_ratio)
        ]

    def format_title(self):
        """
        format title to list
        :return: list
        """
        return ["problem count", "total_time(us)", "time ratio", "income(us)", "income ratio"]
