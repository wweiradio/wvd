#coding:utf8
"""wvd weibo video download
Usage:
  wvd.py  <url> <file_name> 
  wvd.py  -c  
  wvd.py --version
  wvd.py (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.
  -c            generate config file 
"""

# 下载weibo视频小助手
# leafrainy
# leafrainy.cc
# updated by Cason Wang  2020-6-25 
# TODO 
# 1.加一个配置文件，该配置文件放在当前运行目录中。可以自动生成
# 2.URL 命令行提供 -done 
# 3.保存文件的名字命令行提供，如果不提供，就自动生成一个文件名字 - done
# 

from docopt import docopt

from bs4 import BeautifulSoup as bs
import requests
import urllib
import configparser


version = "wvd 微博视频下载 1.00" 

MODE_DOWNLOAD ='mode_download'
MODE_GENERATE ='mode_generate'
MODE_VERSION = 'mode_version'
MODE_HELP = 'mode_help'

mode = 'generate'

url = ''
filename =''
config = None 


def process_cmd():
     global url, filename 
     arguments = docopt(__doc__, version=version)

     if arguments['<url>'] and arguments['<file_name>']:
          url = arguments['<url>']
          filename = arguments['<file_name>']
          return MODE_DOWNLOAD

     if arguments['-c']:
          return MODE_GENERATE
     elif arguments['-h'] or arguments['--help']:
          print(__doc__)
          return MODE_HELP
     elif arguments['--version']:
          print("wvd version:")
          print(version)
          return MODE_VERSION

          
def read_config(filename='config.ini'):
     
     config = configparser.ConfigParser()
     config.read(filename)

     sub = config.get('download','cookie') 
     if sub == '':
          sub = "_2A25z8DKDDeRhGedK7lYS9S3NzD2IHXVQhCNLrDV_PUNbm9AKLVXfkW9NIVt1oQaXS827f6hb8CnUZxyc95gyuxSI"
     
     cookieDict = {
          'SUB': sub,
          # 'SUBP': "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFuLd1BSONkRU_Ak3oGS7J75JpX5KzhUgL.Fo2XSKB0SKepS022dJLoI0MLxKqL1K-L1K.LxKMLB.eL1KqLxKMLBKnL12zLxKML1-2L1hxPi--RiKn7iKnpi--fi-zRiKnR; TC-Page-G0=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFuLd1BSONkRU_Ak3oGS7J75JpX5KzhUgL.Fo2XSKB0SKepS022dJLoI0MLxKqL1K-L1K.LxKMLB.eL1KqLxKMLBKnL12zLxKML1-2L1hxPi--RiKn7iKnpi--fi-zRiKnR",
          # 'TC-Page-G0':'f0aa2e6d566ccd1c288fae19df01df56|1593066955|1593066952',
          # 'TC-V5-G0':'595b7637c272b28fccec3e9d529f251a',
          # '_s_tentry':'weibo.com',
          # 'Apache':'615072946933.9633.1593064866472',
          # 'SINAGLOBAL':'125.33.103.252_1593064867.462337',
          # 'WBStorage':'42212210b087ca50|undefined',
          # 'ULV':'1593064866492:1:1:1:615072946933.9633.1593064866472:'
     }

     cookieList = [ item+'='+cookieDict[item] for item in cookieDict.keys()]
     cookie = ';'.join(cookieList)

     return cookie 

def write_config_file(filename='config.ini', config=None):

     if config is None:
          config = configparser.ConfigParser()
          config['download'] = {'cookie':''}

     with open(filename, 'w') as configfile:
          config.write(configfile)


def process_download() :
     global url, filename

     weiboUrl = url if url != '' else "https://weibo.com/tv/v/J5h6W858w?fid=1034:4512574033559561" 
     mp4Name = filename if filename != '' else "test_default.mp4"

     cookie = read_config()

     header = {'cookie':cookie,'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
     allData = requests.get(weiboUrl,headers=header)

     divData = bs(allData.content,'lxml').find('div',{'class':'weibo_player_fa'}).find_all('div')[0]

     #找到最后的，清晰度最高的一项
     urlQuote = str(divData).split(";")[-2].split("=")[1]
     decodedUrl = urllib.parse.unquote(urlQuote)

     print(decodedUrl)

     url = urllib.parse.unquote(urlQuote)
     r = requests.get(url)
     with open(mp4Name, "wb") as code:
          code.write(r.content)
          print(mp4Name+":下载完成")

def proces_help():
     print("help")

def process_version():
     print("version is", version)

def process_generate():
     print("genenrate")
     write_config_file()

if __name__ == "__main__":
     
     working_mode  = process_cmd()

     if working_mode == MODE_DOWNLOAD:
          process_download()
     elif working_mode == MODE_GENERATE:
          process_generate()
     elif working_mode == MODE_HELP:
          process_help()
     elif working_mode == MODE_VERSION:
          process_version()
     else:
          process_help() 