"""JSON file processing test task. The main module."""

# Standard modules.
import logging
from time import perf_counter
# Local modules.
from json_handler import MainJSONHandler
from log import LogSets


if __name__ == '__main__':
    # Time counter.
    perf_counter()
    # Log initialization.
    LogSets.set_2()
    # Start main JSON file processing.
    MainJSONHandler().start_json_processing()

    logging.info(f'ЗАТРАЧЕННОЕ ВРЕМЯ: [{perf_counter()}] сек.')