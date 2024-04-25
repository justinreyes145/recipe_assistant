import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
from PIL import Image, ImageTk

#Things to implement for the future
#Implement Small login
#implement dynamically changing textbox size (not that important)
#Implement showing the text received from ChatGPT/Preloaded text file
#Remove unused and clunky code
#Add as many comments as possible

#def write_to_txt(input):
#    with open(,'r',newline='') as history:
#        for line in history:
#            history.write(input)

def GPT_answer(query):
    example_response = "DCDA"
    chatbox.config(state=NORMAL)
    chatbox.insert(END,"GourmetGuide: " + example_response + "\n")
    chatbox.config(state=DISABLED)
    #GPT_response = generate_response(query,,)
    #write_to_txt(GPT_response)

#This method is going to be the primary method in order to talk to our chatbot
def contactGPT():
    query = fileTextField.get(1.0, "end-1c")
    #The grid will go Here
    #I gotta put in a text field in order to add onto the chat more easily

    if query:
        fileTextField.delete(1.0,END)
        chatbox.config(state=NORMAL)
        chatbox.insert(END,"User: " + query + "\n")
        #write_to_txt(query)
        GPT_answer(query)
        chatbox.config(state=DISABLED)
    else:
        print("No query detected")
#End of contactGPT 

#Creating the login window
#login_window = tk.Tk()
#make the title
#login_window.title("GourmetGuide")
#set window dimensions
#login_window.geometry("1500x500")

#Create the main window
window = tk.Tk()
#Create the title
window.title("GourmetGuide")
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
logoLabel.place(x=30,y=20)

chatbox = tk.Text(window,height=33,width=225)
chatbox.config(state=DISABLED)
chatbox.place(x=55,y=300)

askButton = tk.Button(
    window,
    text="Ask!",
    command=contactGPT,
    height=2,
    width=5,
)

#Set dimensions
fileTextField = Text(width=228, height=3)
#placement of the text field
fileTextField.place(x=10,y=881)
#set the value for the text as soon as the ask button is placed

#set the button
askButton.place(x=1613,y=885)

#This is the command that enables the window
#Once this command is run, the window will show
window.mainloop()
