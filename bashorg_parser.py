
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
count_pg_to_parse = 2
pages_url_List = []
column_Names = ['quote_Number', 'quote_text', 'count_symbols', 'quote_total', 'quote_date', 'quote_link']
parsed_Data_Df = pd.DataFrame(columns = column_Names)

print(f'Time start: {datetime.now().time()}')

def create_Pages_List(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers = headers)
    if request.status_code == 200:
        print('create pages list status 200 OK')
        soup = bs(request.content, 'lxml')
        try:
            current_Count_Pages = soup.find(class_ = "pager__input").get('value') # Получение номера страницы
            for i in range(count_pg_to_parse): # отсчет 50
                pages_url_List.append(base_url+(f'/index/{int(current_Count_Pages)-i}')) # добавление 50 ссылок
                print(f'Successful append : {pages_url_List[i]}')

            print(f'Pages list created : {datetime.now().time()}\n')

            return pages_url_List
        except:
            pass
    else:
        print('create pages list/ error...')




def bashorg_parse(pages_url_List, headers):
    print(f'Parsing start {datetime.now().time()}')
    i = 0
    for url in pages_url_List:
        session = requests.Session()
        request = session.get(url, headers = headers)
        if request.status_code == 200:
            print(f'\n | {url} - status 200 OK | \n')
            soup = bs(request.content, 'lxml')
            divs = soup.find_all(class_ = "quote__frame")
            for div in divs:
                try:
                    quote_number = div.find('a', attrs = {'class' : 'quote__header_permalink'}).text
                    quote_href = f'''{base_Url}{div.find(class_ = "quote__header_permalink").get('href')}'''
                    quote_text = div.find('div', attrs = {'class' : 'quote__body'}).text
                    count_symbols = len(quote_text)
                    quote_total = div.find('div', attrs = {'class' : 'quote__total'}).text
                    quote_date = div.find('div', attrs = {'class' : 'quote__header_date'}).text[9:20] # 9:20 из за len строки 34, получаем ровную

                    parsed_Data_Df.loc[len(parsed_Data_Df)] = [quote_number, quote_text, count_symbols, quote_total, quote_date, quote_href]

                except:
                    pass
                i += 1
    
                print(f'{quote_number} |  count symbols : {count_symbols} |  count pluses : {quote_total}'
                      f' |  quote date : {quote_date} |')



#bashorg_parse(base_Url, headers)

#print(create_Pages_List(base_Url, headers))

bashorg_parse(create_Pages_List(base_Url, headers) ,headers)