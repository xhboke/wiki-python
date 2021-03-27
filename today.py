import requests, re, json
from urllib.parse import unquote
import datetime


def preg(pattern, str):
    return re.findall(pattern, str)


def get_mid_string(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def get_str_count(target, str):
    return str.count(target)


def curl_get(url):
    proxies = {
        "http": "http://127.0.0.1:10809",
        "https": "http://127.0.0.1:10809",
    }
    return requests.get(url, proxies=proxies).text


def clearRubbish(str):
    str = re.sub("中华民国", "中国台湾", str)
    return str


def clearHtml(html):
    html = re.sub("<sup(.*)</sup>", "", html)  # 去除参考文献
    html = re.sub("<span(.*)</span>", "", html)  # 去除Span标签
    return clearRubbish(re.compile(r'<[^>]+>', re.S).sub('', html))


def get_today_data_and_save_data(fileName, html):
    _title = preg('<li class="toclevel-1(.*)<span class="toctext">(.*)</span>', html)
    _len = len(_title)
    _returnDict = {}
    for _i in _title:
        _now = _i[1]
        _data = get_mid_string(html, '<span class="mw-headline" id="' + _now + '">', '<h2>')
        if _data:
            _returnDict[_now] = []
            _list = preg('<li>(.*)</li>', _data)
            for _l in _list:
                _returnDict[_now].append(clearHtml(_l))
    _json = json.dumps(_returnDict, ensure_ascii=False)
    f = open('./data/' + fileName + '.json', 'w', encoding='utf-8')
    f.writelines(str(_json))
    f.close()


if __name__ == '__main__':
    start = datetime.datetime.now()
    baseUrl = 'https://zh.wikipedia.org/'
    all_days_url = baseUrl + 'wiki/历史上的今天'
    start_flag = '<table border="0" cellpadding="4" cellspacing="0" align="center">'
    end_flag = '<span class="mw-editsection"><span class="mw-editsection-bracket">'
    month_day = get_mid_string(curl_get(all_days_url), start_flag, end_flag)
    month_day_arr = preg('<a href="/(.*)" title="', month_day)
    for i in month_day_arr:
        now_month_day = unquote(i)[5:]
        month_data = curl_get(baseUrl + i.replace('wiki', 'zh-cn'))
        get_today_data_and_save_data(now_month_day, month_data)
        print('[tips]:' + now_month_day)
    end = datetime.datetime.now()
    print((end - start).seconds)
