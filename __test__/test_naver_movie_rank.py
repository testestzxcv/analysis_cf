##2##

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
resp = urlopen(request)
html = resp.read().decode('cp949')
# print("html === ",html)

bs = BeautifulSoup(html, 'html.parser')
print("bs.prettify ===", bs.prettify())

tags = bs.findAll('div', attrs={'class':'tit3'})   # findAll 리스트형식으로 나온다
print("tags === ",tags)

for index, tag in enumerate(tags):
    print(index+1, tag.a.text, tag.a['href'], sep=' : ')   # tag 밑에 a 태그 밑에 text만 출력
    # 1 : 탐정: 리턴즈 : /movie/bi/mi/basic.nhn?code=159892 <- 이런 형식으로 출력됨
    #인덱스 :   text   :      tag.a['href']         각 항목을 : 으로 구분하여 출력


