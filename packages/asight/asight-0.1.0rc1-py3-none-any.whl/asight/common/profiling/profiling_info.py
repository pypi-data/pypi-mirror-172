"""
profiling info
"""
import json
import logging
import os

from config.config import Config
from util.common import get_file_from_directory

logger = logging.getLogger()


class ProfilingInfo:
    """
    profiling info
    """

    def __init__(self, path: str) -> None:
        self._path = path

    def parse_data(self) -> bool:
        """
        parse profiling data
        :return: true for success or false
        """
        file_list = get_file_from_directory(self._path, lambda x: x.startswith("info.json."))
        for info in file_list:
            if self._parse(info):
                return True
        return False

    def get_path(self) -> str:
        """
        get profiling info path
        :return: profiling info path
        """
        return self._path

    @staticmethod
    def _parse(info_file: str) -> bool:
        if info_file.endswith("done"):
            return False  # skip info.json.0.done
        try:
            with open(info_file, encoding="utf-8") as file:
                info = json.load(file)
        except (IOError, ValueError) as error:
            logger.error("Parse json info file %s failed : %s", info_file, error)
            return False
        if "DeviceInfo" not in info:
            logger.error("No device info in json info file %s", info_file)
            return False
        config = Config()
        for device_info in info["DeviceInfo"]:
            if "ai_core_num" in device_info:
                config.set_config("ai_core_num", device_info["ai_core_num"])
                return True
        logger.error("No ai_core_num in json info file %s", info_file)
        return False


class ProfilingModelInfo:
    """
    profiling model info
    """

    def __init__(self, iter_id: int, model_id: int, device_id: int, create_time: int) -> None:
        self._iter_id = iter_id
        self._model_id = model_id
        self._device_id = device_id
        self._create_time = create_time

    def __lt__(self, other) -> bool:
        if self._iter_id != other._iter_id:
            return self._iter_id < other._iter_id
        if self._model_id != other._model_id:
            return self._model_id < other._model_id
        if self._device_id != other._device_id:
            return self._device_id < other._device_id
        return self._create_time < other._create_time

    def get_model_id(self) -> int:
        """
        get model id
        :return: model id
        """
        return self._model_id

    def get_device_id(self) -> int:
        """
        get device id
        :return: device id
        """
        return self._device_id

    def get_iter_id(self) -> int:
        """
        get iter id
        :return: iter id
        """
        return self._iter_id


def get_model_info(file: str) -> ProfilingModelInfo:
    """
    get model info by filename
    :param file: file path
    :return: profiling model info
    """
    create_time = os.path.getctime(file)
    filename = os.path.splitext(file)[0]
    tmp = filename.split("_")
    try:
        device_id = int(tmp[-3])
    except ValueError:
        device_id = 0
    model_id = int(tmp[-2])
    iter_id = int(tmp[-1])
    return ProfilingModelInfo(iter_id, model_id, device_id, create_time)


def get_last_file_by_step(file_list: list) -> str:
    """
    get last file by step
    :param file_list: file list
    :return: last file in file list
    """
    last_file_model_info = ProfilingModelInfo(-1, -1, -1, 0)
    last_file_idx = 0
    for idx, file_name in enumerate(file_list):
        file = file_name
        model_info = get_model_info(file)
        if model_info > last_file_model_info:
            last_file_model_info = model_info
            last_file_idx = idx
    return file_list[last_file_idx]
