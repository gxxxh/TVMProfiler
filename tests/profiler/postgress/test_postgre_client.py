import time

from model_profiler.db.postgre_client import PostGreClient
import configparser
from model_profiler.internal import record
import psycopg2
import uuid


class TestPostGreClient():
    def test_get_columns(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        columns_info = pc.get_columns(pc.model_record_table)
        print(columns_info)
        assert len(columns_info) != 0

    def test_new_execute_id(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        nid, cur = pc.new_exeucte_id()
        assert nid != None
        assert cur != None

    def test_insert_model_record(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        nid, cur = pc.new_exeucte_id()
        model_record = record.ModelRecord(nid, cur, 0, "test0")
        res = pc.insert_model_record(model_record)
        assert res == True

    def test_insert_op_record(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        nid = "7b7407ec-3a4d-11ed-a1ba-f40270f2915a"
        op_record = record.OPRecord(**{
            "execution_id": nid,
            "node_id": 0,
            "node_start_time": time.time(),
            "node_name": "name0",
            "time_list": [1.1, 1.2],
            "avg_time": 1.15
        })
        res = pc.insert_op_record(op_record)
        assert res == True

    def test_insert_op_records(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        nid = "7b7407ec-3a4d-11ed-a1ba-f40270f2915a"
        op_record1 = record.OPRecord(**{
            "execution_id": nid,
            "node_id": 1,
            "node_start_time": psycopg2.TimestampFromTicks(time.time()),
            "node_name": "name0",
            "time_list": [1.1, 1.2],
            "avg_time": 1.15
        })
        op_record2 = record.OPRecord(**{
            "execution_id": nid,
            "node_id": 2,
            "node_start_time": psycopg2.TimestampFromTicks(time.time()),
            "node_name": "name0",
            "time_list": [1.1, 1.2],
            "avg_time": 1.15
        })
        res = pc.insert_op_records([op_record1, op_record2])
        assert res == True

    def test_query_by_execution_id(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        nid = "7b7407ec-3a4d-11ed-a1ba-f40270f2915a"
        res = pc.query_by_execution_id(nid)
        print(res)
        assert isinstance(res, record.ModelRecord)

    def test_query_all_execution_ids(self):
        config = configparser.ConfigParser()
        config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini", encoding="utf-8")
        postgre_config = config["PostGre"]
        pc = PostGreClient(**postgre_config)
        res = pc.query_all_execution_ids()
        print(res)
        assert  len(res)!=None