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
        t = item.find('div', class_='article_time').get_text()
        news_time = datetime.datetime.strptime(t, '%H:%M').time()
        if times and news_time > times[-1]:
            return news[::-1]
        else:
            times.append(news_time)
            news.append({
                'time': item.find('div', class_='article_time').get_text(),
                'header': head.find('a').get_text().replace('відео, фото', '').replace('відео', '').replace('фото', '').replace('список', '').replace('документ', '').replace('ВІДЕО', ''),
                'subheader': subheader,
                'href': HOST + item.find('a').get('href'),
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
    '''newss = parse()
    start_time = datetime.datetime.now() - datetime.timedelta(hours=2)
    start2_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    for news in newss:
        news_time = datetime.datetime.strptime(str(start_time.date()) + ' ' + news['time'], '%Y-%m-%d %H:%M')
        if news_time > start_time and news_time < start2_time:
            if news['subheader'] != None:
                title = f" *{news['header']}*\n{news['subheader']}\n*{news['time']}*"
            else:
                title = f" *{news['header']}*\n*{news['time']}*"

            if news['image'] == None:
                print(news['time'])
                LAST = news_time
            else:
                print(news['time'])
                LAST = news_time
    '''
    newss = parse()
    """for news in newss:
        now_time = datetime.datetime.now().time()
        news_time = datetime.datetime.strptime(news['time'], '%H:%M').time()
        print(now_time)
        print(news['time'])
        print(now_time > news_time)"""
    for news in newss:
        print(news['image'])
