"""
excel module
"""
import dataclasses
import logging
import os

import xlsxwriter

logger = logging.getLogger()

FORMAT_LIST = {
    "TITLE_FORMAT": {
        "bold": True,
        "color": "#FFFFFF",
        "bg_color": "#187498",
        "align": "center",
        "border": 1
    },
    "TEXT_FORMAT": {
        "bold": False,
        "align": "left",
        "valign": "top",
        "border": 1
    },
    "HIGHLIGHT_FORMAT": {
        "bold": False,
        "align": "left",
        "valign": "top",
        "border": 1,
        "bg_color": "#EB5353"
    },
    "WELL_FORMAT": {
        "bold": False,
        "align": "left",
        "valign": "top",
        "border": 1,
        "bg_color": "#36AE7C"
    }
}
MAX_WIDTH = 50
MIN_WIDTH = 2


@dataclasses.dataclass
class SheetAttr:
    """
    sheet attr
    """
    need_idx: bool
    auto_format: bool
    limit_max_width: bool


class Sheet:
    """
    sheet clss
    """

    def __init__(self, excel, sheet: xlsxwriter.worksheet.Worksheet, need_idx: bool, limit_max_width: bool) -> None:
        self._excel = excel
        self.width: list[float] = []
        self._row = 0
        self._idx = 0
        self._col = 0
        self.sheet = sheet
        self.attr = SheetAttr(need_idx=need_idx, auto_format=True, limit_max_width=limit_max_width)

    def set_auto_format(self, auto_format: bool) -> None:
        """
        set auto format attr
        :param auto_format: true or false
        :return:
        """
        self.attr.auto_format = auto_format

    def write_title(self, content: list, col_nums: list = None) -> None:
        """
        write title for sheet
        """
        if self.attr.need_idx:
            if col_nums:
                col_nums.insert(0, 1)
                content.insert(0, "")
            else:
                content.insert(0, "idx")
        if self.attr.auto_format and not col_nums:  # adjust format only by sub_title
            self._adjust_format(content, factor=1.1)
        self._write_row(self._row, content, self._excel.get_format("TITLE_FORMAT"), col_nums)
        self._row += 1
        self._idx = 1

    def _merge_col(self, cols: list, row: int, data: str, cell_format: xlsxwriter.format.Format) -> None:
        """
        merge col
        """
        self.sheet.merge_range(row, cols[0], row, cols[1], data, cell_format)

    def _write_row(self, row: int, content: list, style: xlsxwriter.format.Format, col_nums) -> int:
        """
        write row to excel
        """
        if col_nums:
            first_col = 0
            idx = 0
            for cell_content in content:
                if idx >= len(col_nums):
                    break
                last_col = first_col + col_nums[idx] - 1
                idx += 1
                if first_col == last_col:
                    self.sheet.write(row, first_col, cell_content, style)
                else:
                    self._merge_col([first_col, last_col], row, cell_content, style)
                first_col = last_col + 1
        else:
            col = 0
            self.sheet.write_row(row, col, content, style)
        return row + 1

    def _adjust_format(self, content: list, factor: float = 1.0) -> None:
        width = []
        for attr in content:
            width.append(max(len(line.encode()) * factor for line in str(attr).split('\n')))
        if not self.width:
            self.width = width
            return
        min_len = min(len(self.width), len(width))
        max_len = max(len(self.width), len(width))
        for i in range(0, min_len):
            self.width[i] = max(self.width[i], width[i])
        if len(width) <= len(self.width):
            return
        for _ in range(min_len, max_len):
            self.width.append(max_len)

    def write_text(self, content: list, text_format="TEXT_FORMAT", col_nums: list = None) -> None:
        """
        write text for sheet
        """
        if not content:
            return
        if self.attr.need_idx:
            content.insert(0, self._idx)
        if self.attr.auto_format:
            self._adjust_format(content)
        self._write_row(self._row, content, self._excel.get_format(text_format), col_nums)
        self._row += 1
        self._idx += 1


class Excel:
    """
    excel class
    """

    def __init__(self, filename: str, auto_format=False, need_idx=True) -> None:
        filename = os.path.abspath(filename)
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        self._filename = filename
        self._excel_file = xlsxwriter.Workbook(filename)
        self._formats: dict[str, xlsxwriter.format.Format] = {}
        self._need_idx = need_idx
        for format_name, format_value in FORMAT_LIST.items():
            excel_format = self._excel_file.add_format(format_value)
            if auto_format:
                excel_format.set_text_wrap(True)
            self._formats[format_name] = excel_format
        self.sheets: dict[str, Sheet] = {}  # {sheet_name, Sheet}

    def get_format(self, name: str) -> xlsxwriter.format.Format:
        """
        get format
        """
        return self._formats.get(name)

    def add_sheet(self, sheet_name: str, need_idx=False, limit_max_width=True) -> Sheet:
        """
        add sheet to sheets
        """
        if sheet_name not in self.sheets:
            sheet = self._excel_file.add_worksheet(sheet_name)
            self.sheets[sheet_name] = Sheet(self, sheet, need_idx, limit_max_width)
        return self.sheets[sheet_name]

    def get_sheet(self, sheet_name: str) -> Sheet:
        """
        get sheet by name
        """
        if sheet_name not in self.sheets:
            self.add_sheet(sheet_name)
        return self.sheets[sheet_name]

    def save(self) -> None:
        """
        save excel
        """
        for sheet in self.sheets.values():
            if not sheet.width:
                continue
            for idx, _ in enumerate(sheet.width):
                if sheet.attr.limit_max_width:
                    sheet.width[idx] = min(sheet.width[idx], MAX_WIDTH)
                sheet.width[idx] = max(sheet.width[idx], MIN_WIDTH)
                sheet.sheet.set_column(idx, idx, sheet.width[idx] + 1)
        try:
            self._excel_file.close()
        except (IOError, xlsxwriter.exceptions.FileCreateError) as exception:
            logger.error("Save excel failed, %s", exception)
