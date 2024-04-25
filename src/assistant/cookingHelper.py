import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import time
from PIL import Image, ImageTk
from recipe_rec import generate_response
from recipe_rec import retrieve_thread

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

current_conv_id = '2'

# Method to get answer from assistant and display the answer on the chat box
def GPT_answer(query):
    chatbox.config(state=NORMAL)
    response = generate_response(query, current_conv_id)
    chatbox.insert(END,"GourmetGuide: ", "bold")
    chatbox.insert(END,response + "\n\n", "normal")
    chatbox.config(state=DISABLED)
    chatbox.update()

# This method is going to be the primary method in order to talk to our chatbot
def contactGPT():
    query = inputTextField.get(1.0, "end-1c")
    # The grid will go Here
    # I gotta put in a text field in order to add onto the chat more easily

    if query:
        inputTextField.delete(1.0,END)
        chatbox.config(state=NORMAL)
        chatbox.insert(END,"User: ", "bold")
        chatbox.insert(END,query + "\n\n", "normal")
        chatbox.config(state=DISABLED)
        chatbox.update()
        GPT_answer(query)
    else:
        print("No query detected")
#End of contactGPT 

def open_user_select():
   top = Toplevel(window)
   top.geometry("750x250+585+415")
   top.title("Profiles")
   top.resizable(False, False)
   top.focus_force()


# Create the main window
window = tk.Tk()

# Create the title
window.title("GourmetGuide")

# Set the dimensions of the main window
window.geometry("1700x950+100+10")

# create the menu bar
menubar = tk.Menu(window)

# Here are all of the buttons in the
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

# Label for Project
labelName = StringVar()
mainLabel = Label(window, textvariable=labelName, font=("Stencil",50))
labelName.set("GourmetGuide")
mainLabel.pack()

# Logo
Logo = Image.open('chef.png')
Logo = Logo.resize((200, 200))
Logo = ImageTk.PhotoImage(Logo)
logoLabel = tk.Label(window, image=Logo)
logoLabel.place(x=30,y=20)

chatbox = tk.Text(window,height=13, width=100, font=("Courier", 15, "normal"), padx=10, pady=10)
chatbox.tag_configure("bold", font=("Courier", 15, "bold"))
chatbox.config(state=DISABLED)
chatbox.place(x=35,y=250)

askButton = tk.Button(
    window,
    text="Ask!",
    command=contactGPT,
    height=1,
    width=5,
    font=("Courier", 20, "normal")
)

# Method to retrieve previous conversations
def prevConvo():
    chatbox.delete(1.0, END)

    old_messages = retrieve_thread('1')
    i = old_messages.data.__len__() - 1
    while i >= 0:
        message = old_messages.data[i].content[0].text.value
        role = old_messages.data[i].role

        chatbox.config(state=NORMAL)
        if role == 'user': 
            chatbox.insert(END,"User: ", "bold")
            chatbox.insert(END,message + "\n\n", "normal")
        else:
            chatbox.insert(END,"GourmetGuide: ", "bold")
            chatbox.insert(END,message + "\n\n", "normal")
        chatbox.config(state=DISABLED)
        i -= 1

tempButton = tk.Button(
    window,
    text="Temp",
    command=prevConvo,
    height=1,
    width=5,
    font=("Courier", 15, "normal")
)

tempButton.place(x=100,y=200)

# Set dimensions of input text field
inputTextField = Text(window, width=90, height=2, font=("Courier", 15, "bold"), padx=10, pady=10)

# Placement of the text field
inputTextField.place(x=40,y=800)

# Placemen of the ask button
askButton.place(x=1570,y=800)

# This is the command that enables the window
# Once this command is run, the window will show

window.mainloop()
