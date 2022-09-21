from model_profiler.db import postgre_executor
import uuid
import time


class PostGreSQLClient:
    """
    this class is used to provide crud api for actions
    """

    def __init__(self, database_name, user_name, password, host, port, table_name, table_schema="public"):
        self.executor = postgre_executor.PostGreExecutor(database_name, user_name, password, host, port)
        self.table_name = table_name
        self.table_schema = table_schema
        self.columns = self.GetColumns()

    def get_columns(self):
        sql = "select string_agg(column_name,',') " \
              "from information_schema.columns " \
              "where table_schema='{}' and table_name='{}'" \
            .format(self.table_schema, self.table_name)

        return self.executor.ExceQuery(sql)

    def new_exeucte_id(self):
        return uuid.uuid1(), time.time()

    def insert_op_record(self, op_record):
        """
        insert one record
        :param input_dict:
        :return:
        """
        sql = "INSERT INTO {}(execution_id, start_time, node_id, node_name, node_start_time, time_list, avg_time) \
        VALUES ('{}'::UUID, {}, {}, '{}', {}, array{}, {});" \
            .format(
            self.table_name,
            op_record.get("execution_id"),
            op_record.get("start_time"),
            op_record.get("node_id"),
            op_record.get("node_name"),
            op_record.get("node_start_time"),
            op_record.get("time_list"),
            op_record.get("avg_time")
        )
        return self.executor.ExecNonQuery(sql)

    def insert_model_record(self, **input_dict):
        num = input_dict["num"]
        sql = "INSERT INTO {}" \
              "(execution_id, start_time, node_id, node_name, node_start_time, time_list, avg_time) VALUES" \
            .format(self.table_name)
        for i in range(num):
            sql += " ('{}'::UUID, {}, {}, '{}', {}, array{}, {}),".format(
                input_dict["execution_id"][i],
                input_dict["start_time"][i],
                input_dict["node_id"][i],
                input_dict["node_name"][i],
                input_dict["node_start_time"][i],
                input_dict["time_list"][i],
                input_dict["avg_time"][i]
            )
        return self.executor.ExecNonQuery(sql)

    def query_by_execution_id(self, execution_id):
        """
        query by primary key(executor_id,
        :param execution_id: uuid
        :return:
        """
        sql = "SELECT * FROM {} WHERE execution_id='{}';".format(self.table_name, execution_id)
        return self.executor.ExceQuery(sql)

    def delete_by_execution_id(self, execution_id):
        """
        delete all record of one execution
        :param execution_id: uuid
        :return:
        """
        sql = "DELETE FROM {} WHERE execution_id='{}';".format(self.table_name, execution_id)
        return self.executor.ExecNonQuery(sql)
