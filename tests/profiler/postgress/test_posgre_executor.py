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
        pc = PostGreExecutor(postgre_config["dbname"], postgre_config["username"],
                             postgre_config["password"], postgre_config["host"], postgre_config["port"])
        pc.GetConnectionInfo()
        assert pc._conn != None

    def testExecQuery(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["postgresql"]
        pc = PostGreExecutor(postgre_config["dbname"], postgre_config["username"], postgre_config["password"],
                             postgre_config["host"], postgre_config["port"])
        uid = "5f009d0a-3958-11ed-a1ba-f40270f2915a"
        sql = "SELECT * FROM op_run_time WHERE execution_id='{}'".format(uid)
        res = pc.ExceQuery(sql)
        print(res)
        assert len(res) != 0

    def testExecNonQuery(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["postgresql"]
        pc = PostGreExecutor(postgre_config["dbname"], postgre_config["username"], postgre_config["password"],
                             postgre_config["host"], postgre_config["port"])
        cur = psycopg2.TimestampFromTicks(time.time())
        execution_id = uuid.uuid1()
        # insert
        sql = "INSERT INTO op_run_time(execution_id,start_time, node_id,node_name, node_start_time, time_list, avg_time) \
                VALUES ('{}'::UUID,{},{},'{}',{},array{},{})".format( \
            execution_id, cur, 0, "test_node_name", cur, [1.1, 1.2], 1.05)
        res = pc.ExecNonQuery(sql)
        assert res == True
        sql = "INSERT INTO op_run_time(execution_id,start_time, node_id,node_name, node_start_time, time_list, avg_time) \
                VALUES ('{}'::UUID,{},{},'{}',{},array{},{})".format( \
            execution_id, cur, 1, "node_name1", cur, [1.1, 1.2], 1.05)
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
