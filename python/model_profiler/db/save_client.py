from abc import abstractmethod
import time, uuid


class SaveClient:
    def __init__(self):
        print("this is base class for save log")

    @staticmethod
    def new_execute_id():
        return str(uuid.uuid1()), time.time()

    @abstractmethod
    def insert_model_record(self, model_record):
        raise NotImplementedError

    # @abstractmethod
    # def insert_op_record(self, op_record):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def insert_op_records(self, op_records):
    #     raise NotImplementedError

    @abstractmethod
    def query_by_execution_id(self, execution_id):
        raise NotImplementedError

    @abstractmethod
    def delete_by_execution_id(self, execution_id):
        raise NotImplementedError

    @abstractmethod
    def query_all_execution_ids(self):
        raise NotImplementedError


def GetSaveClient(client_type):
    """
    :param client_type: PostGre, FS
    :return:
    """
    from importlib import import_module
    class_str: str = 'model_profiler.db.{}_client.{}Client'.format(str.lower(client_type), client_type)
    try:
        module_path, class_name = class_str.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(class_str)
