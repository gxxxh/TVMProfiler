from model_profiler.db.save_client import GetSaveClient
from model_profiler.db.postgre_client import PostGreClient


class TestSaveClient:
    def test_get_save_client(self):
        """
        test using reflection to get the save client class
        :return:
        """
        postgre_client = GetSaveClient("PostGre")
        assert PostGreClient.__name__==postgre_client.__name__
