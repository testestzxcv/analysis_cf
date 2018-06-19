##1##

from bs4 import BeautifulSoup

html = '<td class="title">	<div class="tit3">'\
	    '<a href="/movie/bi/mi/basic.nhn?code=158178" '\
        'title="독전">독전</a></div></td>'

# 1. tag 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    print("bs== ",bs)   # html 데이터 전체출력

    tag = bs.td
    print("bs.td== ",tag)   # bs.td 태그 이후 데이터 전체 출력

    tag = bs.a
    print("bs.a== ",tag)   # bs.a 태그 이후 데이터 전체 출력
    print("tag.name== ", tag.name)   # tag name 출력

    tag = bs.td
    print("tag.div== ", tag.div)   # bs.div 태그 이후 데이터 전체 출력

# 2. attribute 값
def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(tag['class']) # td에서 class 값 출력

    tag = bs.div    # div 저장
    #엘리먼트는 각각의 ID가 있다.
    #엘리먼트의 속성을 바꾼다. (자바스크릭트 주용도)
    # 없는값은 에러
    # print(tag['id'])

    print(tag.attrs)

# 3. attributes 조회
def ex3():
    bs = BeautifulSoup(html, 'html.parser')
    print(bs)

    tag = bs.find('td', attrs={'class':'title'}) # td 중에 attrs가 class 가 title인 데이터
    print(tag)

    tag = bs.find(attrs={'class':'tit3'})
    print(tag)


if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()