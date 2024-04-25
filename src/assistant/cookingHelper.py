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


# Create the main window
window = tk.Tk()

# Create the title
window.title("GourmetGuide")

# Set the dimensions of the main window
window.geometry("1250x750+100+10")

conv_frame = ttk.Frame(window)
conv_frame.place(x=0, y=0, relwidth=0.2, relheight=1)
ttk.Label(conv_frame, background='gray').pack(expand=True,fill='both')

main_frame = ttk.Frame(window)
main_frame.place(relx=0.2, y=0, relwidth=0.8, relheight=1)

# Logo
Logo = Image.open('chef.png')
Logo = Logo.resize((100, 100))
Logo = ImageTk.PhotoImage(Logo)
logoLabel = tk.Label(main_frame, image=Logo)
logoLabel.place(x=10,y=10)

# Label for Project
labelName = StringVar()
mainLabel = Label(main_frame, textvariable=labelName, font=("Stencil",50))
labelName.set("GourmetGuide")
mainLabel.pack()


chatbox = tk.Text(main_frame,height=13, width=100, font=("Courier", 15, "normal"), padx=10, pady=10)
chatbox.tag_configure("bold", font=("Courier", 15, "bold"))
chatbox.config(state=DISABLED)
chatbox.pack(anchor='center')

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
    main_frame,
    text="Temp",
    command=prevConvo,
    height=1,
    width=5,
    font=("Courier", 15, "normal")
)

tempButton.place(x=100,y=200)

# Set dimensions of input text field
inputTextField = Text(main_frame, width=90, height=2, font=("Courier", 15, "bold"), padx=10, pady=10)

# Placement of the text field
inputTextField.pack(anchor='center', pady=20)

askButton = tk.Button(
    main_frame,
    text="Ask!",
    command=contactGPT,
    height=1,
    width=5,
    font=("Courier", 20, "normal")
)

# Placemen of the ask button
askButton.pack(anchor='center')

# This is the command that enables the window
# Once this command is run, the window will show

window.mainloop()
