from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import shelve
from urllib.error import HTTPError


# Loading environment variables and retrieving openAI api key
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)

# ------------------------------------------------
# Creating the GPT Assistant (ONLY RUN THIS ONCE!)
# ------------------------------------------------
def create_assistant():
    assistant = client.beta.assistants.create(
        name="Gourmet Guide",
        instructions="You are a personal cooking assistant. Provide recipes and adjust ingredients and portion sizes based on user preference using your own data. Make sure to calculate macronutrients for your recommendations.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-0125",
    )
    return assistant

# create_assistant()

# --------------------------------------------------------------
# Using python's shelve library to create a local dictionary that stores each thread
# --------------------------------------------------------------
def check_if_thread_exists(user_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(user_id, None)

def store_thread(user_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[user_id] = thread_id