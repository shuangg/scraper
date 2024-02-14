# https://www.youtube.com/watch?v=dYWnS8eRf4M
# Building a CLI Tool | Scraping & Processing Data with BeautifulSoup, Requests & Pydantic
import requests
from bs4 import BeautifulSoup, Tag
from pprint import pprint
from pydantic import BaseModel, AnyHttpUrl
from datetime import date

class Episode(BaseModel):
    show_number: int
    date: date
    title: str
    url: AnyHttpUrl
    guest: str

def extract_episode_data(row: Tag) -> dict:
    model_data = {}
    row_data = row.select( 'td')
    for i, td in enumerate(row_data):
        if i == 0:
            model_data['show_number'] = td.text.replace('#', '')
        elif i == 1:
            model_data['date'] = td.text
        elif i == 2:
            link = td.find('a')
            model_data['url'] = base_url + link.attrs['href']
            model_data['title'] = link.text
        elif i == 3:
            model_data['guest'] = td.text
    return model_data

base_url = 'https://talkpython.fm'
url = 'https://talkpython.fm/episodes/all'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.select('tbody > tr')
# episodes = []
# for row in rows:
#     data = extract_episode_data(row)
#     episodes.append(Episode(**data))
# As a one-liner
episodes = [Episode(**extract_episode_data(row)) for row in rows]
def search_episodes():
    search_term = input('Enter a search term: ')
    results = [episode for episode in episodes if search_term.lower() in episode.title.lower()]
    print(f"Found {len(results)} episodes with the term {search_term}")
    pprint(results)
    search_episodes()

search_episodes()