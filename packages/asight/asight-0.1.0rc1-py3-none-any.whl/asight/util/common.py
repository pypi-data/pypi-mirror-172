"""
common functions
"""
import os
from typing import Any

from config.config import Config


def load_module(module_dir: str, *args: Any) -> dict:
    """
    load module from module_dir
    """
    module_list: dict[str, Any] = {}
    root_path = Config().get_root_path()
    for filename in os.listdir(os.path.join(root_path, module_dir)):
        if not filename.endswith(".py") or filename.startswith("_"):
            continue
        module_name = os.path.splitext(filename)[0]
        module = __import__(module_dir.replace('/', '.') + "." + module_name, fromlist=[module_name])
        module.register(module_list, *args)
    return module_list


def create_directory_for_file(file: str) -> None:
    """
    create directory for file
    """
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def get_file_from_directory(path: str, check_func: Any) -> list:
    """
    get file from directory
    """
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            if check_func(file):
                file_list.append(filename)
    return file_list


def format_excel_title(title: str) -> str:
    """
    format excel title
    """
    title = title.lower()
    title = title.replace("(us)", '')
    title = title.replace("(%)", '')
    title = title.replace(" ", "_")
    return title


def to_percent(num: float) -> str:
    """
    change float to percent format
    """
    num = num * 100
    return f"{num:.2f}%"
