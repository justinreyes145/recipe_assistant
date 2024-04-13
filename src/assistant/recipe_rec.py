from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
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


# url = 'https://www.allrecipes.com/recipe/240935/spicy-chipotle-lentil-burgers/'
# url = 'https://www.allrecipes.com/recipe/222582/baked-spaghetti/'
# try:
#    response = requests.get(url)
#    response.raise_for_status()
# except HTTPError as hp:
#     print(hp)
     
# else:
#     print("It works")