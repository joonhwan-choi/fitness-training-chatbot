#pip install requests
#pip install BeautifulSoup4

import requests
from bs4 import BeautifulSoup
import pandas as pd

dic = {} #딕셔너리 형 자료구조
title_name = [] #음식명
title_nutrient = [] #음식 영향성분
pagenum_max = [] #자료의 최대 페이지

file_ = open('./File_.txt', 'r', encoding='UTF8') #txt 파일 read
file_name = file_.readlines()
file_.close()

html_number = 'body > div.mainContent > div.centerContent > div.centerInnerContent > div#content.mem > table.generic > tr > td.leftCell > div.leftCellContent > div.searchResultSummary '
html_list = 'body > div.mainContent > div.centerContent > div.centerInnerContent > div#content.mem > table.generic > tr > td.leftCell > div.leftCellContent > table.generic.searchResult'
html_names = 'tr > td.borderBottom > a.prominent'
html_nutrient = 'tr > td.borderBottom > div.smallText.greyText.greyLink'

def url_search(search, pagenum = 0):
    url = 'https://www.fatsecret.kr/%EC%B9%BC%EB%A1%9C%EB%A6%AC-%EC%98%81%EC%96%91%EC%86%8C/search?q=' + search + '&pg=' + str(pagenum)
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html, 'html.parser')


#페이지 계산
for search_file in file_name:
    soup = url_search(search_file)
    title_list = soup.select_one(html_number)
    pagenum_max.append(int(int(title_list.get_text().split('중')[0]) / 10) + 1)

for i, search_file in enumerate(file_name):

    for pagenum in range(pagenum_max[i]):
        soup = url_search(search_file, pagenum)
        title_list = soup.select_one(html_list)
        title_names = title_list.select(html_names)
        title_nutrients = title_list.select(html_nutrient)

        for num in range(len(title_nutrients)):
            title_name.append(title_names[num].get_text())
            title_nutrient.append(title_nutrients[num].get_text().replace('\r', '').replace('\t', '').split('\n')[1])

        print("{0}의 {1}개 완료....{2}/{3}".format(search_file, (pagenum * 10 + len(title_names)), pagenum + 1, pagenum_max[i]))

dic['title_name'] = title_name
dic['title_nutrient'] = title_nutrient

df = pd.DataFrame(dic)
df.to_csv('./keyword.csv', index=False, encoding='cp949')
