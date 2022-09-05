from model import models
import numpy as np
import tvm
from model.runner.model_runner import ModelRunner


class TransformerModelRunner(ModelRunner):
    def __init__(self, args):
        super(TransformerModelRunner, self).__init__(args)
        self.input_name = "input_ids"

    def loadModel(self):
        self.mod, self.params, self.input_shape, _ = \
            models.transformers_nns.get_network(self.model_name, self.batch_size, dtype="float32", sequence=128)

    def loadInputData(self):
        return tvm.nd.array((np.random.uniform(size=self.input_shape)).astype("int64"))

    def getLibModuleDev(self, config={}):
        return super(TransformerModelRunner, self).getLibModuleDev(config={"relay.backend.use_auto_scheduler": False})

    def getRunTimeModule(self):
        return super(TransformerModelRunner, self).getRunTimeModule()

    def runOnTVM(self):
        return super(TransformerModelRunner, self).runOnTVM()

    def tuneOnTVM(self):
        return super(TransformerModelRunner, self).tuneOnTVM()


class BertRunner(TransformerModelRunner):
    def __init__(self, args):
        self.model_name = "bert"
        super(BertRunner, self).__init__(args)
        super(BertRunner, self).loadModel()
