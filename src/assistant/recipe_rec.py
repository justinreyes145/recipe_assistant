from openai import OpenAI
from dotenv import load_dotenv
from searchAPI import search_web
from searchAPI import default_func
import os
import time
import shelve

# Loading environment variables and retrieving openAI api key
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)


# Creating the GPT Assistant (ONLY RUN THIS ONCE!)
def create_assistant():
    assistant = client.beta.assistants.create(
        # Assigning a name to the assistant
        name="Gourmet Guide",

        # Giving specific instructions for the assistant to follow
        instructions="You are a personal cooking assistant. " +
                     "Use the search_web function included to get a recipe from online. " +
                     "Then, read the information from the returned url and provide the recipe to the user, " + 
                     "with very specific step-by-step instructions. Adjust ingredients and portion sizes based on " +
                     "user preference using your own data. Make sure to calculate macronutrients for your recommendations.",

        # Assigning tools for the assistant to use, including a code interpreter and a function for searching the internet for recipes
        tools=[{"type": "code_interpreter"},
               {"type": "function",
                "function": {
                    "name": "search_web",
                    "description": "fetch URLs for food recipes based on a search query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                        },
                        "required": ["query"]
                    }
                }
                }],

        # Assign the gpt model to be used for the assistant
        model="gpt-3.5-turbo-0125",
    )
    return assistant


# Using python's shelve library to check a local dictionary for existing conv-thread information
def check_if_thread_exists(conv_id):
    # Opening the dictionary file on read mode and checking if conv_id has corresponding thread_id
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(conv_id, None)


# Using python's shelve library to create a local dictionary that stores each thread
def store_thread(conv_id, thread_id):
    # Opening the dictionary file on write mode and writing a (key, value) pair of (conv_id, thread_id)
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[conv_id] = thread_id


# Generating a message and running the assistant based on conv_id
def generate_response(message_body, conv_id):
    # Check if there is already a thread_id for the conv_id
    thread_id = check_if_thread_exists(conv_id)

    # If a thread does not exist for the conversation, create a new one and store it in the dictionary
    if thread_id is None:
        print(f"Creating new thread for conv_id {conv_id}")
        thread = client.beta.threads.create()
        store_thread(conv_id, thread.id)
        thread_id = thread.id
    # Else, a thread exists so retrieve it from the dictionary
    else:
        print(f"Retrieving existing thread for conv_id {conv_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Adding a message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get a response
    new_message = run_assistant(thread)
    return new_message


# Running the assistant, waiting for a response, and returning the response
def run_assistant(thread):
    # Retrieve the assistant using its unique id from the openai website
    assistant = client.beta.assistants.retrieve("asst_E5HNH1zyiySRc9Wsffyk8arj")

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for the run status to be complete
    while run.status != "completed":
        # Checking every 0.5 seconds for the assistant's run status
        time.sleep(0.5)

        # Checking if the assistant is trying to call the search_web function
        if run.status == 'requires_action':
            # Retrieve the query prepared by the assistant for the search_web function
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            print(tool_calls)
            if tool_calls[0].function.name == 'search_web':
                try:
                    # Retrieve the output of the search_web function
                    tool_outputs = map(search_web, tool_calls)
                    tool_outputs = list(tool_outputs)
                    print(tool_calls)
                    print(tool_outputs)

                    # Submit the output of the search_web function to the assistant
                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id, 
                        run_id=run.id, 
                        tool_outputs=tool_outputs)
                except:
                    # If the search_web function ran into an error, tell the assistant that the function failed
                    print("API Search failed")
            else:
                # Retrieve the output of the default_func function
                tool_outputs = map(default_func, tool_calls)
                tool_outputs = list(tool_outputs)
                print(tool_calls)
                print(tool_outputs)

                # Submit the output of the default_func function to the assistant
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id, 
                    run_id=run.id, 
                    tool_outputs=tool_outputs)
        # Once the assistant has the necessary url info from search_web(), let the assistant process the information
        else: run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the messages from the thread and get the latest message (the reply from the assistant)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value

    return new_message


# Method to retrieve old message thread
def retrieve_thread(conv_id):
    thread_id = check_if_thread_exists(conv_id)
    if thread_id: 
        thread = client.beta.threads.retrieve(thread_id)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages
    else: return None


# Method to cancel a run in case of errors
def cancel_run(thread, run):
    run = client.beta.threads.runs.cancel(
        thread_id=thread,
        run_id=run
        )


# Create assistant (AGAIN ONLY RUN THIS ONCE)
if __name__ == "__main__":
    # create_assistant()
    cancel_run('thread_LWKboaNR3XPUuwK9T3UbaPjU', 'run_HuGHdfwpo9UkjIK02NjWGLKd')
