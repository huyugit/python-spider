#-*- coding:UTF-8 -*-
import sys
import pymysql
import requests
import json
import re

import datetime
from bs4 import BeautifulSoup

from wxpy import *

def getTodayNews(link):
    today = datetime.date.today()
    print (today)
    fhandle=open("news.txt","wb")
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
        strong=one.find_all('strong')
        for one_strong in strong:
            #print (type(one_strong))
            company=one_strong.find_all('span')
            #print (type(company))
            #print (company)
            #company.text.replace('(',' ')
            for eachs  in company:
               #print (eachs)
               cmpystr1=str(eachs.string)
               #cmpystr1.replace('(','')
               #cmpystr = cmpystr1
               cmpystr = cmpystr1[:6]
               if cmpystr != "None" and cmpystr != "专区" and cmpystr != ')':
                   cmpystr= cmpystr.lstrip()
                   print (cmpystr)
                   cmpystr+='\n'
                   fhandle.write(cmpystr.encode('utf-8'))
                   num = 0
                   #fhandle.next()
            news = one_strong.find_all('a')
            for onenews in news:
                if onenews.string != "None" and onenews.string !="专区":
                    onenewsstr = onenews.string                   
                    num +=1
                    onenewsstr+='\n'
                    onenewsstr = str(num)+'.'+onenewsstr
                    print (onenewsstr)
                    fhandle.write(onenewsstr.encode('utf-8'))
                    #fhandle.next()
    
    fhandle.close()


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

            
    #print(req.text)
    
    
    bot = Bot(cache_path=True)
    fo=open("news.txt","r+",encoding='utf-8')
    lines= fo.read()
    bot.file_helper.send(lines)
    my_friend = bot.friends().search(u'圆圆')[0]
    my_friend.send(lines)
    fo.close()
