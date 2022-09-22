import psycopg2, time
from model_profiler.internal import record

class TestRecord():
    def testOPRecord2Json(self):
        nid = "a8e32342-3986-11ed-a1ba-f40270f2915a"
        op_record1 = record.OPRecord(**{
            "execution_id": nid,
            "node_id": 1,
            "node_start_time": time.time(),
            "node_name": "name0",
            "time_list": [1.1, 1.2],
            "avg_time": 1.15
        })

        js = op_record1.__str__()
        assert isinstance(js, str)

    def testModelRecord2Json(self):
        nid = "a8e32342-3986-11ed-a1ba-f40270f2915a"
        op_record1 = record.OPRecord(**{
            "execution_id": nid,
            "node_id": 1,
            "node_start_time": time.time(),
            "node_name": "name0",
            "time_list": [1.1, 1.2],
            "avg_time": 1.15
        })
        op_record2 = record.OPRecord(**{
            "execution_id": nid,
            "node_id": 2,
            "node_start_time": time.time(),
            "node_name": "name0",
            "time_list": [1.1, 1.2],
            "avg_time": 1.15
        })
        model_record = record.ModelRecord(**{
            "execution_id": nid,
            "start_time": time.time(),
            "num_ops": 2,
            "model_name": "test",
        })
        model_record.op_records = [op_record1, op_record2]
        js = model_record.__str__()
        print(js)
        assert isinstance(js, str)