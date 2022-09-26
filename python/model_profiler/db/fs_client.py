import os.path

from . import save_client


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
        with open(file_path, "r") as f:
            model_record_json = f.readlines()
            return model_record_json

    def delete_by_execution_id(self, execution_id):
        file_path = self.dump_path + "/" + execution_id + ".json"
        if os.path.exists(file_path):
            os.remove(file_path)
        return
