import os.path
import json
from . import save_client
from model_profiler.internal import record


class FSClient(save_client.SaveClient):
    """
    this class is using to save time record to local file system
    """

    def __init__(self, dump_path):
        self.op_record_table_columns = []
        self.model_record_table_columns = []
        self.dump_path = dump_path

    def insert_model_record(self, model_record):
        file_path = self.dump_path + "/" + str(model_record.execution_id) + ".json"
        with open(file_path, "w") as f:
            f.write(str(model_record))

    def query_by_execution_id(self, execution_id):
        file_path = self.dump_path + "/" + execution_id + ".json"
        if not os.path.exists(file_path):
            return ""
        with open(file_path, "r") as f:
            model_record_dict = json.load(f)
            model_record = record.ModelRecord(**model_record_dict)
            return model_record

    def delete_by_execution_id(self, execution_id):
        file_path = self.dump_path + "/" + execution_id + ".json"
        if os.path.exists(file_path):
            os.remove(file_path)
        return

    def query_all_execution_ids(self):
        if not os.path.exists(self.dump_path):
            return "Error, log path not exist!!!"
        file_names = os.listdir(self.dump_path)
        return [file_name for file_name in file_names if file_name.find(".json") != -1]
