"""JSON file handler for RITA project."""

# Standard modules.
import asyncio
import logging
from json import load as json_load
from random import random
from traceback import format_exc
# Local modules.
from settings import JSONKeys, Paths


class BaseGraphHandler:
    """
    Graph handler abstract class.
    """
    async def graph_processing(self, graph: dict, *args):
        """
        Specifies how to process the graph.
        """
        raise NotImplementedError()


class BaseNodeHandler:
    """
    Node handler abstract class.
    """
    async def node_processing(self, node: dict, *args):
        """
        Specifies how to process the node.
        """
        raise NotImplementedError()


class BaseVarHandler:
    """
    Var handler abstract class.
    """
    async def var_processing(self, var: dict, *args):
        """
        Specifies how to process the var.
        """
        raise NotImplementedError()


class NodeHandler(BaseNodeHandler):
    """
    Node handler standard.
    """
    async def node_processing(self, node: dict, *args):
        """
        Specifies how to process the node.
        """
        await asyncio.sleep(random())
        result = await self.standard_node_processing(node, *args)
        return result

    async def standard_node_processing(self, node: dict, vars_uuid_for_check_ref: list) -> str:
        node_vars_in = [var_in for var_in in node[JSONKeys.DATA][JSONKeys.VARS][JSONKeys.INPUTS]]
        node_vars_out = [var_out for var_out in node[JSONKeys.DATA][JSONKeys.VARS][JSONKeys.OUTPUTS]]
        all_node_vars = node_vars_in + node_vars_out
        self.__check_node_ref(all_node_vars, vars_uuid_for_check_ref)

        node_vars_name = ', '.join([var[JSONKeys.NAME] for var in all_node_vars])
        result = f'{node[JSONKeys.DATA][JSONKeys.UUID]}, {node[JSONKeys.NAME]}, {node_vars_name}\n'

        return result

    def __check_node_ref(self, all_node_vars: list, vars_uuid_for_check_ref: list):
        """
        If there is an argument with the "ref" tag in the "inputs" or "outputs" of the node,
        then check that the graph variable (in the "vars" tag of the graph) has this uuid.
        If not, then throw an exception.
        """
        logging.info('Checking the "ref" tag...')

        node_ref = [el.get(JSONKeys.REF) for el in all_node_vars if el.get(JSONKeys.REF)]
        for ref in node_ref:
            if ref not in vars_uuid_for_check_ref:
                raise Exception(f'Reference [{ref}] not found in graph variables!')


        logging.info('The "ref" tag validation completed.')


class VarHandler(BaseVarHandler):
    """
    Var handler standard.
    """
    async def var_processing(self, var: dict, *args):
        """
        Specifies how to process the var.
        """
        await asyncio.sleep(random())
        result = await self.standard_var_processing(var)
        return result

    async def standard_var_processing(self, var: dict) -> str:
        result = f'{var[JSONKeys.UUID]}, {var[JSONKeys.NAME]}, {var[JSONKeys.DATA_TYPE]}\n'
        return result


class GraphHandler(BaseGraphHandler, NodeHandler, VarHandler):
    """
    Graph handler standard.
    """
    async def graph_processing(self, graph: dict, *args):
        """
        Specifies how to process the graph.
        """
        await asyncio.sleep(random())
        await self.standard_graph_processing(graph, *args)

    async def standard_graph_processing(self, graph: dict):
        logging.info(f'[{graph[JSONKeys.NAME]}] - Start asynchronous graph data processing...')

        graph_result = f'\nГраф: {graph[JSONKeys.NAME]}, {graph[JSONKeys.UUID]}\n'
        vars_result = 'Список переменных:\n'
        nodes_result = 'Список нод:\n'

        # Vars---------------------------------------------------------------------------------------------------------
        vars = [var for key in graph[JSONKeys.VARS] for var in graph[JSONKeys.VARS][key]]
        for var in vars:
            logging.info(f'[{graph[JSONKeys.NAME]}] | [{var[JSONKeys.NAME]}] - '
                         f'Start asynchronous var data processing...')

            vars_result += await self.var_processing(var)

            logging.info(f'[{graph[JSONKeys.NAME]}] | [{var[JSONKeys.NAME]}] - '
                         f'Asynchronous processing of var data completed.')
        # Nodes--------------------------------------------------------------------------------------------------------
        nodes = graph[JSONKeys.NODES]
        vars_uuid = [var[JSONKeys.UUID] for var in vars]
        for node in nodes.values():
            logging.info(f'[{graph[JSONKeys.NAME]}] | [{node[JSONKeys.NAME]}] - '
                         f'Start asynchronous node data processing...')

            nodes_result += await self.node_processing(node, vars_uuid)

            logging.info(f'[{graph[JSONKeys.NAME]}] | [{node[JSONKeys.NAME]}] - '
                         f'Asynchronous processing of node data completed.')

        logging.info('РЕЗУЛЬТАТ:\n' + graph_result + vars_result + nodes_result)
        logging.info(f'[{graph[JSONKeys.NAME]}] - Asynchronous processing of graph data completed.')


class MainJSONHandler(GraphHandler):
    def __init__(self):
        self.graphs = MainJSONHandler.get_json_data_from_local_file()[JSONKeys.ROBOT_GRAPHS]

    def start_json_processing(self):
        logging.info('Start asynchronous JSON data processing...')

        loop = asyncio.get_event_loop()

        tasks = []
        for graph in self.graphs:
            tasks += [loop.create_task(self.graph_processing(graph))]

        wait_tasks = asyncio.gather(*tasks)
        try:
            loop.run_until_complete(wait_tasks)
            loop.close()
        except Exception:
            logging.warning(f'Data was not processed successfully!\n{format_exc()}')

        logging.info('Asynchronous processing of JSON data completed.')

    @staticmethod
    def get_json_data_from_local_file() -> dict:
        """
        Get JSON data from a file located in the root directory.

        :return: data dictionary from JSON file.
        """
        file_path = Paths.JSON_FILE_PATH
        json_data = {}

        logging.info(f'Get JSON data from file [{file_path}]...')
        with open(file_path, 'r', encoding='utf-8') as json_file:
            json_data = json_load(json_file)
        logging.info(f'JSON data from file [{file_path}] received.')

        return json_data
