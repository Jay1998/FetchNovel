#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import urllib.request
import re

 
def write_file(file_name, s_article):
    with open(file_name, 'a',encoding='utf8') as f:
        f.write(s_article)  
        

def read_article_XiaoShuo_chapter(article_title,article_url):#从章节里读取内容，写入小说文件里
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=article_url, headers=headers)
    html = urllib.request.urlopen(req).read()#.decode('utf8')#, 'ignore'    
    bsObj = BeautifulSoup(html, "lxml") 
    chapter_title=bsObj.find('div',attrs={'class':'bookname'}).h1.get_text()
    print(chapter_title)
    write_file(article_title, '\n'+chapter_title+'\n')
    a_list=bsObj.findAll('div',attrs={'id':'content'})    
    for a in a_list:
        s=a.get_text()
        s1=re.sub(u'(\xa0)+', '\n',s)
        s2=re.sub('(.*－－?)|(－－.*－－?)|(－－.*)','',s1,flags=re.DOTALL)
        s2=re.sub('[a-zA-Z]+?','',s2,flags=re.DOTALL)
        write_file(article_title, s2+'\n')

def read_article_title(article_url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=article_url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('gbk')#, 'ignore'   
    bsObj = BeautifulSoup(html, "lxml") 
    
    article_title=bsObj.div.h1.get_text()+'.txt'  #获得小说名字
    for ch in bsObj.find('div',attrs={'id':'list'}).findAll('a',attrs={'href':True}):#获取小说链接
        chapter_name=ch.get_text()#章节名称
        chapter_href=ch.get('href')#章节链接
#        print(ch.get_text(),'  ',chapter_href)
        read_article_XiaoShuo_chapter(article_title,chapter_href)
read_article_title('http://www.ranwen.net/files/article/81/81269/')
