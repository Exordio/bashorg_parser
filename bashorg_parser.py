
#50+ pages for parsig, from bash.im
#dependence of the number of pluses to the ratio of the number of characters in the quote
#frequency of the word "joke"
#graph of the number of "likes"
#table with the distribution of the number of posts by date

import requests
import os
import json
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
base_Url = 'https://bash.im'
count_pg_to_parse = 1
pages_url_List = []

print(f'Time start: {datetime.now().time()}')

def create_Pages_List(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('create pages list status 200 OK')
        soup = bs(request.content, 'lxml')
        try:
            input_PG_IN = soup.find(class_="pager__input")
            current_Count_Pages = input_PG_IN.get('value') # Получение номера страницы
            for i in range(count_pg_to_parse): # отсчет 50
                pages_url_List.append(base_url+(f'/index/{int(current_Count_Pages)-i}')) # добавление 50 ссылок
                print(f'Successful append : {pages_url_List[i]}')

            print(f'Pages list created : {datetime.now().time()}\n')

            return pages_url_List
        except:
            pass
    else:
        print('create pages list/ error...')

def write_to_json(quote_nbr, quote_txt, quote_total, quote_date):
    with open('test.json' 'r')


def bashorg_parse(pages_url_List, headers):
    print(f'Parsing start {datetime.now().time()}\n')
    i = 0
    for url in pages_url_List:
        session = requests.Session()
        request = session.get(url, headers = headers)
        if request.status_code == 200:
            print(f'{url} - status 200 OK')
            soup = bs(request.content, 'lxml')
            divs = soup.find_all(class_="quote__frame")
            for div in divs:
                try:
                    quote_number = div.find('a', attrs = {'class' : 'quote__header_permalink'}).text
                    quote_text = div.find('div', attrs = {'class' : 'quote__body'}).text
                    count_symbols = len(quote_text)
                    quote_total = div.find('div', attrs = {'class' : 'quote__total'}).text
                    quote_date = div.find('div', attrs = {'class' : 'quote__header_date'}).text[9:20] # 9:20 из за len строки 34, ровная дата


                except:
                    pass
                i += 1
                print('{0} - {1} \n Кол во символов : {2} - Кол во лайков {3}'
                      ' Цитата {4} Дата публикации : {5}'.format(i, quote_text, count_symbols, quote_total, quote_number, quote_date))

#bashorg_parse(base_Url, headers)

#print(create_Pages_List(base_Url, headers))

bashorg_parse(create_Pages_List(base_Url, headers) ,headers)