import csv
import json
import sys
from datetime import date, datetime
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from newspaper import Article


class Scraping():

    def __init__(self):
        self.cnn_page = "https://www.cnnindonesia.com/indeks/"

    def initCsvFile(self):
        with open('output/scrape-cnn-kelompok-7.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add header
            csv_writer.writerow(['link', 'title', 'author', 'publish_date',
                                 'text', 'top_image', 'keywords', 'summary'])

    def getContentLinks(self, page_until):
        links = []
        section_url = self.cnn_page + str(page_until)
        html = requests.get(section_url)

        soup = BeautifulSoup(html.content, "lxml")
        articles = soup.find_all('article')

        for article in articles:
            links.append(article.find('a')["href"])

        return links

    def getIsiBerita(self, link):
        html = requests.get(link)
        soup = BeautifulSoup(html.content, "lxml")
        d = ""
        try:
            d = soup.find("div", {"id": "detikdetailtext"}).text
        except:
            pass
        return d.replace("\n", "")

    def writeToCsv(self, data):
        now = datetime.now()
        filename = 'scrape-cnn-kelompok-7.csv'
        with open('output/'+filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def doScrape(self, page):
        links = self.getContentLinks(int(page))

        news_list = []

        for link in links:
            print("Scraping: "+link)

            news = Article(link)
            news.download()
            try:
                news.parse()
                news.nlp()

                isi_berita = news.text
                if isi_berita == "":
                    isi_berita = getIsiBerita(link)

                row_list = [
                    link,
                    news.title,
                    news.authors,
                    news.publish_date,
                    news.text,
                    news.top_image,
                    news.keywords,
                    news.summary
                ]

                news_list.append(row_list)
            except Exception as e:
                pass

        self.writeToCsv(news_list)


if __name__ == "__main__":
    scrape = Scraping()
    scrape.initCsvFile()
    for i in range(int(sys.argv[1])):
        scrape.doScrape(i+1)
