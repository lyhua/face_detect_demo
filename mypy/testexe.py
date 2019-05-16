import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import *

def callback():
    fileName = filedialog.askopenfilename()
    print(fileName)

def callback1():
    fileName = colorchooser.askcolor()
    print(fileName)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("FishC Demo")
    Button(root, text="选择颜色", command=callback1).pack()
    mainloop()
