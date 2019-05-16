import os
import cv2
import numpy as np
import datetime
import skimage.io


def synthetic_video(images_path, fps, vedio_save_path, vedio_filename, format):
    """
    进行视频合成
    :param images_path: 处理后的人脸图片
    :param fps: 每秒钟播放的帧数
    :param vedio_save_path: 视频保存的地址
    :param vedio_filename: 保存的视频文件名
    :param format: 人脸图像的文件格式
    :return:
    """
    # 判断文件夹是否存在
    if os.path.exists(images_path) is False:
        # TODO 外壳程序提示需要进行合并的人脸视频的图片为空
        return -1
    # 打开已经处理好的人脸图片
    filelist = os.listdir(images_path)
    # !!!如果人脸图片命名方式改变，这个程序应该废了
    filelists = sorted(filelist, key=lambda x: int(x.split(".")[0]))

    # 判断文件夹是否为空
    if len(filelists) == 0:
        # TODO 提示文件夹为空
        return -2

    # 获取人脸图片大小
    filelist = os.listdir(images_path)
    path = filelist[0]
    path = os.path.join(images_path, path)
    image = skimage.io.imread(path)
    size = (image.shape[1], image.shape[0])

    # 判断保存视频文件夹是否存在
    if os.path.exists(vedio_save_path) is False:
        os.mkdir(vedio_save_path)

    # 保存视频绝对路径
    real_save_vedio = os.path.join(vedio_save_path, vedio_filename)

    # 开启vedio上下文
    video = cv2.VideoWriter(real_save_vedio, cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

    # 开始合成视频
    ends = "." + format
    for item in filelists:
        if item.endswith(ends):
            item = images_path + "\\" + item
            img = cv2.imread(item)
            video.write(img)
    # 释放视频上下文并保存
    video.release()
    cv2.destroyAllWindows()


def segment_vedio(vedio_path, vedio_save_path, timeF, format):
    """
    返回一共分割的视镇数
    :param vedio_path: 需要分割的视频的绝对路径
    :param vedio_save_path: 分割的图片保存绝对路径
    :param timeF: 分割的时间间隔(越小分割越多)
    :param format: 分割的图片的保存格式
    :return: 返回一共分割多少图片
    """
    # 打开视频分割上下文
    vc = cv2.VideoCapture(vedio_path)
    # 是否提取视频flag
    rflag = False

    # 保存一共分割多少视频帧
    c = 0
    # 文件序号
    num = 1
    # 判断视屏是否能够打开
    if vc.isOpened():
        rflag = True
    else:
        # TODO 外壳程序提示视频不能打开
        return -1

    # 保存的文件格式
    image_format = "." + format
    if os.path.exists(vedio_save_path) is False:
        os.mkdir(vedio_save_path)

    # 视屏能够打开，开始提取视屏中帧
    while rflag:
        rflag, frame = vc.read()
        if(c%timeF == 0):
            filename = str(num) + image_format
            pic_save_path = os.path.join(vedio_save_path, filename)
            # 每个timeF帧进行保存
            cv2.imwrite(pic_save_path, frame)
            num = num + 1
        c = c + 1
    # 关闭视频上下文
    vc.release()
    # 返回一共分割的视镇数
    return num - 1




if __name__ == "__main__":
    # # 测试视频合成
    # # TODO 这里路径是绝对路径，需要改成相对路径
    # images_path = "C:\\Users\\12455\\Desktop\\test1\\testface"
    # fps = 12
    # # 这里是要处理人脸图片大小
    # vedio_save_path = "./vedio"
    # vedio_filename = "vedio.avi"
    # format = "png"
    # synthetic_video(images_path, fps,vedio_save_path, vedio_filename, format)


    # 测试视频分割
    vedio_path = "C:\\Users\\12455\\Desktop\\test1\\video\\1.mp4"
    vedio_save_path = "./facevedio"
    timeF = 10
    format = "png"
    segment_vedio(vedio_path, vedio_save_path, timeF, format)



