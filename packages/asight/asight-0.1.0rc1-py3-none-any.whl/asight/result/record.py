"""
result record
"""


class Record:
    """
    record base class
    """

    def format(self):
        """
        format record to list
        :return: list
        """

    def format_title(self):
        """
        format record title to list
        :return: list
        """


class OptimizeRecord(Record):
    """
    optimize record
    """

    def __init__(self, optimization_item, statistics_item) -> None:
        self.optimization_item = optimization_item
        self.statistics_item = statistics_item

    def __lt__(self, other):
        return self.statistics_item.task_duration > other.statistics_item.task_duration

    def format(self):
        """
        format record to list
        :return: list
        """
        return self.optimization_item.format() + self.statistics_item.format()

    def format_title(self):
        """
        format record title to list
        :return: list
        """
        return [self.optimization_item.format_title() + self.statistics_item.format_title()]


class DetailRecord(Record):
    """
    detail record
    """

    def __init__(self, detail: list) -> None:
        self.detail = detail

    def format_title(self):
        """
        format record title to list
        :return: list
        """
        title = [self.detail]
        # write detail as title, so no need to write as text again
        self.detail = None
        return title

    def format(self):
        """
        format record to list
        :return: list
        """
        return self.detail
