class SaveClient:
    def __init__(self):
        self.name = "base save client"


def GetSaveClient(client_type):
    """
    :param client_type: PostGre, FS
    :return:
    """
    from importlib import import_module
    class_str: str = 'model_profiler.db.{}_client.{}Client'.format(str.lower(client_type), client_type)
    try:
        module_path, class_name = class_str.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(class_str)
