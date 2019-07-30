import urllib.request
import re
import ssl
#有序字典
from collections import OrderedDict
#写入数据
from pyexcel_xls import save_data

def doubanCrawlel(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36"
    }

    req = urllib.request.Request(url, headers=headers)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(req,context=context)
    HTML = response.read().decode("utf-8")
    #print(HTML)
    #print(type(HTML))
    expression =r'{"rating":.*?:false}'
    compileExpression = re.compile(expression,re.S)
    crawlelList = compileExpression.findall(HTML)
    #print(crawlelList)
    lists = []

    for cra in crawlelList:
        listmin = []
        #电影名               #以下内容可写for循环
        movieEnpression = r',"title":"(.*?)",'
        compileMovie = re.compile(movieEnpression,re.S)
        movienames = compileMovie.findall(cra)
        moviename = movienames[0]
        listmin.append(moviename)
        #print(moviename)

        #豆瓣排名
        rankEnpression = r',"rank":(.*?),'
        compilerank = re.compile(rankEnpression, re.S)
        ranknames = compilerank.findall(cra)
        rankname = ranknames[0]
        listmin.append(rankname)
        #print(rankname)

        #上映日期
        timeEnpression = r'"release_date":"(.*?)",'
        compiletime= re.compile(timeEnpression, re.S)
        timenames = compiletime.findall(cra)
        timename = timenames[0]
        listmin.append(timename)
        #print(timename)
        #拍摄国家地点
        countryEnpression = r'"regions":(.*?),'
        compilecountry = re.compile(countryEnpression, re.S)
        countrynames = compilecountry.findall(cra)
        countryname = countrynames[0]
        listmin.append(countryname)
        #print(countryname)
        #电影类型
        typeEnpression = r'"types":(.*?),"regions"'
        compiletype = re.compile(typeEnpression, re.S)
        typenames = compiletype.findall(cra)
        typename = typenames[0]
        listmin.append(typename)
        #print(typename)
        #分数
        scoreEnpression = r'"score":"(.*?)",'
        compilescore = re.compile(scoreEnpression, re.S)
        scorenames = compilescore.findall(cra)
        scorename = scorenames[0]
        listmin.append(scorename)
        #print(scorename)
        #演员
        actorEnpression = r'"actors":(.*?),"is_watched"'
        compileactor = re.compile(actorEnpression, re.S)
        actornames = compileactor.findall(cra)
        actorname = actornames[0]
        listmin.append(actorname)
        #print(actorname)

        lists.append(listmin)

    return lists

def makeExcelFile(path, dict):
    dic = OrderedDict()
    for sheetName, sheetValue in dict.items():
        d = {}
        d[sheetName] = sheetValue
        dic.update(d)

    save_data(path, dic)

excelPath = r"C:\Users\xbdzh\Desktop\Python\代码练习\爬虫\电影排行榜.xls"
finallyList = [["电影名","豆瓣排名","上映日期","拍摄国家","电影类型","豆瓣评分","主要演员"]]
for i in range(0,30):
    url = r"https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start="+str(20*i)+"&limit=20"
    finallyList.extend(doubanCrawlel(url))
dict = {}
dict["电影排行榜(剧情)"] = finallyList
makeExcelFile(excelPath, dict)
