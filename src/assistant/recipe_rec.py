from openai import OpenAI
from dotenv import load_dotenv
import os


# Loading environment variables and retrieving openAI api key
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)

# Creating the GPT Assistant (ONLY RUN THIS ONCE!)
def create_assistant():
    file = client.files.create(file=open())
    assistant = client.beta.assistants.create(
        name="Cooking Assistant",
        instructions="You are a personal chef assistant. Provide recipes from the given dataset and adjust them based on user preference using your own data.",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-0125",
        file_ids=[file.id]
    )
    return assistant
