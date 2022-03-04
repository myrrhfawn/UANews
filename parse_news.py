import requests
from bs4 import BeautifulSoup

URL= "https://www.pravda.com.ua/news/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
           'accept': '*/*'}
HOST = "https://www.pravda.com.ua"


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='article_news_list')

    news = []
    for item in items:
        head = item.find('div', class_='article_header')
        subhead = item.find('div', class_='article_subheader').get_text()
        img = item.find('img')
        if subhead:
            subheader = subhead
        else:
            subheader = None
        if img:
            image = img.get('src')
        else:
            image = None

        news.append({
            'time': item.find('div', class_='article_time').get_text(),
            'header': head.find('a').get_text().replace('ВІДЕО', ''),
            'subheader': subheader,
            'href': HOST + item.find('a').get('href'),
            'image': image,
        })
    return news


def parse(url):
    html = requests.get(url, headers=HEADERS)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("error")

if __name__ == '__main__':
    parse(URL)


