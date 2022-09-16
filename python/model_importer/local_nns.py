import os

from tvm import relay
import tvm.relay.testing

from yolort.models import yolov5n
from yolort.relay import get_trace_module

os.environ['TVM_BACKTRACE'] = "1"




def get_network(name, batch_size=1, layout="NCHW", dtype="float32", sequence=128, hidden_size=768, num_hidden_layers=12,
                num_attention_heads=12, intermediate_size=3072, max_position_embeddings=512):
    """Get the symbol definition and random weight of a network"""

    # auto-scheduler prefers NHWC layout
    if layout == "NHWC":
        image_shape = (224, 224, 3)
    elif layout == "NCHW":
        image_shape = (3, 224, 224)
    else:
        raise ValueError("Invalid layout: " + layout)

    input_shape = (batch_size,) + image_shape
    output_shape = (batch_size, 1000)
    if name.startswith("resnet-"):
        n_layer = int(name.split("-")[1])
        mod, params = relay.testing.resnet.get_workload(
            num_layers=n_layer,
            batch_size=batch_size,
            layout=layout,
            dtype=dtype,
            image_shape=image_shape,
        )
    elif name.startswith("resnet3d-"):
        n_layer = int(name.split("-")[1])
        mod, params = relay.testing.resnet.get_workload(
            num_layers=n_layer,
            batch_size=batch_size,
            layout=layout,
            dtype=dtype,
            image_shape=image_shape,
        )
    elif name == "mobilenet":
        mod, params = relay.testing.mobilenet.get_workload(
            batch_size=batch_size, layout=layout, dtype=dtype, image_shape=image_shape
        )
    elif name == "squeezenet_v1.1":
        assert layout == "NCHW", "squeezenet_v1.1 only supports NCHW layout"
        mod, params = relay.testing.squeezenet.get_workload(
            version="1.1",
            batch_size=batch_size,
            dtype=dtype,
            image_shape=image_shape,
        )
    elif name == "inception_v3":
        input_shape = (batch_size, 3, 299, 299) if layout == "NCHW" else (batch_size, 299, 299, 3)
        mod, params = relay.testing.inception_v3.get_workload(batch_size=batch_size, dtype=dtype)
    elif name == "yolov5n":
        in_size = 640
        input_shape = (in_size, in_size)
        model_func = yolov5n(pretrained=True, size=(in_size, in_size))
        script_module = get_trace_module(model_func, input_shape=input_shape)
        input_name = "input0"
        shape_list = [(input_name, (1, 3, *input_shape))]
        mod, params = relay.frontend.from_pytorch(script_module, shape_list)
        output_shape = ""
    return mod, params, input_shape, output_shape