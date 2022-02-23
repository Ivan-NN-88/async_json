"""Settings module."""

# Standard modules.
import os


class JSONKeys:
    DATA = 'data'
    DATA_TYPE = 'data_type'
    INPUTS = 'inputs'
    NAME = 'name'
    NODES = 'nodes'
    OUTPUTS = 'outputs'
    REF = 'ref'
    ROBOT_GRAPHS = 'robot_graphs'
    UUID = 'uuid'
    VARS = 'vars'


class Paths:
    ROOT_DIRECTORY = os.getcwd()
    JSON_FILE_PATH = fr'{ROOT_DIRECTORY}\inc\sample.json'
    LOG_PATH = fr'{ROOT_DIRECTORY}\logs'
    LOG_FILE_PATH = fr'{LOG_PATH}\log.log'
    LAST_LOG_FILE_PATH = fr'{LOG_PATH}\last_log.log'
