"""The CLI entry of asight."""
import importlib
import os
import sys


def main():
    """Entrance of asight."""
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    model_path = "asight_wrapper.asight_entrance"
    module_class = "AsightEntrance"
    asight_entrace_module = importlib.import_module(model_path)
    if hasattr(asight_entrace_module, module_class):
        getattr(asight_entrace_module, module_class)().main()


def init():
    """For unit  test only."""
    if __name__ == '__main__':
        main()


init()
