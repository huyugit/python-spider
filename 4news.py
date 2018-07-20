#-*- coding:UTF-8 -*-
import sys
import pymysql
import requests
import json
import re

import datetime
from bs4 import BeautifulSoup

from wxpy import *

num = 0
fhandle=open("news.txt","wb")
def newswrite(news):
            newsstr =str(news)
            newsstr = newsstr.lstrip()
            newsstr = newsstr.rstrip() 
            if newsstr!= "None" and newsstr !="专区" and newsstr !=")" and "点击查看" not in newsstr and newsstr!= " ":
                global num
                num +=1
                newsstr+='\n'
                newsstr = str(num)+'.'+newsstr
                print (newsstr)
                fhandle.write(newsstr.encode('utf-8'))


def getTodayNews(link):
    today = datetime.date.today()
    print (today)
    #fhandle=open("news.txt","wb")
    #datestr=today.strftime('%Y年%m-%d')
    datestr =str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
    datestr+="四大证券报头条"
    print (datestr)
    datestr +='\n'
    fhandle.write(datestr.encode('utf-8'))
    print (link)
    req1 = requests.get(url=link)
    print (req1.encoding)
    req1.encoding = 'utf-8'
    
    html2 = req1.text
    bf1 = BeautifulSoup(html2,"html.parser")
    news_texts = bf1.find_all('div', class_ = 'Body')
    for one in news_texts:
        ps=one.find_all('p')
        for p in ps:
            strongs = p.find_all('strong')
            for strong in strongs:
                spans = strong.find_all('span')
                for span in spans:
                    cmpystr =str(span.string)
                    cmpystr = cmpystr[:6]
                    if cmpystr != "None" and cmpystr != "专区" and cmpystr != ')':
                        cmpystr= cmpystr.lstrip()
                        print (cmpystr)
                        cmpystr+='\n'
                        fhandle.write(cmpystr.encode('utf-8'))
                        global num
                        num = 0
                aas = strong.find_all('a')
                for aa in aas:
                    newswrite(aa.string)
              
            aaas = p.find_all('a')
            for aaa in aaas:
                strong1s = aaa.find_all('strong')
                #print (strong1s)
                for strong1 in strong1s:
                    newswrite(strong1.string)
    
    fhandle.close()

def sendNews():
    bot = Bot(cache_path=True)
    fo=open("news.txt","r+",encoding='utf-8')
    lines= fo.read()
    bot.file_helper.send(lines)
    my_friend = bot.friends().search(u'圆圆')[0]
    my_friend.send(lines)
    fo.close()
    

if __name__ == '__main__':
   
    today = datetime.date.today()
    print (today)
    datestr=today.strftime('%Y%m%d');
    print (datestr)
    target = 'http://stock.eastmoney.com/news/cbktt.html'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    print (req.encoding)
    html = req.text
    bf = BeautifulSoup(html,"html.parser")
    news_texts = bf.find_all('div', class_ = 'text')
    for oneday in news_texts:
        onetext=oneday.find_all('a')
        #print(onetext)
        for each in onetext:
            day_link = each.get('href')
            if datestr in day_link:
                today_link = day_link
                print (today_link)
                getTodayNews(today_link)

    sendNews()
                
