
#50+ pages for parsig, from bash.im
#dependence of the number of pluses to the ratio of the number of characters in the quote
#frequency of the word "joke"
#graph of the number of "likes"
#table with the distribution of the number of posts by date

import requests
import threading
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
base_Url = 'https://bash.im'
count_pg_to_parse = 50
find_word = 'шутка'
csv_File = 'output_Quote_Date.csv'
pages_url_List = []
column_Names = ['quote_Number', 'quote_text', 'count_symbols', 'quote_total', 'quote_date', 'quote_link']
parsed_Data_Df = pd.DataFrame(columns = column_Names)


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
            print(f'\nPages list created : {datetime.now().time()}\n')

            return pages_url_List
        except:
            pass
    else:
        print('create pages list/ error...')

def bashorg_parse(pages_url_List, headers):
    for url in pages_url_List:
        session = requests.Session()
        request = session.get(url, headers = headers)
        if request.status_code == 200:
            print(f'\n | {url} - status 200 OK |')
            soup = bs(request.content, 'lxml')
            divs = soup.find_all(class_ = "quote__frame")
            for div in divs:
                try:
                    quote_number = div.find('a', attrs = {'class' : 'quote__header_permalink'}).text
                    quote_href = f'''{base_Url}{div.find(class_ = "quote__header_permalink").get('href')}'''
                    quote_text = str(div.find('div', attrs = {'class' : 'quote__body'}).text).lstrip(' ')
                    count_symbols = len(quote_text)
                    quote_total = int(div.find('div', attrs = {'class' : 'quote__total'}).text)
                    quote_date = div.find('div', attrs = {'class' : 'quote__header_date'}).text[9:20] # 9:20 из за len строки 34, получаем ровную
                    parsed_Data_Df.loc[len(parsed_Data_Df)] = [quote_number, quote_text, count_symbols, quote_total, quote_date, quote_href]
                except:
                    pass

def parallelize_parsing(pages_url_list, func, headers): #парс в 2 потока
    start_time = datetime.now().time()
    print('\n\n ------------|| START PARSING ||------------')
    print(f'\nParsing start : {start_time}')
    #a, b, c ,d, e, f = np.array_split(pages_url_list, 6)
    a, b  = np.array_split(pages_url_list, 2) # разделение списка на 2 части
    e1 = threading.Event()
    e2 = threading.Event()
    t1 = threading.Thread(target=func, args=(a, headers))
    t2 = threading.Thread(target=func, args=(b, headers))
    t1.start()
    t2.start()
    e1.set()
    t1.join()
    t2.join()
    end_time = datetime.now().time()
    print(f'\nParsing complete : {end_time}\n')
    print(f'Start {start_time}  end : {end_time}')
    print('\n ------------|| END PARSING ||------------\n\n')


def word_Frequency(parsed_data, search_word):
    count_word = 0
    for index, row in parsed_data.iterrows():
        text = row['quote_text'].lower()
        c = Counter(text.split())
        count_word += c[search_word]
    print(f' | На {count_pg_to_parse} страниц, постов проверено {25*count_pg_to_parse} : слово "{search_word}" встречалось : {count_word} раз |')


def graphic_barplot_nbr_Likes(parsed_Data_Df):
    ax = parsed_Data_Df.sort_values(by='quote_total', ascending = False)
    ax = ax.head(10) # Для удобства 10 лучших
    ax = ax.plot.bar(x='quote_Number', y='quote_total', rot=0, color = '#cc0000', align = 'center', fontsize = 8)
    ax.set_xlabel('Number of quote')
    ax.set_ylabel('Count likes')
    ax.set_title('graph of the number of likes with descending sort')
    ax.plot()
    plt.savefig('nbr_like_plot.png')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

def graphic_Dependence_CSymb_To_Likes(dependence_DF):
    ax = dependence_DF
    ax = ax.plot(x = 'count_symbols', y = 'quote_total', rot = 0, style ='.-', color = '#cc0000')
    ax.legend(['count_symbols/quote_total'])
    ax.set_xlabel('Count symbols')
    ax.set_ylabel('Count likes')
    ax.set_title('dependence of the number of pluses to the ratio of the number of characters in the quote')
    ax.grid(which="major", linewidth=1.2)
    ax.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
    ax.plot()
    plt.savefig('Dependence_plot.png')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

def create_Dependence_df(parsed_Data_Df):
    dependence_DF = parsed_Data_Df[['quote_total', 'count_symbols']]
    dependence_DF = dependence_DF.sort_values(by='count_symbols', ascending = True)#[#Сортировка от меньшего
    return dependence_DF

def df_to_list(parsed_data_df):
    list_ar = parsed_data_df['quote_date'].values.tolist()
    return list_ar

def create_Table(parsed_data_df, csv_filename):
    df_to_list(parsed_data_df)
    count_Posts_on_date = Counter(df_to_list(parsed_data_df))
    to_table_df = pd.DataFrame(columns = ['post_Date', 'count_Posts'])
    for i in count_Posts_on_date:
        to_table_df.loc[len(to_table_df)] = [i, count_Posts_on_date.get(i)]
    to_table_df['post_Date'] = pd.to_datetime(to_table_df.post_Date, dayfirst = True)
    to_table_df = to_table_df.sort_values(by='post_Date', ascending = False)
    print(to_table_df)
    to_table_df.to_csv(csv_filename, sep=';', encoding='utf-8', index = False)



def main():
    print(f'Time start: {datetime.now().time()}')
    parallelize_parsing(create_Pages_List(base_Url, headers), bashorg_parse, headers)

    print(' ------------|| ANALYSIS PART ||------------\n')

    word_Frequency(parsed_Data_Df, find_word)

    print('\n | Launch dependence graph |')
    graphic_Dependence_CSymb_To_Likes(create_Dependence_df(parsed_Data_Df))

    print('\n | Launch graph of the number of likes with sort |')
    graphic_barplot_nbr_Likes(parsed_Data_Df)

    print('\n | Create table with the distribution of the number of posts by date | \n')
    create_Table(parsed_Data_Df, csv_File)

    print('\n | Launch file | \n')
    try:
        os.startfile(csv_File)
    except AttributeError:
        print(' | On linux module os, has no attribute startfile. Check directory to exec csv file | ')

    print('\n ALL DONE \n')
    print('\n ------------|| END ANALYSIS PART ||------------\n')

if __name__ =="__main__":
    main()



