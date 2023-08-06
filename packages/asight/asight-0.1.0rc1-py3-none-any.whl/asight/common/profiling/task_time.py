"""
task time
"""
import json
import logging
from typing import List

from common.profiling.profiling_info import get_last_file_by_step
from util.common import get_file_from_directory

logger = logging.getLogger()

AICPU_TASK_TYPE = "AI_CPU"
AICORE_TASK_TYPE = "AI_CORE"


class Task:
    """
    task info
    """

    def __init__(self, content: dict) -> None:
        self._parse_json(content)

    def _parse_json(self, content):
        self._name = content.get("name", "")
        self._pid = content.get("pid", 0)
        self._starttime = content.get("ts", 0)
        self._dur = content.get("dur", 0)
        args = content.get("args", None)
        if args:
            self._task_type = args.get("Task Type")
            self._stream_id = args.get("Stream Id")
            self._task_id = args.get("Task Id")
        else:
            self._task_type = "NA"
            self._stream_id = "NA"
            self._task_id = "NA"

    def get_pid(self):
        """
        get pid
        :return: pid
        """
        return self._pid

    def get_task_type(self):
        """
        get pid
        :return: pid
        """
        return self._task_type

    def get_starttime(self):
        """
        get starttime
        :return: starttime
        """
        return self._starttime

    def get_dur(self):
        """
        get duration
        :return: duration
        """
        return self._dur

    def get_name(self):
        """
        get task name
        :return: task name
        """
        return self._name


class TaskTime:
    """
    task time info
    """

    def __init__(self, path: str) -> None:
        self._path = path
        self._tasks: List[Task] = []
        self._aicore_tasks: List[Task] = []
        self._aicpu_tasks: List[Task] = []
        self._process_map: dict[str, str] = {}
        self._pid_map: dict[str, str] = {}

    def get_aicpu_tasks(self):
        """
        get aicpu tasks
        :return: aicpu tasks
        """
        return self._aicpu_tasks

    def get_aicore_tasks(self):
        """
        get aicore tasks
        :return: aicore tasks
        """
        return self._aicore_tasks

    def parse_data(self) -> bool:
        """
        pase task time file
        :return: true or false
        """
        file_list = get_file_from_directory(self._path, lambda x: (x.startswith("task_time_")) and x.endswith(".json"))
        if not file_list:
            logger.warning("Cannot find task_time*.json under %s", self._path)
            return False
        file = get_last_file_by_step(file_list)
        if len(file_list) > 1:
            logger.info("Multiple copies of task time data were found, use %s", file)
        return self._parse(file)

    def _parse(self, file_path: str):
        logger.debug("Parse file %s", file_path)
        try:
            with open(file_path, encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError) as error:
            logger.error("Parse task time file %s failed : %s", file_path, error)
            return False
        for item in data:
            if item.get("ph") != "M":  # header
                continue
            if item.get("name") != "process_name":
                continue
            pid = item.get("pid")
            pname = item["args"]["name"]
            self._process_map[pid] = pname
            self._pid_map[pname] = pid
        for item in data:
            if item.get("ph") == "M":  # header
                continue
            task = Task(item)
            self._tasks.append(task)
            if task.get_pid() != self._pid_map.get("Task Scheduler"):
                continue
            if task.get_task_type() == AICORE_TASK_TYPE:
                self._aicore_tasks.append(task)
            elif task.get_task_type() == AICPU_TASK_TYPE:
                self._aicpu_tasks.append(task)
        self._aicore_tasks.sort(key=lambda x: x.get_starttime())
        self._aicpu_tasks.sort(key=lambda x: x.get_starttime())
        if not self._tasks:
            logger.error("No valid task info in %s", file_path)
            return False
        return True
