import urllib.request
import urllib.parse
import json
import jsonpath
from bs4 import BeautifulSoup

url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv12120&productId=100000287163&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1"
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Referer":"https://item.jd.com/100000287163.html",
    "Cookie":"__jdu=1543070941478785842296; unpl=V2_ZzNtbREFQRQhWk8GfxpfA2JREAlKAhRCdg5BBCtOWVJiAxVeclRCFX0UR1dnGl0UZwsZXkpcQR1FCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsdWQdmBRNVR1dGE3wOT1ByHF8GbwQibUVncyVxAENSfyldNWYzUAkeU0ASdglFGXsdWQdmBRNVR1dGE3wOT1ByHF8GbwQiXHJU; __jda=122270672.1543070941478785842296.1543070941.1547967903.1550662181.3; __jdc=122270672; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_bc30ec8c52274c3e9dff276aaf4f4162|1550662180622; PCSYCityID=1601; shshshfpa=13f56743-dd2b-2b61-bbf5-07997fa96b87-1550662184; shshshfpb=lml66Pe6OnVX1Pa6iq4xIRA%3D%3D; ipLoc-djd=1-72-4137-0; areaId=1; _gcl_au=1.1.1397748750.1550662192; 3AB9D23F7A4B3C9B=PSMVE2R6YEXQT5NOO2GD3SPSN3WGVCBPNGHOLZIUZV62Y663HI5THXLXSTFMHJNVAHKZDJICHO4GUXVE5WMQJR34K4; shshshfp=3459fb43173d49ba852335169a1a2746; shshshsID=00340ac6b7f64ccd9220d6dc072b9257_3_1550662225558; __jdb=122270672.4.1543070941478785842296|3.1550662181; JSESSIONID=ABAFB314A7E1D3CED30EDC24302F7C01.s1",
    #cookie未破解
}
req = urllib.request.Request(headers=header,url=url)
response = urllib.request.urlopen(req)
#print(response.read().decode("utf8","ignore"))
# with open("json.txt","wb") as fp:
#     fp.write(response.read())
json_text = response.read().decode("gbk","ignore").replace("fetchJSON_comment98vv12120","").strip("; () \n\t\r")
#print(json_text)
objects = json.loads(json_text)
#获取评论、时间、用户名、头像、评论图片url、手机颜色、内存大小
user_info = objects["comments"]
#print(user_info)
for user in user_info:
    content = jsonpath.jsonpath(user,"$.content")[0]
    createTime = jsonpath.jsonpath(user,"$.creationTime")[0]
    nickname = jsonpath.jsonpath(user,"$.nickname")[0]
    userImageUrl = jsonpath.jsonpath(user,"$.userImageUrl")[0]
    color = jsonpath.jsonpath(user,"$.productColor")[0]
    imgUrl = jsonpath.jsonpath(user,"$..imgUrl")
    videosUrl = jsonpath.jsonpath(user,"$..remark")[0]
    saleValue = jsonpath.jsonpath(user,"$..saleValue")[0]
    print(content,"\n",createTime,nickname,color,"\n",imgUrl,"\n",videosUrl,"\n",saleValue)
    break