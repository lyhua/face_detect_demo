import os
import sys
# import random
# import math
import numpy as np
import skimage.io
# import matplotlib
# import matplotlib.pyplot as plt
import cv2
import time
# from tkinter import messagebox
import demo


# from PIL import Image

from PIL import Image

# 项目的根目录
ROOT_DIR = os.path.abspath("../../")

# 为了方便加载
sys.path.append(ROOT_DIR)
# from mrcnn.config import Config
from mrcnn import model as modellib, utils, visualize

from samples.face.face import FaceConfig
# from samples.face.displayface import display_face
from samples.face.displayface import display_face1
# import video
from mypy import video

# 获取当前目录
ROOT_DIR = os.getcwd()

# TODO 这个参数没有什么用(但是必须存在)
MODEL_DIR = os.path.join(ROOT_DIR, "log")

# 模型的绝对路径
# TODO 这里必须一定要改成相对目录
MODEL_WEIGHT_PATH = "./modeldata/mask_rcnn_face_0040.h5"

# from PyInstaller.utils.hooks import collect_data_files, collect_submodules
#
# datas = collect_data_files("skimage.io._plugins")
# hiddenimports = collect_submodules('skimage.io._plugins')

# 预测类配置
# TODO 感觉这里不需要
class InferFaceConfig(FaceConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def face_detect(image_path, image_save_path, image_filename):
    """
    对人脸图片进行检测并且保存人脸图像(这里是单张图片处理)
    :param image_path: 需要检测人脸图像位置
    :param image_save_path: 检测后的人脸图像保存位置
    :param image_filename: 保存的人脸图像文件名字
    :return:
    """
    # 如果模型不存提示并且退出程序
    if not os.path.exists(MODEL_WEIGHT_PATH):
        print("MODEL_WEIGHT_PATH: ", MODEL_WEIGHT_PATH)
        print("no exists ", MODEL_WEIGHT_PATH.split("\\")[-1])
        # 返回出错
        # 程序外壳提示没有训练模型
        return -1

    # 类别(这里写死，因为数据集就是这样命名)
    class_names = ["BG", "fake", "real"]

    # 创建预测类配置
    config = InferFaceConfig()

    # 创建网络
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # 加载权重
    model.load_weights(MODEL_WEIGHT_PATH, by_name=True)

    # 判断图片是否存在，不存在提示并退出程序
    if not os.path.exists(image_path):
        print("no image file")
        # TODO 提示检测图片不存在
        return -2

    # 开始预测
    # 加载图片
    image = skimage.io.imread(image_path)
    # image = cv2.imread(image_path)

    size = image.size
    # 进行预测
    result = model.detect([image], verbose=1)
    r = result[0]

    # 对图片进行mask
    # 下面的颜色可以进行改变
    color1 = (1.0, 0.0, 0.0)
    color2 = (0.0, 1.0, 0.0)
    color3 = (0.0, 0.0, 1.0)
    colors = np.array([color1, color2, color3])
    image = display_face1(image, r['rois'], r['masks'], r['class_ids'], class_names, scores=r['scores'], colors=colors)

    # 进行图片保存
    if os.path.exists(image_save_path) is False:
        os.mkdir(image_save_path)
    real_image_save_path = os.path.join(image_save_path, image_filename)
    image = Image.fromarray(image)
    image.save(real_image_save_path)


def detect_more_face(images_path, images_save_path):
    """
    进行多张图片人脸图片检测处理
    :param images_path: 需要处理的人脸图片的目录绝对位置
    :param images_save_path: 保存处理后的人脸图片目录的绝对位置
    :return:
    """
    # 判断文件夹是否存在
    if os.path.exists(images_path) is False:
        # TODO 外壳程序需要提示需要判断文件夹不存在
        return -1

    # 判断保存的文件夹
    if os.path.exists(images_save_path) is False:
        # 不存在创建
        os.mkdir(images_save_path)

    # 打开已经处理好的人脸图片
    filelist = os.listdir(images_path)
    # !!!如果人脸图片命名方式改变，这个程序应该废了
    filelists = sorted(filelist, key=lambda x: int(x.split(".")[0]))

    # 类别(这里写死，因为数据集就是这样命名)
    class_names = ["BG", "fake", "real"]

    # 创建预测类配置
    config = InferFaceConfig()

    # 创建网络
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # 加载权重
    model.load_weights(MODEL_WEIGHT_PATH, by_name=True)

    # 下面的颜色可以进行改变
    color1 = (1.0, 0.0, 0.0)
    color2 = (0.0, 1.0, 0.0)
    color3 = (0.0, 0.0, 1.0)

    for item in filelists:
        image_real_path = os.path.join(images_path, item)

        image = skimage.io.imread(image_real_path)

        # 进行预测
        result = model.detect([image], verbose=1)
        r = result[0]

        # 对图片进行mask
        colors = np.array([color1, color2, color3])
        image = display_face1(image, r['rois'], r['masks'], r['class_ids'], class_names, scores=r['scores'],
                              colors=colors)

        # 进行图片保存
        real_image_save_path = os.path.join(images_save_path, item)
        image = Image.fromarray(image)
        image.save(real_image_save_path)


def detect_face_thread(images_path, images_save_path, image_nums, video_save_path, video_name):
    """
    这个检测专门用于线程
    :param images_path: 需要检测视频的图片
    :param images_save_path: 保存检测图片的位置
    :param image_nums: 一共需要检测的图片数量
    :param video_save_path: 保存的合成视频的路径
    :param video_name: 保存的视频的名字
    :return:
    """
    # 循环判断要检测的文件夹是否存在
    # TODO 这里可以进行优化， 可以有消息进行优化
    while True:
        if os.path.exists(images_path):
            break
        time.sleep(1)

    # 判断保存的文件夹
    if os.path.exists(images_save_path) is False:
        # 不存在创建
        os.mkdir(images_save_path)

    # 类别(这里写死，因为数据集就是这样命名)
    class_names = ["BG", "fake", "real"]

    # 创建预测类配置
    config = InferFaceConfig()

    # 创建网络
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # 加载权重
    # 判断是否加载权重
    if demo.is_load_weights:
        model.load_weights(MODEL_WEIGHT_PATH, by_name=True)
        demo.is_load_weights = False

    # 下面的颜色可以进行改变
    color1 = (1.0, 0.0, 0.0)
    color2 = (0.0, 1.0, 0.0)
    color3 = (0.0, 0.0, 1.0)

    # 用来记录处理的图片的数量，用来判断退出程序
    num = 0
    print(image_nums)
    while num < image_nums:
        # 获取锁
        if demo.semaphore.acquire():
            print("face_detect")
            # TODO 这里也可以进行优化
            # 打开已经处理好的人脸图片
            filelist = os.listdir(images_path)
            # !!!如果人脸图片命名方式改变，这个程序应该废了
            filelists = sorted(filelist, key=lambda x: int(x.split(".")[0]))

            # 进行检测
            item = filelists[num]
            print("item ", item)
            image_real_path = os.path.join(images_path, item)

            image = skimage.io.imread(image_real_path)

            # 进行预测
            result = model.detect([image], verbose=1)
            r = result[0]

            # 对图片进行mask
            colors = np.array([color1, color2, color3])
            image = display_face1(image, r['rois'], r['masks'], r['class_ids'], class_names, scores=r['scores'],
                                  colors=colors)

            # 进行图片保存
            real_image_save_path = os.path.join(images_save_path, item)
            image = Image.fromarray(image)
            image.save(real_image_save_path)

            # 进行下一张图片检测
            num = num + 1
            # 释放锁
            demo.semaphore.release()
        # time.sleep(1)

    # 合成视频
    video.synthetic_video(images_save_path, 12, video_save_path, video_name, "png")
    print("视频检测结束")

    # 退出子线程
    sys.exit(0)









if __name__ == "__main__":
    # 测试单张图片检测
    # # 这里添加需要预测的图片
    # # TODO 弄成一个参数
    # image_path = "C:\\Users\\12455\Desktop\\test1\\fake_1.png"
    # # 相对路径
    # image_save_path = ".\\faceimage"
    # filename = "fake_1.png"
    # face_detect(image_path, image_save_path, filename)


    # 测试多张图片检测
    images_path = "./facevedio"
    images_save_path = "./faceimage"
    detect_more_face(images_path, images_save_path)




