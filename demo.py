#-*- coding:utf-8 -*-
# import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
# from myprogressbar import Progressbar
from mypy.myprogressbar import Progressbar
import threading
from PIL import Image
import time
# import glob
# import numpy as np
from mypy import video
# from video import *
from mypy import facemodel
# import facemodel
import threading
import shutil
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

sys.path.append("./mypy")

# 互斥锁
semaphore = threading.Semaphore(1)

# 是否重新加载权重
is_load_weights = True



# 被检测视屏的路径
video_path = ""

# 分割的视频保存路径
vedio_save_path = "./facevedio"

# 分割的视频的格式
format = "png"

# 处理后的人脸图像存放位置
face_images_path = "./faceimage"

# 检测完的视频保存路径
video_save_path ="./vedio"

# 保存的视频的名字
video_name = "vedio.avi"


def center_window(root, width, height):
    """
    设置窗口大小以及窗口位置
    :param root:窗口句柄
    :param width: 窗口宽度
    :param height:窗口高度
    :return:
    """
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height)/2 - 150)
    root.geometry(size)

def create_memu(root):
    """
    创建窗口菜单
    :param root: 窗口句柄
    :return:
    """
    # 创建一个顶级菜单
    menubar = Menu(root)
    # 创建一个文件下拉菜单
    filemenu = Menu(menubar, tearoff=False)
    filemenu.add_command(label="打开", command=open_file)
    filemenu.add_separator()
    # 退去软件
    filemenu.add_command(label="退出", command=root.quit)
    menubar.add_cascade(label="文件", menu=filemenu)

    # 创建编辑下拉菜单
    editmenu = Menu(menubar, tearoff=False)
    editmenu.add_command(label="检测视频效果最佳检测", command=check_video_good)
    editmenu.add_command(label="速度最快检测", command=check_video)
    editmenu.add_command(label="打开检测视频", command=open_vedio_dir)
    menubar.add_cascade(label="编辑", menu=editmenu)

    # 显示菜单
    root.config(menu=menubar)


def open_vedio_dir():
    pwd = os.getcwd()
    vedio_abspath = os.path.join(pwd, "vedio")
    print(vedio_abspath)
    if os.path.exists(vedio_abspath) is False:
        messagebox.showerror("error", "不存在检测视频")
        return -1
    # 打开相应的文件夹
    os.startfile(vedio_abspath)

# TODO 检测视频有没有被篡改
def check_video():
    # 删除之前处理的视频帧
    remove_path = os.getcwd()
    remove_path = os.path.join(remove_path, "faceimage")
    remove_dir(remove_path)

    # 检测视频有没有被篡改
    # TODO 检测多个视频这里可能有bug
    global face_image_display
    face_image_display = 1
    print("开始检测视频 video_path ", video_path)
    # TODO 视频是否存在以及视频的格式是否满足要求
    # 没有输入视频文件
    if video_path == "":
        messagebox.showerror("error", "请先输入视频文件")
        return
    if os.path.exists(video_path) is False:
        # 提示没有选择视频
        messagebox.showerror("error", "视频文件不存在")
        return
    else:
        # 文件存在，开始进行检测
        print("开始检测视频")
        # create_progressbar()
        # 创建进度条，开始检测视频
        # TODO 创建进度条提示用户
        # t1 = threading.Thread(target=create_progressbar)
        # t1.start()
        # 先进行视频分割
        # vedio_num 为视频分割的帧数
        messagebox.showinfo("", "正在预处理视频，请等待!")
        # vedio_num = 18
        vedio_num = video.segment_vedio(video_path, vedio_save_path, 10, format)

        # print("vedio_num ", vedio_num)

        # TODO 创建两个线程（一个处理视频图片， 一个显示后的图片）
        # 进行人脸检测
        messagebox.showinfo("", "开始检测视频")
        # 创建检测线程
        # detect_more_face(vedio_save_path, face_images_path)
        # TODO 显示处理后的视频图片
        # 创建人脸显示线程
        face_display_thread = threading.Thread(target=images_thread_dispaly, args=(face_images_path, vedio_num, "png", root, ))
        # 创建人脸检测线程
        detect_face_thread = threading.Thread(target=facemodel.detect_face_thread, args=(vedio_save_path, face_images_path, vedio_num, video_save_path, video_name))

        face_display_thread.setDaemon(True)
        detect_face_thread.setDaemon(True)

        # 开启人脸心事线程
        face_display_thread.start()
        # 开启人脸处理线程
        detect_face_thread.start()

        # face_display_thread.join()
        # detect_face_thread.join()


# TODO 检测视频有没有被篡改
def check_video_good():
    # 删除之前处理的视频帧
    remove_path = os.getcwd()
    remove_path = os.path.join(remove_path, "faceimage")
    remove_dir(remove_path)

    # 检测视频有没有被篡改
    # TODO 检测多个视频这里可能有bug
    global face_image_display
    face_image_display = 1
    print("开始检测视频 video_path ", video_path)
    # TODO 视频是否存在以及视频的格式是否满足要求
    # 没有输入视频文件
    if video_path == "":
        messagebox.showerror("error", "请先输入视频文件")
        return
    if os.path.exists(video_path) is False:
        # 提示没有选择视频
        messagebox.showerror("error", "视频文件不存在")
        return
    else:
        # 文件存在，开始进行检测
        print("开始检测视频")
        # create_progressbar()
        # 创建进度条，开始检测视频
        # TODO 创建进度条提示用户
        # t1 = threading.Thread(target=create_progressbar)
        # t1.start()
        # 先进行视频分割
        # vedio_num 为视频分割的帧数
        messagebox.showinfo("", "正在预处理视频，请等待!")
        # vedio_num = 181
        vedio_num = video.segment_vedio(video_path, vedio_save_path, 2, format)

        # print("vedio_num ", vedio_num)

        # TODO 创建两个线程（一个处理视频图片， 一个显示后的图片）
        # 进行人脸检测
        messagebox.showinfo("", "开始检测视频")
        # 创建检测线程
        # detect_more_face(vedio_save_path, face_images_path)
        # TODO 显示处理后的视频图片
        # 创建人脸显示线程
        face_display_thread = threading.Thread(target=images_thread_dispaly, args=(face_images_path, vedio_num, "png", root, ))
        # 创建人脸检测线程
        detect_face_thread = threading.Thread(target=facemodel.detect_face_thread, args=(vedio_save_path, face_images_path, vedio_num, video_save_path, video_name))

        # 开启人脸心事线程
        face_display_thread.start()
        # 开启人脸处理线程
        detect_face_thread.start()


def remove_dir(path):
    """
    删除该文件夹中的所有内容
    :param path: 文件夹的绝对路径
    :return:
    """
    if os.path.exists(path) is False:
        # TODO提示文件夹不存在
        return -1
    filelists = os.listdir(path)
    for f in filelists:
        filepath = os.path.join(path, f)
        # 判断是不是文件
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)




# TODO 打开文件
def open_file():
    """
    获取文件的绝对路径
    :return: 返回文件的路径
    """
    fileName = filedialog.askopenfile()
    if fileName is not None:
        print(fileName.name)
        # 判断文件是不是视频文件
        if(is_vedio(fileName.name) is False):
            messagebox.showerror("error", "不支持这种格式或这不是视频文件")
            return
        # 保存打开的需要检测视频的位置(全局变量)
        global video_path
        video_path = fileName.name
        # print("video_path ", video_path)
        messagebox.showinfo("", "视频加载成功")
        return fileName.name

# 判断文件是不是视频文件
def is_vedio(vedio_path):
    """
    判断给定路径是不是视频文件(根据后缀名判断)
    :param vedio_path: 视频绝对路径
    :return:
    """
    vedio_formats = ["mp4", "wmv", "asf", "asx", "rmvb", "avi", "dat", "mkv", "flv", "vob"]
    # 获取视频名字
    filename = vedio_path.split("\\")[-1]
    # 获取视频格式
    format = filename.split(".")[-1]
    # if format == "mp4" or format == "wmv" or format == "asf" or  format == "asx" or format == "rmvb":
    if format in vedio_formats:
        return True
    else:
        return False

# 创建进度条
def create_progressbar():
    progressbar = Progressbar(500)
    progressbar.progress()

# TODO 这两个变量需要谨慎使用(如果把它变成类的成员变量比较好)
# 全局变量保存图片的数量
face_image_num = 181
# 全局变量保存要显示的图片
face_image_display = 1

def image_display():
    """
    显示检测的视频
    :return:
    """
    # TODO 这里写死了，需要改成相对目录
    # TODO 这里必须改成相对目录
    image_path = "C:\\Users\\12455\\Desktop\\test1\\testface1"
    image_temp_save = "C:\\Users\\12455\\Desktop\\test1\\tempsave\\temp.png"

    global face_image_display
    global photo
    global imgLabel
    # TODO 这里图片格式写死了
    image_filename = str(face_image_display) + ".png"
    image_path = os.path.join(image_path, image_filename)
    print("image_path ", image_path)
    # image_path = "F:\\v1\\vdeiopic1\\1.png"
    image = Image.open(image_path)
    # TODO 根据实际情况进行缩放
    image = image.resize((960, 540), Image.ANTIALIAS)
    image.save(image_temp_save)
    photo = PhotoImage(file=image_temp_save)
    imgLabel.configure(image=photo, width=960, height=540)

    # 改变全局变量
    # global face_image_display
    face_image_display = face_image_display + 1
    if(face_image_display == face_image_num):
        return
        face_image_display = 1
    imgLabel.after(1000, image_display)


def images_thread_dispaly(face_images_path, image_nums, format, root):
    # TODO 用完要删除
    image_temp_save = "./tempsave/temp.png"
    # 判断暂存文件是否存在
    if os.path.exists("./tempsave") is False:
        os.mkdir("./tempsave")

    # 一直等待人脸处理程序把处理好的人脸放在该文件件
    while True:
        if os.path.exists(face_images_path):
            break
        else:
            time.sleep(1)

    # 等待部位空
    # 打开已经处理好的人脸图片
    filelist = os.listdir(face_images_path)
    # !!!如果人脸图片命名方式改变，这个程序应该废了
    filelists = sorted(filelist, key=lambda x: int(x.split(".")[0]))
    while True:
        if len(filelists) != 0:
            break
        else:
            # 打开已经处理好的人脸图片
            filelist = os.listdir(face_images_path)
            # !!!如果人脸图片命名方式改变，这个程序应该废了
            filelists = sorted(filelist, key=lambda x: int(x.split(".")[0]))
            time.sleep(1)

    # 开始异步显示
    global face_image_display
    global photo
    global imgLabel

    # 获取锁
    if semaphore.acquire():
        print("face_display")
        # 打开已经处理好的人脸图片
        filelist = os.listdir(face_images_path)
        # !!!如果人脸图片命名方式改变，这个程序应该废了
        filelists = sorted(filelist, key=lambda x: int(x.split(".")[0]))

        # TODO!!!!!!!!
        length = len(filelists)
        if length > face_image_display:
            length = face_image_display

        # TODO 这里图片格式写死了
        # image_filename = str(face_image_display) + "." + format
        image_filename = str(length) + "." + format

        # TODO 这里有bug
        # image_path = os.path.join(face_images_path, image_filename)
        image_path = face_images_path + "/" + image_filename
        print("image_path ", image_path)

        # 判断文件是否存在
        if os.path.exists(image_path):
            image = Image.open(image_path)
            # TODO 根据实际情况进行缩放
            image = image.resize((960, 540), Image.ANTIALIAS)
            image.save(image_temp_save)
            photo = PhotoImage(file=image_temp_save)
            imgLabel.configure(image=photo, width=960, height=540)

            # 改变全局变量
            face_image_display = face_image_display + 1
        # 已经显示到末尾，不在显示，结束
        # 释放锁
        semaphore.release()
        if len(filelists) != image_nums:
            time.sleep(4)
    if length == image_nums:
        pwd = os.getcwd()
        vedio_abspath = os.path.join(pwd, "vedio")
        messagebox.showinfo("检测完成", "请到%s查看检测视频或点击打开检测视频按钮" % vedio_abspath)
        # TODO !!!!!!!(重新刷新主线程)
        # root.mainloop()
        # 退出子线程
        # 删除所有提取的视频帧
        remove_path = os.getcwd()
        remove_path = os.path.join(remove_path, "facevedio")
        remove_dir(remove_path)
        sys.exit(0)
        return
    else:
        imgLabel.after(1000, images_thread_dispaly(face_images_path=face_images_path, image_nums=image_nums, format=format, root=root))




if __name__ == "__main__":
    root = Tk()
    root.title("demo")
    # 设置窗口大小以及位置
    center_window(root, 1080, 600)
    # 创建菜单
    create_memu(root)

    # TODO 这里需要改成相对目录
    real_path = "./img/begin.png"
    # real_path = "F:\\v1\\vdeiopic1\\1.png"
    global photo
    photo = PhotoImage(file=real_path)
    global imgLabel
    imgLabel = Label(root, image=photo, width=960, height=540, compound="center")
    imgLabel.pack()

    # 进行标签以后监听事件
    # imgLabel.after(1000, image_display)

    # 禁止改变窗口大小
    root.resizable(0, 0)

    root.mainloop()


