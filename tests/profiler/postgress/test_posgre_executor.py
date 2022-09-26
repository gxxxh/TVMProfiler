import pytest
import time
from model_profiler.db.postgre_executor import PostGreExecutor
import configparser
import psycopg2
import uuid


class TestPostGreExecutor:
    def testConnect(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["postgresql"]
        pc = PostGreExecutor(postgre_config["database_name"], postgre_config["user_name"],
                             postgre_config["password"], postgre_config["host"], postgre_config["port"])
        pc.GetConnectionInfo()
        assert pc._conn != None

    def testExecQuery(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["postgresql"]
        pc = PostGreExecutor(postgre_config["database_name"], postgre_config["user_name"],
                             postgre_config["password"], postgre_config["host"], postgre_config["port"])
        sql = "SELECT * FROM {}".format(postgre_config["model_record_table"])
        res = pc.ExceQuery(sql)
        print(res)
        assert len(res) != 0

    def testExecNonQuery(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["postgresql"]
        pc = PostGreExecutor(postgre_config["database_name"], postgre_config["user_name"],
                             postgre_config["password"], postgre_config["host"], postgre_config["port"])
        cur = psycopg2.TimestampFromTicks(time.time())
        execution_id = uuid.uuid1()
        # insert
        sql = "INSERT INTO {}(execution_id,start_time, num_ops, model_name) \
                VALUES ('{}'::UUID,{},{},'{}')".format( \
            postgre_config["model_record_table"], execution_id, cur, 0, "test_model_name")
        res = pc.ExecNonQuery(sql)
        assert res == True

        # # update
        # sql = ""
        # res = pc.ExecNonQuery(sql)
        # assert res == True
        #
        # delete

        # sql = "DELETE FROM op_run_time WHERE execution_id=1 "
        # res = pc.ExecNonQuery(sql)
        # assert res == True
