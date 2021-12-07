import os
import importlib

from day import Day


def get_days():
    days = []
    files = [
        file for file in os.listdir(os.path.dirname(__file__))
        if file.endswith('py') and file != '__init__.py'
    ]

    for file in files:
        mod_name = file[:-3]
        importlib.import_module(f'days.{mod_name}')

    return Day.__subclasses__()
