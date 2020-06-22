import requests
import re
import datetime
import time


#取文本中间
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
    if end >= 0:
        return html[start:end].strip()

#这里去除引用
def getoutofli(listr):
    c = re.compile(r'<.*?>')
    ret = c.sub('', listr)
    c = re.compile(r'&#91;.*?&#93;')
    ret = c.sub('', ret)
    ret = ret.replace('&#160;','')
    return ret

#获取分类
def getfenlei( strstr ):
    match_obj_1 = re.compile(r'<li class="toclevel-1.*?><a href=".*?"><span class="tocnumber">.*?</span> <span class="toctext">.*?</span></a>', re.S)
    fenlei = re.findall(match_obj_1,strstr)
    array = []
    for i in fenlei:
        array.append('<span class="mw-headline" id="'+getmidstring(i,'<a href="#','"><')+'">')

    return array
'''
['大事记', '出生', '逝世', '节假日和习俗', '参看', '參考資料', '外部連結']
'''



#通过月日获取数据
def getdata( month , day ):
    url ="https://zh.wikipedia.org/zh-cn/"+month+"月"+day+"日"
    r = requests.get(url)
    r.encoding ='utf-8'
    so_url = r.request.url
    html = r.text
    #取标志分割
    fenlei = getfenlei(html)
    #打开文件
    f= open("data/"+month+'_'+day+".txt","w+",encoding='utf-8')
    #取大事件
    try:
        f.write('大事件\n')
        eventdata = getmidstring(html,fenlei[0],fenlei[1])
        r1 = re.compile(r'<li>.*?</li>', re.S)
        event = re.findall(r1,eventdata)
        for i in event:
            f.write(getoutofli(i)+'\n')
        #取出生
        f.write('出生\n')
        birthdata = getmidstring(html,fenlei[1],fenlei[2])
        r1 = re.compile(r'<li>.*?</li>', re.S)
        birth = re.findall(r1,birthdata)
        for i in birth:
            f.write(getoutofli(i)+'\n')
        #取去世
        f.write('去世\n')
        deathdata = getmidstring(html,fenlei[2],fenlei[3])
        r1 = re.compile(r'<li>.*?</li>', re.S)
        death = re.findall(r1,deathdata)
        for i in death:
            f.write(getoutofli(i)+'\n')
        #取风俗节日
        f.write('风俗节日\n')
        if(len(fenlei) <= 4):
            newbiaozhi = '<div id="catlinks" class="catlinks" data-mw="interface">'
            fesdata = getmidstring(html,fenlei[3],newbiaozhi)
            r1 = re.compile(r'<li>.*?</li>', re.S)
            fes = re.findall(r1,fesdata)
            for i in fes:
                f.write(getoutofli(i)+'\n')
            f.close()
        else:
            fesdata = getmidstring(html,fenlei[3],fenlei[4])
            r1 = re.compile(r'<li>.*?</li>', re.S)
            fes = re.findall(r1,fesdata)
            for i in fes:
                f.write(getoutofli(i)+'\n')
            f.close()
    except:
        print(month+"月"+day+"日录入失败！")

#主程序
if __name__ == '__main__':
    start = '2003-12-31'
    end = '2004-12-31'
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        getdata(datestart.strftime('%m'),datestart.strftime('%d'))
        print (datestart.strftime('%m')+'月'+datestart.strftime('%d')+"日录入成功！")
    




    
