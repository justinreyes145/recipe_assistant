import requests
import os
from dotenv import load_dotenv
import json

# Loading environment variables and retrieving google search api key and id
load_dotenv()
google_search_api = os.getenv("GOOGLE_SEARCH_API")
google_search_ID = os.getenv("GOOGLE_SEARCH_ID")

# Function to search the web using a query
def search_web(tool_call):
    query = json.loads(tool_call.function.arguments)["query"]

    # Loading the google api as the url for requests method
    url = 'https://www.googleapis.com/customsearch/v1'

    # Setting parameters for searching
    params = {
        'q': query,
        'key': google_search_api,
        'cx': google_search_ID
    }

    # Getting the response from search API and returning the result
    response = requests.get(url, params=params)
    results = response.json()['items'][0]['link']
    return {
        "tool_call_id": tool_call.id,
        "output": results
        }
# End of search_web()


# Function to search the web using a query
def search_image(query):
    # Loading the google api as the url for requests method
    url = 'https://www.googleapis.com/customsearch/v1'

    # Setting parameters for searching
    params = {
        'q': query,
        'key': google_search_api,
        'cx': google_search_ID,
        'searchType': 'image'
    }

    # Getting the response from search API and returning the result
    response = requests.get(url, params=params)
    results = response.json()['items'][0]['link']
    return {
        "output": results
        }
# End of search_image()


# Function to search the web using a query
def default_func(tool_call):
    # Return a message saying no function was called
    return {
        "tool_call_id": tool_call.id,
        "output": "This function does not exist."
        }
# End of search_web()


# Testing
if __name__ == "__main__":
    print(search_image("https://feelgoodfoodie.net/recipe/ground-beef-tacos-napa-cabbage-guacamole/"))
