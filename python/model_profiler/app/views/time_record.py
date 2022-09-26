from flask import Blueprint, request
from model_profiler.db.save_client import GetSaveClient
import configparser
import json

time_profile_blue = Blueprint('time_record', __name__, url_prefix='/time_record')

save_config = configparser.ConfigParser()
# todo using environment variable
save_config.read("/home/gh/TVMProfiler/python/model_profiler/config.ini")
save_type = (save_config["APPConfig"])["save_type"]
save_client = (GetSaveClient(save_type))(**(save_config[save_type]))


@time_profile_blue.route('/setSaveClient/', methods=['GET'])
def setSaveClient():
    clientType = request.args.get('clientType')
    saveClient = GetSaveClient(clientType)


@time_profile_blue.route('/allRecordIDs')
def allRecordIDs():
    return json.dumps(save_client.query_all_execution_ids())


@time_profile_blue.route('/getRecord/<recordID>')
def getRecord(recordID):
    print(recordID)
    model_record = save_client.query_by_execution_id(recordID)
    return str(model_record)

@time_profile_blue.route('/deleteRecord/<recordID>')
def deleteRecord():
    return "deleteRecord"
