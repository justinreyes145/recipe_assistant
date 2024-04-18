import requests
import os
from dotenv import load_dotenv

load_dotenv()
google_search_api = os.getenv("GOOGLE_SEARCH_API")
google_search_ID = os.getenv("GOOGLE_SEARCH_ID")

#search = input()
search = 'i want the recipe for a hamburger'

url = 'https://www.googleapis.com/customsearch/v1'

params = {
    'q': search,
    'key': google_search_api,
    'cx': google_search_ID,
    'searchType': 'image'
}

response = requests.get(url, params=params)
results = response.json()['items'][0]['link']

print(results)
