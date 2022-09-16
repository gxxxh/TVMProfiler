basePath = "/home/gh/TVMProfiler"
configSpacePath = basePath+"data/ConfigSpace/"

def WriteConfigSpace(tasks, model_name, target):
    fName = configSpacePath + model_name + "-" + target + ".json"
    f = open(fName, "w")
    for i, task in enumerate(tasks):
        # print(task)
        f.write(task.config_space.__str__())
        # print(task.config_space)
    f.close()
    return

def getYoloData():
    from yolort.utils import get_image_from_url
    import numpy as np
    import cv2

    in_size = 640
    img_source = "https://huggingface.co/spaces/zhiqwang/assets/resolve/main/bus.jpg"
    # img_source = "https://huggingface.co/spaces/zhiqwang/assets/resolve/main/zidane.jpg"
    img = get_image_from_url(img_source)

    img = img.astype("float32")
    img = cv2.resize(img, (in_size, in_size))

    img = np.transpose(img / 255.0, [2, 0, 1])
    img = np.expand_dims(img, axis=0)
    return img