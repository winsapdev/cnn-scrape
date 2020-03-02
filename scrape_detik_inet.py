import csv
import sys
import os

import requests
from bs4 import BeautifulSoup
from newspaper import Article


def writeToCsv(data):
    with open('output/scrape-detik-inet.csv', 'a+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['article_number', 'media_name',
                         'date_publication', 'title', 'content', 'category'])
        writer.writerows(data)


cnn_page = 'https://inet.detik.com/'
html = requests.get(cnn_page)

soup = BeautifulSoup(html.content, "lxml")
articles = soup.find_all('article')

# print(articles)
links = []
for i in articles:
    links.append(i.find('a')['href'])

# remove '#'
stopword = ['#']
for i in links:
    if i in stopword:
        links.remove(i)

# print(links)
# print(len(links))
all_row_list = []
i = 0
for link in links:
    print("Scraping: "+link)

    news = Article(link)
    news.download()
    try:
        news.parse()
        news.nlp()

        row_list = [
            i,
            'detik_inet',
            news.publish_date,
            news.title,
            news.text.replace("\n", ""),
            'teknologi'
        ]
        i += 1
        all_row_list.append(row_list)
    except Exception:
        pass

writeToCsv(all_row_list)
