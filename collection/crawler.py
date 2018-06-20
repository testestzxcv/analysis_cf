import sys
from urllib.request import Request, urlopen
from datetime import datetime
# def error(e):
#     print('%s : %s' % (e, datetime.now()), file=sys.stderr)

def crawling(url = '',
             encoding='utf-8',
             proc=lambda html: html,    # 람다는 마지막 결과를 반드시 리턴하게 되어있다.
             store = lambda html: html, # 넣지 않으면 통과(?)
             err=lambda e: print('%s : %s' % (e, datetime.now()), file=sys.stderr)):    # 크롤러 모듈에서 제공하는 에러함수 사용, 람다함수로 에러처리
    # 이부분을 함수로 만든다.
    # request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    # resp = urlopen(request)
    # html = resp.read().decode('cp949')

    try:
        request = Request(url)
        resp = urlopen(request)

        try:
            receive = resp.read()
            result = store(proc(receive.decode(encoding)))
        except UnicodeDecodeError:
            result = receive.decode(encoding, 'replace')

        print('%s: success for request [%s]' % (datetime.now(), url))
        return result

    except Exception as e:
        print("에러는 여기서 생겨욬ㅋ")
        err(e)
        # print('%s : %s' % (e, datetime.now()), file=sys.stderr)