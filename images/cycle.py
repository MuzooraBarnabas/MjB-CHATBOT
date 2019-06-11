from tkinter import*
from tkinter import ttk
from tkinter import*
from tkinter import ttk, messagebox, filedialog, simpledialog, scrolledtext
from datetime import datetime, date, time
import time, webbrowser, sqlite3
from itertools import cycle
import tkinter as tk
from time import sleep
from math import trunc
import tkinter.font as tkFont

cycleT = Tk()
cycleT.title("Image Cycle")
cycleT.geometry("300x300")




#------------slide show--------------
images = ["1.png", "2.png", "3.png"]
photos = cycle(PhotoImage(file=image) for image in images)

def slideShow():
  img = next(photos)
  disaplyscreen.config(image=img, bg="lightgray")
  cycleT.after(100, slideShow)

pic = PhotoImage(file="1.png")
disaplyscreen = Label(cycleT, text='\n', image=pic, compound=BOTTOM, font=('times', 10, 'bold'))
disaplyscreen.pack()


refL = Label(cycleT, text="Cycle Images")
refL.pack()

def cyc(*args):
	cycleT.after(10, lambda: slideShow())

def cycStop(*args):
	disaplyscreen.config(image=pic)
	

ref = ttk.Button(cycleT, text="Refresh", command=cyc)
ref.pack()

ttk.Button(cycleT, text="Stop Cycle", command=cycStop).pack()


cycleT.mainloop()