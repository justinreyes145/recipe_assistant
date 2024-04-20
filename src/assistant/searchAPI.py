import requests
import os
from dotenv import load_dotenv

# Loading environment variables and retrieving google search api key and id
load_dotenv()
google_search_api = os.getenv("GOOGLE_SEARCH_API")
google_search_ID = os.getenv("GOOGLE_SEARCH_ID")

# Function to search the web using a query
def search_web(query):
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
    return results

# Testing
# print(search_web("I want a hamburger recipe"))
