
# coding: utf-8

# In[3]:


# coding: utf-8
import requests
import random
import time
import codecs
import json
import urllib.request
import re
import sys
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
from urllib import error
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


def judge_element(browser,href,filename,word):
    time.sleep(0.1)
    html_text = browser.page_source
    href_list = []
    try:
        bs = BeautifulSoup(html_text,"html.parser")
        tmp = bs.find("ul",class_="custom_dot para-list list-paddingleft-1")
        div_list = tmp.find_all("div",class_="para")
        for div in div_list:
            a = div.find("a")
            href = "https://baike.baidu.com" + a.get("href")
            href_list.append(href)
            filename.append(a.text)
        return href_list
    except AttributeError:
        href_list.append(href)
        filename.append(word)
        return href_list
    except TypeError:
        href_list.append(href)
        filename.append(word)
        return href_list
    else:
        href_list.append(href)
        filename.append(word)
        return href_list

def get_detail(browser,url,file_name,word):
    time.sleep(0.1)
    #f = codecs.open("C://Users//Zhang//Desktop//tmp//bdbk//" + file_name + ".txt","w","utf-8")
    html_text = browser.page_source
    bs = BeautifulSoup(html_text,"html.parser")
    try:
        dd = bs.find("dd",class_="lemmaWgt-lemmaTitle-title")
        title = dd.text
        title = title.replace("\n","")
        title = title.replace(title[-4:],"")
        abstract = bs.find("div",class_="lemma-summary")
        abst = abstract.find("div",class_="para").text
        div_list_title = bs.find_all("div",class_="para-title level-2")
        #print(div_list_title)
        title_level_2 = []
        redict = {'topic_word':'','abstract':'','cols':[],'body':[],'extendWords':{},'info_box':{}}
        for div_title in div_list_title:
            try:
                h2 = div_title.find("h2",class_="title-text").text
                tmp_len = len(word)
                h2 = h2[tmp_len:]
                title_level_2.append(h2)
            except AttributeError:
                continue
        redict['topic_word'] += title
        redict['abstract'] += abst
        redict['cols'] = title_level_2
        para_list = bs.find_all("div",class_="para")
        content = [""]*len(title_level_2)
        for para in para_list:
            try:
                h3_tmp = para.find_previous("div",class_="para-title level-2")
                h3 = h3_tmp.find("h2",class_="title-text").text
                tmp_len = len(word)
                h3 = h3[tmp_len:]
                index = title_level_2.index(h3)
                content[index] += para.text
            except AttributeError:
                continue
        redict['body'] = content
        info_box = {}
        div_table = bs.find("div",class_="basic-info cmn-clearfix")
        dt_list = div_table.find_all("dt")
        dd_list = div_table.find_all("dd")
        index = 0
        for dt in dt_list:
            text1 = dt.text
            text2 = dd_list[index].text
            text1 = text1.replace("\xa0","")
            text2 = text2.replace("\n","")
            info_box[text1] = text2
            index += 1
        redict['info_box'] = info_box
        title = title.replace("/","")
        with open("C://Users//Zhang//Desktop//tmp//bdbk//"+title+".json","w+",encoding="utf-8") as f:
            json.dump(redict,f,ensure_ascii=False)
    except AttributeError:
        url = "https://baike.baidu.com/search/none?word="+word+"&pn=0&rn=10&enc=utf8"
        browser.get(url)
        redict = {'topic_word':'','abstract':'','cols':[],'body':[],'extendWords':{},'info_box':{}}
        tmp = {}
        time.sleep(0.1)
        html_text = browser.page_source
        bs = BeautifulSoup(html_text,"html.parser")
        try:
            search_list = bs.find("dl",class_="search-list")
            dd_list = search_list.find_all("dd")
            for dd in dd_list:
                word_tmp = dd.find("a").text
                word_tmp = word_tmp.replace("_百度百科","")
                explan = dd.find("p").text
                tmp[word_tmp] = explan
            redict['extendWords'] = tmp
        except AttributeError:
            tmp = {'None':"None"}
            redict['extendWords'] = tmp
        word = word.replace("/","、")
        with open("C://Users//Zhang//Desktop//tmp//bdbk//"+word+".json","w+",encoding="utf-8") as f:
            json.dump(redict,f,ensure_ascii=False)
            
if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.maximize_window()

    word_list = []#读文件
    f = codecs.open("C://Users//Zhang//Desktop//new_word.txt","r",encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        if "【" not in line:
            word_list.append(line)

    index = 0
    for word in word_list:
        #
        #
        #
        #index 为当前开始位置 例如1500即从文件的第1500行开始
        if index > 24200:
            word = word.replace("\ufeff","")
            word = word.replace("\r\n","")
            url_list = []
            filename = []
            url = "https://baike.baidu.com/item/" + word
            browser.get(url)
            url_list = judge_element(browser,url,filename,word)
            flag = 0
            for u in url_list:
                browser.get(u)
                get_detail(browser,url,filename[flag],word)
                flag += 1
        index += 1
    browser.quit()
    print("ok")

