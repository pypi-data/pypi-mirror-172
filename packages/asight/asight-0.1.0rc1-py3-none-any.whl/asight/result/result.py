"""
all kind of result module
"""
import logging
from typing import List

from config.config import Config
from result.record import DetailRecord, OptimizeRecord, Record
from util.common import create_directory_for_file
from util.excel import Excel, Sheet
from util.singleton import singleton

logger = logging.getLogger()


class Form:
    """
    excel form
    """

    def __init__(self, name, page) -> None:
        self.name = name
        self.page = page
        self.record_list: List[Record] = []

    @staticmethod
    def _write_title(sheet: Sheet, title, sub_title_list: list):
        sub_title: List[str] = sum(sub_title_list, [])
        title_col_nums = [len(sub_title) for sub_title in sub_title_list]
        if len(title) == 1:
            title_col_nums = [sum(title_col_nums)]
        sheet.write_title(title, title_col_nums)
        sheet.write_title(sub_title)

    def show(self, sheet: Sheet):
        """
        show content of form
        """
        if not self.record_list:
            return
        try:
            self.record_list = sorted(self.record_list)
        except TypeError:
            pass
        record = self.record_list[0]
        title = [self.name]
        sub_title_list = record.format_title()
        self._write_title(sheet, title, sub_title_list)
        for record in self.record_list:
            sheet.write_text(record.format())

    def add_record(self, record):
        """
        add record to form
        """
        self.record_list.append(record)


class Page:
    """
    excel page
    """

    def __init__(self, name, need_index=False) -> None:
        self.name = name
        self.need_index = need_index
        self.form_dict: dict[str, Form] = {}  # {form_name, Form}

    def show(self, excel: Excel):
        """
        show content of page
        """
        sheet = excel.get_sheet(self.name)
        for form in self.form_dict.values():
            form.show(sheet)

    def add_form(self, name):
        """
        add form to page
        """
        if name in self.form_dict:
            return self.form_dict[name]
        form = Form(name, self)
        self.form_dict[name] = form
        return form


class Result:
    """
    result base class
    """

    def __init__(self, result_file: str) -> None:
        self.page_dict: dict[str, Page] = {}  # {page_name, Page}
        self.record: List[Record] = []
        self._result_file = result_file
        create_directory_for_file(self._result_file)

    def add_page(self, name, need_index=False):
        """
            add page to excel
        """
        if name in self.page_dict:
            return self.page_dict[name]
        page = Page(name, need_index)
        self.page_dict[name] = page
        return page

    def show(self):
        """
           show result
        """
        excel = Excel(self._result_file, auto_format=True, need_idx=False)
        if not self.page_dict:
            return
        logger.info("Save result to file %s", self._result_file)
        for page in self.page_dict.values():
            page.show(excel)
        excel.save()


@singleton
class OptimizeResult(Result):
    """
       result of optimize
    """

    def __init__(self) -> None:
        config = Config()
        super().__init__(config.analysis_result_file)

    def add(self, record: OptimizeRecord):
        """
          add record to result
        """
        page = self.add_page("overview", need_index=True)
        form = page.add_form("overview")
        form.add_record(record)

    def add_detail(self, name, record: DetailRecord):
        """
          add detail records to result
        """
        page = self.add_page(name, need_index=True)
        form = page.add_form(name)
        form.add_record(record)
