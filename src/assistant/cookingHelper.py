import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText
from conversations import retrieve_conversations
from conversations import save_conversation
from recipe_rec import generate_response
from recipe_rec import retrieve_thread
from functools import partial


# Setting global variable for current conversation id and retrieving all existing conversations
current_conv_id = '0'
conv_list = retrieve_conversations()
print(conv_list)

# Method to get answer from assistant and display the answer on the chat box
def GPT_answer(query):
    chatbox.config(state=NORMAL)

    # Get the response from assistant
    response = generate_response(query, current_conv_id)

    # Insert response into chat box
    chatbox.insert(END,"GourmetGuide: ", "red")
    chatbox.insert(END,response + "\n\n", "normal")
    chatbox.config(state=DISABLED)
    chatbox.update()
# End of GPT_answer()


# This method is going to be the primary method in order to talk to our chatbot
def contactGPT():
    # Retrieve the text from the input field
    query = inputTextField.get(1.0, "end-1c")

    # If query exists, send it to the assistant, else do nothing
    if query:
        # Delete current input text
        inputTextField.delete(1.0,END)

        # Insert query to chat box
        chatbox.config(state=NORMAL)
        chatbox.insert(END,"User: ", "green")
        chatbox.insert(END,query + "\n\n", "normal")
        chatbox.config(state=DISABLED)
        chatbox.update()

        # Get assistant response
        GPT_answer(query)
    else:
        print("No query detected")
# End of contactGPT()


# Create the main window
window = tk.Tk()

# Create the title
window.title("GourmetGuide")

# Set the dimensions of the main window
window.geometry("1250x750+100+10")

# Create a frame to input the conversation buttons into
conv_frame = ttk.Frame(window)
conv_frame.place(x=0, y=0, relwidth=0.2, relheight=1)
conv_frame.columnconfigure((0), weight=1)

# Create a frame for the main chat box
main_frame = ttk.Frame(window)
main_frame.place(relx=0.2, y=0, relwidth=0.8, relheight=1)
main_frame.columnconfigure((0,1,2), weight=1, uniform='a')

# Label for Project
labelName = StringVar()
mainLabel = Label(main_frame, textvariable=labelName, font=("Stencil",50))
labelName.set("GourmetGuide")
mainLabel.grid(row=0,column=0, sticky='nswe', columnspan=2)

# Logo
Logo = Image.open('chef.png')
Logo = Logo.resize((50, 50))
Logo = ImageTk.PhotoImage(Logo)
logoLabel = tk.Label(main_frame, image=Logo)
logoLabel.grid(row=0, column=2, sticky='nswe', columnspan=1)

# Creating the chat box with scroll bar
chatbox = ScrolledText(main_frame,height=20, width=100, font=("Courier", 15, "normal"), padx=10, pady=10, wrap=WORD)
chatbox.tag_configure("green", font=("Courier", 15, "bold"), foreground="green")
chatbox.tag_configure("red", font=("Courier", 15, "bold"), foreground="red")

# Disabling the chat box to start with
chatbox.config(state=DISABLED)

# Chatbox placement
chatbox.grid(row=1,column=0, sticky='nswe', columnspan=3, padx=5)


# Method to retrieve previous conversations
def prevConvo(conv_id):
    conv_id = str(conv_id)
    print(f'conv_id:{conv_id}')

    # Set current_conv_id to id of prev conv
    global current_conv_id
    current_conv_id = conv_id

    # Delete the current displayed text on the chat box
    chatbox.config(state=NORMAL)
    chatbox.delete(1.0, END)
    chatbox.config(state=DISABLED)
    chatbox.update()

    # Retrieve the conversation based on thread
    old_messages = retrieve_thread(conv_id)

    # Print the conversations on the thread if one exists
    if old_messages:
        i = old_messages.data.__len__() - 1
        while i >= 0:
            # Get the message and role
            message = old_messages.data[i].content[0].text.value
            role = old_messages.data[i].role

            # Insert message into chat box based on role
            chatbox.config(state=NORMAL)
            if role == 'user': 
                chatbox.insert(END,"User: ", "green")
                chatbox.insert(END,message + "\n\n", "normal")
            else:
                chatbox.insert(END,"GourmetGuide: ", "red")
                chatbox.insert(END,message + "\n\n", "normal")
            chatbox.config(state=DISABLED)
            i -= 1
    
    # Allow user to input queries
    inputTextField.config(state=NORMAL)
# End of prevConvo()


# Method to delete old text from chat box and initialize new conversation
def newConvo():
    # Delete the current displayed text on the chat box
    chatbox.config(state=NORMAL)
    chatbox.delete(1.0, END)
    chatbox.config(state=DISABLED)
    chatbox.update()

    # Delete the current displayed text on the input text box
    inputTextField.delete(1.0, END)
    inputTextField.config(state=DISABLED)

    # Getting a new conversation id
    global current_conv_id
    current_conv_id = f'{retrieve_conversations().__len__()}'
    print(current_conv_id)
    createConvo()
# End of newConvo()


# Method to create new conversation
def createConvo():
    # Creating pop up window for saving
    save_window = Toplevel(window)
    save_window.geometry("300x200")
    save_window.title("New Conversation")

    # Creating label for save window
    save_label = StringVar()
    save_title = Label(save_window,textvariable=save_label,font=("Courier", 20, "normal"))
    save_label.set("Conversation Name")
    save_title.pack(pady=10)

    # Creating input field for save window
    ConvoTitleField = Text(save_window,width=60,height=1,font=("Courier", 20, "normal"), padx=10, pady=10)
    ConvoTitleField.pack(pady=10)

    # Creating button for save window
    save_button = tk.Button(
        save_window,
        text="Save",
        font=("Courier", 20, "normal"),
        background='gray20',
        command=partial(saveConvo, ConvoTitleField, save_window),
        foreground='white'
    )
    save_button.pack(pady=10)
# End of createConvo()


# Method to save new convo in list
def saveConvo(conv_field, save_window):
    # Getting the title of the conversation and saving it in the convos_db file
    title = conv_field.get(1.0, "end-1c")

    # If there is text in the field, create the new conversation
    if title:
        save_conversation(current_conv_id, title)
        save_window.destroy()

        # Retrieving the list of conversations to update the side buttons
        global conv_list
        conv_list = retrieve_conversations()
        updateConvos()
        window.update()
        
        # Allow user to input queries
        inputTextField.config(state=NORMAL)
# End of saveConvo()


# Creating new conversation button
newConvoButton = tk.Button(
    conv_frame,
    text="New Conversation",
    command=newConvo,
    height=1,
    width=5,
    font=("Courier", 15, "normal"),
    background='gray10',
    foreground='white'
)

# Placing new conversation button in the left frame
newConvoButton.grid(row=0,column=0,sticky='nswe',columnspan=1, padx=5, pady=5)

# Set dimensions of input text field
inputTextField = Text(main_frame, width=80, height=2, font=("Courier", 15, "bold"), padx=10, pady=10, wrap=WORD)

# Placement of the text field
inputTextField.grid(row=2,column=0, sticky='nswe', columnspan=2, pady=10, padx=5)

# Disable the text field on start up to prevent queries with non-existing conversation ids
inputTextField.config(state=DISABLED)

# Creating the button for communicating with the AI
askButton = tk.Button(
    main_frame,
    text="Ask!",
    command=contactGPT,
    height=1,
    width=5,
    font=("Courier", 20, "normal")
)

# Placement of the ask button
askButton.grid(row=2,column=2, sticky='nswe', columnspan=1, pady=10, padx=5)

# Method to update the list of conversations
def updateConvos():
    # Iterating over all the saved conv_id and conv_titles
    id = 0
    for val in conv_list:
        # Creating a new button for each conv
        newButton = tk.Button(
            conv_frame,
            text=val,
            command=partial(prevConvo, id),
            font=("Courier", 15, "normal")
        )
        # Setting the new button placement
        newButton.grid(row=id+1,column=0,sticky='nswe',columnspan=1, padx=10, pady=5)
        id += 1
# End of updateConvos()


# Update the list of conversations and pop up the main window
updateConvos()
window.mainloop()
