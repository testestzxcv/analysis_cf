import urllib
import pandas as pd
import time
from datetime import datetime

import sys
from selenium import webdriver
from itertools import count
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import collection.crawler as cw
from collection.data_dict import sido_dict, gungu_dict
import re

# def my_error(e):
#     print("myerror:" + str(e))

# def proc(html):
#     print("processing..."+html)
#
# def store(result):
#     pass


# cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
#          encoding='cp949'
         # proc=proc, # 안써도 됨
         # store=store # 안써도 됨
         #             )  # 커스텀 에러처리 하고 싶을때 err=함수 이름을 쓴다.

# print("processing..." + result)

RESULT_DIRECTORY = '__result__/crawling'


def crawling_pelicana():
    results = []
    for page in count(start=1): # 1부터 진행된다 탈출조건은 만들어 줘야 한다.
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?page=%d&branch_name=&gu=&si=' % page
        html = cw.crawling(url=url)
        # print("html result === ", html)

        bs = BeautifulSoup(html, 'html.parser')
        # print("beautiful === ", bs)

        tag_table = bs.find('table', attrs={"class":'table mt20'})  # table 태그에서 class=table mt20 라인에서 시작하여 </table>이 나올때까지 스크랩한다.
        # print("tag_table === ",tag_table)
        tag_tbody = tag_table.find('tbody') # tbody 태그에서 시작하여 </tbody> 나올때까지 스크랩한다.
        # print("tag_tbody === ", tag_tbody)
        tags_tr = tag_tbody.findAll('tr') # tr 태그에서 시작하여 </tr> 나올때까지 스크랩한다.
        # print("tags_tr === ", tags_tr)

        # 끝 검출
        if len(tags_tr) == 0:
            break;

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            print("strings === ",strings)

            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]
            # print("sidogu === ", sidogu)

            results.append( (name, address) + tuple(sidogu))


    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
    # print("table === ", table)

    table['sido'] = table.sido.apply(lambda v : sido_dict.get(v, v))
    # print("table['sido'] === ", table['sido'])
    table['gungu'] = table.gungu.apply(lambda  v: gungu_dict.get(v, v))
    # print("table['gungu'] === ", table['gungu'])

    table.to_csv(   #파일 저장
        '{0}/pelicana_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)


def proc_nene(xml):
    root = et.fromstring(xml)
    results = []
    for el in root.findall('item'):
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results  # 리턴해줘야 한다.


def store_nene(data):
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.sido.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(  # 파일 저장
        '{0}/nene_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)

def crawling_kyochon():
    results = []

    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            print("sido1 === ", sido1)
            print("sido2 === ", sido2)
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            # print("url===",url)
            html = cw.crawling(url=url)
            # print("html === ",html)

            if html == None:
                print("파일없어요")
                break

            bs = BeautifulSoup(html, 'html.parser')
            # print("bs === ", bs)

            tag_div = bs.find('div', attrs={"class" : "shopSchList"})
            # print("tag_table === ", tag_div)
            tag_ul = tag_div.find('ul', attrs={"class" : "list"})
            # print("tag_ul === ", tag_ul)
            # tag_li = tag_ul.find('li')
            # print("tag_li === ", tag_li)
            tag_dl = tag_ul.findAll('dl')
            # print("tag_dl === ", tag_dl)
            # tag_dt = tag_dl.find('dt')
            # print("tag_dt === ", tag_dt)
            # tag_dd = tag_dl.findAll('dd')
            # print("tag_dd === ", tag_dd)

            for dl in tag_dl:
                # print("dl ==== loop ",dl)
                try:
                    strings = list(dl.strings)
                    print("strings === ", strings)

                    print("strings[1] =====", strings[1])
                    name = strings[1] + "점"
                    address = strings[3]
                    # print(strings[3])
                    address_after = re.sub("[\rnt]", "", address)
                    # print("address_after === ",address_after)
                    address_strip = address_after.strip()
                    print("address_after.strip() === ", address_strip)
                    sidogu = address.split()[:2]
                    print("sidogu === ", sidogu)

                    results.append((name, address_strip) + tuple(sidogu))

                    print("results === ", results)
                except Exception as e:
                    print("오류 === ", e)
                    continue



    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(  # 파일 저장
        '{0}/kyochon_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)

def crawling_goobne():
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:/bigdata/chromedriver/chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    results = []
    for page in count(start=1):
        # 자바스크립트 실행
        # <a href="javascript:store.getList('3');">3</a> url이 아니라 자바 스크립트를 실행시킨다는 의미
        script = 'store.getList(%d)' % page
        wd.execute_script(script)   # 스크립트 실행
        print('%s : success for script execute [%s]' % (datetime.now(), script))
        time.sleep(5)

        # 실행결과 HTML(rendering된 HTML) 가져오기
        html = wd.page_source  # 소스 가져오기

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 마지막 검출
        if tags_tr[0].get('class') is None: # <tr class="on 이부분이 on이 아니면 클래스가 없다는 의미
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    print(results)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v)) # get(v, v) 의 의미는 앞의 v 값이 없으면 뒤의 v값을 리턴해준다.
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(  # 파일 저장
        '{0}/gooubne_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)


def crawling_cu():
    url = 'http://cu.bgfretail.com/store/list.do?category=store'

    wd = webdriver.Chrome('D:/bigdata/chromedriver/chromedriver.exe')
    wd.get(url)
    # time.sleep(2)

    results = []
    for page in range(1, 201):
        script = 'newsPage(%d)' % page
        wd.execute_script(script)  # 스크립트 실행
        print('%s : success for script execute [%s]' % (datetime.now(), script))
        time.sleep(1)

        html = wd.page_source
        # print(html)

        bs = BeautifulSoup(html, 'html.parser')
        tag_div = bs.find('div', attrs={'class':'detail_store'})
        tag_tbody = tag_div.find('tbody')
        # print("tag_tbody === ", tag_tbody)
        tags_tr = tag_tbody.findAll('tr')
        # print("tag_tr === ", tags_tr)

        # 마지막 검출
        if tags_tr == []:
            print("끄~~~~~~~~~~~~~~~~~~읕!!!!!!!!!!!")
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            # print("strings === ",strings)
            name = strings[2]
            phone = strings[4]
            address = strings[10]
            sidogu = address.split()[:2]

            results.append((name, address, phone) + tuple(sidogu))

    print(results)

    # store
    table = pd.DataFrame(results, columns=['name', 'address','phone', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(  # 파일 저장
        '{0}/cu_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)


def crawling_mnet():
    results = []

    for year in range(2008, 2018):
        temp_year = "{0}년".format(year)
        for page in range(1, 3):
            print("page === ",page)
            url = 'http://www.mnet.com/chart/TOP100/%d?pNum=%d' % (year, page)
            print("url === ", url)

            html = cw.crawling(url=url)
            # print("html === ", html)

            if html == None:
                print("파일없어요")
                break

            bs = BeautifulSoup(html, 'html.parser')
            # print("bs === ", bs)

            tags_tr = bs.findAll('tr')
            # print('tags_tr === ',tags_tr)

            for tag_tr in tags_tr:
                strings = list(tag_tr.strings)
                # print("strings === ", strings)
                if strings == []:
                    break

                rank = strings[2]
                title = strings[14]
                if rank == "\n":
                    continue

                print("year === ", temp_year)
                print("rank === ", rank)
                print("title === ", title)

                results.append((temp_year, rank, title))

                # print("results === ", results)

    table = pd.DataFrame(results, columns=['year','rank','title'])
    table= table.set_index('year')

    table.to_csv(
        '{0}/mnet_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)


if __name__ == '__main__':

    # pelicana
    # crawling_pelicana()

    # nene
    # cw.crawling(
    #     url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'
    #         % (urllib.parse.quote("전체"), urllib.parse.quote("전체")),
    #     proc=proc_nene,
    #     store=store_nene)

    # kyochon
    # crawling_kyochon()

    # goobne
    # crawling_goobne()

    # cu
    # crawling_cu()

    # mnet
    crawling_mnet()