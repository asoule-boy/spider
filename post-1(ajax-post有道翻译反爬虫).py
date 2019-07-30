import urllib.request,urllib.parse,time,random,hashlib

post_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
word = input("input:")
c = "p09@Bn{h02_BIEe]$P^nG"
ts = int(time.time() * 1000)
salt =str(int(time.time() * 1000)) + str(random.randint(1, 10))
sign = hashlib.md5(( 'fanyideskweb'+ word + salt + c).encode('utf-8')).hexdigest()

form_data = {"i":word,
             "from": "AUTO",
             "to": "AUTO",
             "smartresult": "dict",
             "client": "fanyideskweb",
             "salt": salt,
             "sign": sign,
             "ts": ts,
             "bv": "9920fbb76fd558e911cf93832183285b",
             "doctype": "json",
             "version": "2.1",
             "keyfrom": "fanyi.web",
             "action": "FY_BY_REALTIME",
             "typoResult": "false"}
form_data = urllib.parse.urlencode(form_data).encode()

header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
          "Referer": "http://fanyi.youdao.com/",
          #"Origin": "http://fanyi.youdao.com",
          #"X - Requested - With": "XMLHttpRequest",
          "Cookie": "OUTFOX_SEARCH_USER_ID=744686868@59.111.179.154; _ntes_nnid=88530289beeca2a0a1a6a7a0df4f2252,1544100809503; OUTFOX_SEARCH_USER_ID_NCOO=1406107827.2885666; JSESSIONID=aaakMpcvwHVjXct6l4GHw; ___rl__test__cookies=1547881592644"}

req = urllib.request.Request(headers=header,url=post_url,method="POST")
res = urllib.request.urlopen(req,data=form_data)
print(res.read().decode())