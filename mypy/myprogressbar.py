import tkinter as tk
import time

class Progressbar:
    def __init__(self, photonums):
        self.photonums = photonums
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title('进度条')
        self.window.geometry('630x150')

        # 设置下载进度条
        self.canvas = tk.Canvas(self.window, width=465, height=22, bg="white")
        self.canvas.place(x=110, y=60)

    def create_progressbar(self):
        pass

    # 显示下载进度
    def progress(self):
        # 填充进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        x = 500  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        for i in range(x):
            n = n + 465 / x
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.window.update()
            time.sleep(0.02)  # 控制进度条流动的速度
        # 自动消亡
        self.window.destroy()



if __name__ == "__main__":
    progressbar = Progressbar(500)
    time.sleep(5)
    progressbar.progress()