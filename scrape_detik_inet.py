import csv

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
    if i.find('a')['href'] == '#':
        continue
    else:
        links.append(i.find('a')['href'])


all_row_list = []
i = 1
for link in links[:25]:
    print("Scraping: "+link)

    news = Article(link)
    news.download()
    try:
        news.parse()
        news.nlp()
        kategori = link.split('/')[3]

        row_list = [
            i,
            'detik_inet',
            news.publish_date,
            news.title,
            news.text.replace("\n", ""),
            kategori
        ]
        i += 1
        all_row_list.append(row_list)

    except Exception:
        pass

writeToCsv(all_row_list)
