import requests
from bs4 import BeautifulSoup
import re
import string
import os


titles = []


def get_content(link):
    r = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
    return r


def soup_find(r, tag, attrs):
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all(tag, attrs)

num_of_pages = int(input())
article_type = input()
for i in range(1, num_of_pages + 1):
    dir_name = f'Page_{i}'
    os.mkdir(dir_name)
    r = get_content(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}')
    for link in soup_find(r, 'a', {'data-track-action': 'view article'}):
        link = 'https://www.nature.com' + link.get('href')
        r = get_content(link)
        if soup_find(r, 'meta', {'name': 'dc.type', 'content': f'{article_type}'}):
            content = soup_find(r, 'p', {'class': 'article__teaser'})
            title = soup_find(r, 'h1', {'class': 'c-article-magazine-title'})[0].text
            title = re.sub(re.escape(string.punctuation), '', title)
            title = re.sub(' ', '_', title).strip() + '.txt'
            titles.append(title)
            file_path = os.path.join(dir_name, title)
            with open(file_path, 'wb') as file:
                for p in content:
                    file.write(p.text.encode())
print(f'Saved articles: {titles}')
