import requests
from bs4 import BeautifulSoup
import datetime

URL= "https://www.pravda.com.ua/news/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
           'accept': '*/*'}
HOST = "https://www.pravda.com.ua"
LAST = datetime.datetime(2000, 1, 1)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='article_news_list')
    times = []
    news = []
    for item in items:
        head = item.find('div', class_='article_header')
        em = head.find('em')
        if em != None:
            em = em.text
            header = head.find('a').get_text().replace(em, '')
        else:
            header = head.find('a').get_text()
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
        if "https" in item.find('a').get('href'):
            link = item.find('a').get('href')
        else:
            link = HOST + item.find('a').get('href')
        t = item.find('div', class_='article_time').get_text()
        news_time = datetime.datetime.strptime(t, '%H:%M').time()
        if times and news_time > times[-1]:
            return news[::-1]
        else:
            times.append(news_time)
            news.append({
                'time': item.find('div', class_='article_time').get_text(),
                'header': header,
                'subheader': subheader,
                'href': link,
                'image': image,
            })
    return news[::-1]

def parse():
    url = "https://www.pravda.com.ua/news/"
    html = requests.get(url, headers=HEADERS)
    if html.status_code == 200:
        news = get_content(html.text)
        return news
    else:
        print("error")

if __name__ == '__main__':