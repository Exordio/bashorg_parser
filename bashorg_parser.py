import requests
import os
import pandas as pd
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
base_Url = 'https://bash.im/'
count_pg_to_parse = 50
pages_List = []


def create_Pages_List(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('create pages list status 200 OK')
        soup = bs(request.content, 'lxml')
        try:
            input_PG_IN = soup.find(class_="pager__input")
            current_Count_Pages = input_PG_IN.get('value')
            for i in range(count_pg_to_parse):
                pages_List.append(base_url+(f'/index/{int(current_Count_Pages)-i}'))
               
            return pages_List
        except:
            pass
    else:
        print('create pages list error...')



def bashorg_parse(base_url, headers):

    url = base_url

    session = requests.Session()
    request = session.get(url, headers = headers)

    if request.status_code == 200:
        print('status 200 OK')

        soup = bs(request.content, 'lxml')
        try:
            current_Count_Pages = soup.find(class_="pager__input")
            print(current_Count_Pages.get('value'))
        except:
            pass

#bashorg_parse(base_Url, headers)

create_Pages_List(base_Url, headers)