import datetime
import json
import time


class RecordBase():
    def toJSON(self):
        # return json.dumps(self, default=lambda o: o.__dict__,
        #                   sort_keys=True, indent=4, ensure_ascii=False)
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4, ensure_ascii=False)

    def __str__(self):
        return self.toJSON()

    def __repr__(self):
        return self.__str__()

    def get(self, key):
        return self.__getitem__(key)

    def __getitem__(self, item):
        return self.__dict__[item]


class OPRecord(RecordBase):
    """
    this class is used to describe a operator's executing record
    node_start_time: timestamp;
    """

    def __init__(self, execution_id, node_id, node_start_time, node_name, time_list, avg_time):
        """
        node_start_time need to be timestamp
        :param execution_id:
        :param node_id:
        :param node_start_time:
        :param node_name:
        :param time_list:
        :param avg_time:
        """
        if (isinstance(node_start_time, datetime.datetime)):
            node_start_time = time.mktime(node_start_time.timetuple()) + node_start_time.microsecond / 1000000.0
        self.execution_id = execution_id
        self.node_id = node_id
        self.node_start_time = node_start_time
        self.node_name = node_name
        self.time_list = [float(t) for t in time_list]
        self.avg_time = float(avg_time)


class ModelRecord(RecordBase):
    """
    this class is using to describe a model's inference record
    """

    def __init__(self, execution_id, start_time, num_ops, model_name, op_records=[]):
        """
        start_time need to be timestamp
        :param execution_id: generate by uuid, need to be type str
        :param start_time:
        :param num_ops:
        :param model_name:
        """
        if (isinstance(start_time, datetime.datetime)):
            start_time = time.mktime(start_time.timetuple()) + start_time.microsecond / 1000000.0
        self.execution_id = execution_id
        self.start_time = start_time
        self.num_ops = num_ops
        self.model_name = model_name
        self.op_records = op_records

    def add_op_record(self, op_record):
        self.op_records.append(op_record)
        self.num_ops = len(self.op_records)
