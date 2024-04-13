import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk

def functionKill():
    plotType.destroy()

def createPlots():
    if selectPlot.get() == "line":
        print("Line")
    elif selectPlot.get() == "scatter":
        print("Scatter")
    elif selectPlot.get() == "histogram":
        print("Histogram")
    elif selectPlot.get() == "pie":
        print("Pie Chart")
    else:
        print("No Graph Selected")

def fileName():
    global fileNameMenu
    fileNameMenu = Toplevel(window)
    fileNameMenu.geometry("500x75")
    fileNameMenu.title("Input File Name")
    global fileTextField
    fileTextField = Text(fileNameMenu,width=60, height=1)
    fileTextField.pack(pady=5)
    fileButton = tk.Button(
        fileNameMenu,
        text="Upload File Name",
        command=textGetter
    )
    fileButton.pack(side="bottom", pady=5)
    global inputFileName

#Create the main window
window = tk.Tk()
#Create the title
window.title("DataViz")
#set the dimensions
window.geometry("1700x950")

#create the menu bar
menubar = tk.Menu(window)
#Here are all of the buttons in the
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command="none")
filemenu.add_command(label="Open", command="none")
filemenu.add_command(label="Save", command="none")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu="filemenu")
window.config(menu=menubar)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command="none")
helpmenu.add_command(label="About...", command="none")
menubar.add_cascade(label="Help", menu="helpmenu")

#Label for Project
labelName = StringVar()
mainLabel = Label(window, textvariable=labelName, font=("Stencil",50))
labelName.set("GourmetGuide")
mainLabel.pack()


#Logo
Logo = Image.open('chef.png')
Logo = ImageTk.PhotoImage(Logo)
logoLabel = tk.Label(window, image=Logo)
logoLabel.pack(fill="none", expand=True)

createButton = tk.Button(
    window,
    text="Ask!",
    command=createPlots,
    height=2,
    width=5,
)

fileTextField = Text(width=228, height=3)
fileTextField.place(x=10,y=881)
createButton.place(x=1613,y=885)
#plotPoints.pack(side="bottom", padx=20, pady=10)
#uploadButton.pack(side="bottom", padx=20, pady=10)

window.mainloop()
