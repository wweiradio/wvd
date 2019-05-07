#coding:utf8
#下载weibo视频小助手
#leafrainy
#leafrainy.cc

from bs4 import BeautifulSoup as bs
import requests
import urllib

weiboUrl = "https://weibo.com/tv/v/HsC2doyzB?fid=1034:4368193872168868"
mp4Name = "789.mp4"
cookie = "SUB=_2AkMrjQZOf8NxqwJRmPAdxW3iao92yQ_EieKd0feVJRMxHRl-yT9jqnwttRB6AA0ooVVm2V3z9NmvaaQBW49sgyDC3Var; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9Wh_xQjrkMWQwHVyvXhYTE9l; TC-Page-G0=2f200ef68557e15c78db077758a88e1f|1557236089|1557236085; TC-V5-G0=841d8e04c4761f733a87c822f72195f3; _s_tentry=passport.weibo.com; Apache=888864284052.7195.1557236090682; SINAGLOBAL=888864284052.7195.1557236090682; WBStorage=dbba46d4b213c3a3|undefined; ULV=1557236090737:1:1:1:888864284052.7195.1557236090682:"
header = {'cookie':cookie,'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
allData = requests.get(weiboUrl,headers=header)
divData = bs(allData.content,'lxml').find('div',{'class':'weibo_player_fa'}).find_all('div')[0]
urlQuote = str(divData).split(";")[-2].split("=")[1]
url = urllib.parse.unquote(urlQuote)
r = requests.get(url)
with open(mp4Name, "wb") as code:
     code.write(r.content)
     print(mp4Name+":下载完成")
