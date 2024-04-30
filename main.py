from bs4 import BeautifulSoup
from urllib.request import urlopen


URL = urlopen("https://www.cnews.ru/reviews/videonabludenie_2023/articles/rossijskie_postavshchiki_videoanalitiki")
page = BeautifulSoup(URL, features='lxml')

for i in page.find('body').find_all(id='table8069'):
    i = i.text.strip()
    print(i)