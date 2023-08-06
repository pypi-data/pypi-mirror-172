import logging
import logging.handlers
from pathlib import Path

from addok.config import config


notfound_logger = None
query_logger = None
slow_query_logger = None


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    filename = Path(config.LOG_DIR).joinpath("{}.log".format(name))
    try:
        handler = logging.handlers.TimedRotatingFileHandler(
            str(filename), when="midnight"
        )
    except FileNotFoundError:
        print("Unable to write to {}".format(filename))
    else:
        logger.addHandler(handler)
    return logger


@config.on_load
def on_load():
    if config.LOG_NOT_FOUND:
        global notfound_logger
        notfound_logger = get_logger("notfound")

    if config.LOG_QUERIES:
        global query_logger
        query_logger = get_logger("queries")

    if config.SLOW_QUERIES:
        global slow_query_logger
        slow_query_logger = get_logger("slow_queries")


def log_notfound(query):
    if config.LOG_NOT_FOUND:
        notfound_logger.debug(query)


def log_query(query, results):
    if config.LOG_QUERIES:
        if results:
            result = str(results[0])
            score = str(round(results[0].score, 2))
        else:
            result = "-"
            score = "-"
        query_logger.debug("\t".join([query, result, score]))


def log_slow_query(query, results, timer):
    if config.SLOW_QUERIES:
        if results:
            result = str(results[0])
            score = str(round(results[0].score, 2))
            id_ = results[0].id
        else:
            result = "-"
            score = "-"
            id_ = "-"
        slow_query_logger.debug("\t".join([str(timer), query, id_, result, score]))
