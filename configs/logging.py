# from https://towardsdatascience.com/basic-to-advanced-logging-with-python-in-10-minutes-631501339650
import os
import logging
from configs.common import logs_dir


class LevelOnlyFilter:
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


LOGGING_CONFIG = {
    "version": 1,
    "loggers": {
        "": {  # root logger
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stream_handler", "file_handler"],
        },
        "custom_logger": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stream_handler"],
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "ERROR",
            "filters": ["only_error"],
            "formatter": "default_formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": f"{os.path.join(logs_dir, 'ds-memo.log')}",
            "mode": "w",
            "level": "DEBUG",
            "formatter": "default_formatter",
        },
    },
    "filters": {
        "only_error": {
            "()": LevelOnlyFilter,
            "level": logging.ERROR,
        },
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s",
        },
    },
}

