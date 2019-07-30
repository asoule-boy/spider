import re
import urllib.request
import urllib.parse
import os.path


def re_request(url):#发出请求，并返回页面
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",}
    request = urllib.request.Request(url=url,headers=header)
    response = urllib.request.urlopen(request)
    return response.read().decode()


def re_findall(response):#根据返回的页面，进行正则匹配出图片链接地址，并返回一个列表
    com_pattern = re.compile(r'<div class="thumb">.*?<a href=.*?<img src="(.*?)" alt=".*?</div>',re.S)
    finda = com_pattern.findall(response)
    return finda

def main(start_page,end_page,path):
    url = "https://www.qiushibaike.com/pic/page/"
    for page in range(start_page,end_page +1):
        urls = url + str(page) + "/"
        print("正在爬取第%d 页"%page)
        response = re_request(urls)
        list = re_findall(response)
        download(list,path,page)


def download(list,path,page):
    num = 0
    for img_url in list:
        num += 1
        img_urls = "https:" + img_url
        filename = str(page) + "_" + str(num) + ".jpg"
        finallypath = os.path.join(path,filename)
        print("正在下载第%d 页中第%d 张" % (page,num))
        urllib.request.urlretrieve(img_urls,finallypath)


if __name__ == "__main__":
    start_page = int(input("请输入起始页面："))
    end_page = int(input("请输入终止页面："))
    nowpath = os.getcwd()
    if os.path.exists("糗事百科图片"):
        os.remove("糗事百科图片")
    os.mkdir("糗事百科图片")
    path = nowpath + "\糗事百科图片"
    main(start_page,end_page,path)
