import requests
from bs4 import BeautifulSoup

def download_png(url,header,s):
    r = s.get(url=url,headers=header)
    soup = BeautifulSoup(r.text,"lxml")
    view = soup.find("input",id="__VIEWSTATE")["value"]
    views = soup.find("input",id="__VIEWSTATEGENERATOR")["value"]
    png = soup.find("img",id = "imgCode")["src"]
    png_url = "https://so.gushiwen.org"+png
    image = s.get(url=png_url,headers=header)
    with open("code.png","wb") as fp:
        fp.write(image.content)
    return view,views
    
def login(s,view,views,header):
    code = input("兄嘚，请输下验证码呗：")
    formData = {
        "__VIEWSTATE": view,
        "__VIEWSTATEGENERATOR": views,
        "from": "",
        "email": "*********@qq.com", #邮箱
        "pwd": "*******",   #密码
        "code": code,
        "denglu": "登录",
    }
    loginUrl = "https://so.gushiwen.org/user/login.aspx?from="
    rs = s.post(url=loginUrl,headers=header,data=formData)
    with open("login.html","w",encoding="utf8") as fp:
        fp.write(rs.text)
    
def main():
    s = requests.session()
    url = "https://so.gushiwen.org/user/login.aspx"
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
    view, views = download_png(url,header,s)
    login(s,view,views,header)
    
if __name__ == '__main__':
    main()