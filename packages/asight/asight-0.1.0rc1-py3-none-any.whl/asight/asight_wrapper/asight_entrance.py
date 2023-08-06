"""
Main module.
"""

import argparse
import os
import sys
from typing import Tuple

from datasets.dataset import Dataset
from util import log
from util.common import load_module

# pylint:disable=too-few-public-methods


class AsightEntrance:
    """
    Asight entrance
    """

    def __init__(self) -> None:
        self._datasets = None
        self._logger = log.init_logger()

    def _analyze(self, parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
        if not any(vars(args).values()):
            parser.print_help()
            return
        data = self._parse_data(args)
        if not data:
            self._logger.error("No data to by analyzed")
            return
        for key, value in data.items():
            self._logger.info("%s : %s", key, value.get_data_path())
        self._logger.info("Analyze start.")
        results = self._optimize(data)
        self._logger.info("Analyze end.")
        self._show_result(results)

    def _parse_data(self, args: argparse.Namespace) -> dict:
        data: dict[str, Dataset] = {}
        if not self._datasets:
            return data
        for key, dataset in self._datasets.items():
            if not hasattr(args, key):
                continue
            arg = getattr(args, key)
            if arg is None:
                continue
            arg = os.path.abspath(arg)
            if not os.path.exists(arg):
                self._logger.error("Directory %s is not exist", arg)
                return None
            dataset(arg, data, self._datasets)
        return data

    @staticmethod
    def _optimize(data: dict) -> list:
        optimizers = load_module("optimizer")
        results = []
        for optimizer in optimizers.values():
            result = optimizer.optimize(data)
            if result is None:
                continue
            if result not in results:
                results.append(result)
        return results

    @staticmethod
    def _show_result(results: list) -> None:
        if not results:
            return
        for result in results:
            result.show()

    def _init_arg_parser(self) -> Tuple[argparse.ArgumentParser, dict]:
        command_handler = {}
        parser = argparse.ArgumentParser(prog='asight', description="Ascend Sight")
        subparsers = parser.add_subparsers()
        analyze_parser = subparsers.add_parser("analyze", help="Analyze data and make optimization recommendations")
        self._init_analyze_parser(analyze_parser)
        command_handler["analyze"] = {"parser": analyze_parser, "handler": self._analyze}
        return parser, command_handler

    def _init_analyze_parser(self, parser: argparse.ArgumentParser) -> None:
        self._datasets = load_module("datasets", parser)

    def main(self):
        """
        main function of asight entrance
        :return: None
        """
        parser, command_handler = self._init_arg_parser()
        if len(sys.argv) < 2:
            parser.print_help()
            return
        args = parser.parse_args(sys.argv[1:])
        handler = command_handler.get(sys.argv[1])
        if not handler:
            parser.print_help()
            return
        handler.get("handler")(handler.get("parser"), args)
