# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 18:32:50 2021

@author: COM
"""
#%% 설정
import os
os.chdir("D:\\MW\\jyh\\project\\프로젝트2")


import requests
from bs4 import BeautifulSoup

#%% 댓글 가져오기

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

driver = webdriver.Chrome("C:/chromedriver")  #브라우저 켜기

driver.get('https://www.naver.com/') # 페이지 이동

el = driver.find_element_by_css_selector('div.green_window > input#query')
el.click()
el.send_keys("아스트라제네카")
el.send_keys(Keys.ENTER)

#뉴스 메뉴 선택
news = driver.find_elements_by_css_selector("li.menu > a.tab")
news[1].click()

#더보기 메뉴
driver.implicitly_wait(1)
more = driver.find_element_by_css_selector("div.group_more > a#search_option_button")
more.click()

#언론사 선택
journal = driver.find_elements_by_css_selector("ul.option_menu > li.menu > a.m")
journal[4].click()

#조선
select_journal = driver.find_element_by_css_selector("div.snb_itembox > div.group_sort > div.scroll_area > div.select_item > div.item > div.rule_check > input#ca_1023")
select_journal.click()

#동아
select_journal = driver.find_element_by_css_selector("div.snb_itembox > div.group_sort > div.scroll_area > div.select_item > div.item > div.rule_check > input#ca_1020")
select_journal.click()

#중앙
select_journal = driver.find_element_by_css_selector("div.snb_itembox > div.group_sort > div.scroll_area > div.select_item > div.item > div.rule_check > input#ca_1025")
select_journal.click()

confirm = driver.find_element_by_css_selector("span.btn_inp_inner > button.type_default ")
confirm.click()

#기간설정
journal = driver.find_elements_by_css_selector("ul.option_menu > li.menu > a.m")
journal[1].click()
month1 = driver.find_elements_by_css_selector("div.group_choice > ul.lst_choice > li > a")
month1[3].click()

#키워드 추가
keyword = driver.find_elements_by_css_selector('li.menu > a.m')
keyword[6].click()
input_key = driver.find_element_by_css_selector("div.inp_op > input._input_exact_")
input_key.click()
input_key.send_keys("백신")

# 제외 키워드 추가
input_key = driver.find_element_by_css_selector("div.inp_op > input._input_exclude_")
input_key.click()
input_key.send_keys("LH, 부동산, 의협")
input_key.send_keys(Keys.ENTER)

nav_rpl1=[]
nav_rpl2 = []
astra = []
#%% 댓글 크롤링
import nltk
import konlpy
from konlpy.tag import Kkma 

# 페이지 반복
while True:
    next_btn = driver.find_element_by_css_selector("div.sc_page > a.btn_next")
    next_btn_check = next_btn.get_attribute("aria-disabled")
    to_nav_news = driver.find_elements_by_css_selector("div.news_area > div.news_info > div.info_group > a.info")
    # 뉴스 읽기
    for news in range(len(to_nav_news)):
        if news % 2 == 1:
            to_nav_news[news].click()
            driver.switch_to_window(driver.window_handles[-1])
            driver.implicitly_wait(0.5)
            #댓글버튼 클릭
            try:
                rpl_btn = driver.find_element_by_css_selector("div.article_btns_left > a.pi_btn_count")
                rpl_btn
            except Exception:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
            else:
                rpl_btn.click()
            driver.switch_to_window(driver.window_handles[-1])
            while True:
                try:
                    rpl_more = driver.find_element_by_css_selector("div.u_cbox_paginate")
                    WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_paginate')))
                    rpl_more.click()
                except Exception :
                    astra= driver.find_elements_by_css_selector('div.u_cbox_area > div.u_cbox_text_wrap > span.u_cbox_contents')
                    for i in rpls:
                        nav_rpl2.append(i.text)
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    break
    if next_btn_check == 'true':
        break
    else:
        next_btn.click()
     
#%% 기사
article_list=[]
while True:
    next_btn = driver.find_element_by_css_selector("div.sc_page > a.btn_next")
    next_btn_check = next_btn.get_attribute("aria-disabled")
    to_nav_news = driver.find_elements_by_css_selector("div.news_area > div.news_info > div.info_group > a.info")
    # 뉴스 읽기
    for news in range(len(to_nav_news)):
        if news % 2 == 1:
            to_nav_news[news].click()
            driver.switch_to_window(driver.window_handles[-1])
            driver.implicitly_wait(0.5)
            while True:
                content = driver.find_element_by_css_selector("div#articleBodyContents")
                article_list.append(content.text)
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                break
    if next_btn_check == 'true':
        break
    else:
        next_btn.click()

article_list
#%% 길이 확인
# len(cs_rpl)
# len(ja_rpl)
# len(da_rpl)
# cs_rpl2 = list(set(cs_rpl)) # 조선
# ja_rpl = list(set(ja_rpl)) # 중앙
# ja_rpl = list(set(da_rpl)) # 동아

# len(ja_rpl)
# len(cs_rpl)

len(rpl_list)



#%% 사용자 단어 추가
from ckonlpy.tag import Twitter
from konlpy.tag import Okt

okt = Okt()
okt.add_dictionary()

tw = Twitter()

from konlpy.tag import Twitter
tw2 = Twitter()
tw.nouns

tw.add_dictionary('아스트라제네카', 'Noun')
tw.add_dictionary('아스트라','Noun')
tw.add_dictionary('화이자','Noun')
tw.add_dictionary('모더나','Noun')
tw.add_dictionary('일베','Noun')
tw.add_dictionary('문재앙','Noun')
tw.add_dictionary('코로나','Noun')
tw.add_dictionary('코로나19','Noun')
tw.add_dictionary('재배포','Noun')
tw.add_dictionary('확진자','Noun')


#%% 기사 텍스트 마이닝
import nltk
import konlpy
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Okt
okt = Okt()
kkma = Kkma()
km = Komoran()
# 기사
len(article_list)
len(article_noun_list)
article_list[1]
article_noun_list=[]
for i in range(len(article_list)):
    noun = tw.nouns('%r'%article_list[i])
    noun_filter = filter(lambda x:len(x)>1 and x not in stop_w, noun)
    article_noun_list.append(list(noun_filter))
    
article_noun_list
rp_noun_list
#%% 댓글 텍스트 마이닝
## 명사 추출
rp_noun_list2=[]
from tqdm.notebook import tqdm
for i in range(len(nav_rpl2)):
    rp_noun = tw.nouns(nav_rpl2[i])
    rp_noun_f = filter(lambda x: len(x)>1 and x not in stop_w, rp_noun)
    rp_noun_list2.append(list(rp_noun_f))
len(rp_noun_list2)

from itertools import chain
rp_text=' '.join(list(chain(*rp_noun_list)))
art_text = ' '.join(list(chain(*article_noun_list)))
len(rp_text)
len(art_text)

rp_noun_list

with open('네이버 보수언론 댓글.txt','w', encoding='cp949') as f:
    f.write(rp_text)

import csv
rp_nouns = pd.DataFrame(rp_noun_list)
rp_nouns.to_csv('네이버 보수언론 댓글 리스트.csv',encoding='cp949')

with open('D:\\MW\\jyh\\project\\프로젝트2\\댓글\\네이버보수언론댓글.csv','r',encoding='utf8')as f:
    a = csv.reader(f)
rp_noun_list = list(a)


#%% 불용어 사전 추가
from wordcloud import STOPWORDS
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
stop_w = set(['코로나', '면서','바이러스','코로나바이러스', '조선일보','조선','일보', '중앙','중앙일보','기저','질환','사람','기저 질환','기저질환', '병원','요양','요양 병원','요양병원', '접종','구독', '배포','무단','금지','기자','오늘','내일','다음', '기저','질환','기저질환','기저 질환','접종','까지','이상','뉴스','재배','재배포','신문'])

#%% 워드클라우드
import matplotlib.pyplot as plt
from wordcloud import WordCloud as wc

wordc.generate(text)
plt.imshow(wordc)

import numpy as np
from PIL import Image
import os
os.chdir("D:\\MW\\jyh\\project\\프로젝트2")
img = Image.open('covid19.png').convert('RGBA')
mask = Image.new('RGB',img.size, (255,255,255))
mask.paste(img,img)
mask_ar = np.array(img)


# 장
import numpy as np
from PIL import Image
img=Image.open("covid19.jpg").convert("RGBA")
mask_ar=np.array(img)

def make_colors(word, font_size, position, orientation, random_state, **kwagrs):
     color = 'hsl(0,100%%,%d%%)'%np.random.randint(50,100)
     return color

wordcloud = wc(background_color='black', max_words=1000,
               stopwords= stop_w,
               font_path="C:/Windows/Fonts/malgun.ttf",
               random_state=42,
               mask=mask_ar)

import matplotlib.pyplot as plt
from wordcloud import ImageColorGenerator
wordc = wordcloud.generate(art_text)
wordc.recolor(color_func=make_colors)
plt.figure(figsize=(15,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
wordcloud.to_file('네이버_보수언론_기사최종.png')


#%% 단어 빈도수 확인하는 그래프
import nltk
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.figure(figsize=(12,6))
font_name = fm.FontProperties(fname = "C:/Windows/Fonts/H2GTRM.TTF").get_name()
plt.rc('font',family = font_name)
nltk.Text(rp_text).plot(10)
rp_text
#%% nltk 변환: str 필요

from nltk import Text
from nltk.tokenize import RegexpTokenizer
import matplotlib.font_manager as fm
from nltk.tag import pos_tag
font_name = fm.FontProperties(fname="C:/Windows/Fonts/H2GTRM.TTF").get_name()
plt.rc("font",family=font_name)
ret = RegexpTokenizer("[\w]+")
rp = nltk.Text(ret.tokenize(rp_text))
art = nltk.Text(ret.tokenize(art_text))
rp
rp.plot(15)
rp_text = rp_text.replace('기저',"")
art.plot(15)

#%% 단어 빈도 그래프 그리기
rp.plot(20)
art.plot(20)
art_rank = art.vocab()
rp_rank = rp.vocab()

import pandas as pd
pd.DataFrame(rp_rank)
rp_rank
art_rank
#%% 단어 선별
from nltk import Text
from nltk import FreqDist
FreqDist(rp).most_common(15)
FreqDist(art).most_common(15)

list(nltk.Text(ret.tokenize(" ".join(article_noun_list[1]))).vocab())
list(nltk.Text(ret.tokenize(" ".join(article_noun_list[1]))).vocab())[:15]
nltk.Text(ret.tokenize(" ".join(article_noun_list[1]))).vocab()
list(nltk.Text(ret.tokenize(" ".join(article_noun_list[0]))).vocab())[:10]

art_words_list=[]
for i in range(len(article_noun_list)):
    x=list(nltk.Text(ret.tokenize(" ".join(article_noun_list[i]))).vocab())[:20]
    art_words_list.append(x)

rp_words_list=[]
for i in range(len(rp_noun_list)):
    x=list(nltk.Text(ret.tokenize(" ".join(rp_noun_list[i]))).vocab())[:20]
    rp_words_list.append(x)
    

#%% 연관분석
from apyori import apriori
import pandas as pd

rules_rpl = apriori(rp_noun_list, min_support=0.005, min_confidence=0.005)
rules_article = apriori(art_words_list, min_support=0.05, min_confidence=0.05)
results_rpl = list(rules_rpl)
results_article = list(rules_article)
results_rpl
results_article
results[0]


#%%연관규칙 조회
print("lhs => rhs \t support \t confidence \t lift")
result_df = pd.DataFrame(None, columns = ['lhs','rhs','support', 'confidence','lift'])
index=0
for row in results_article:
    support = row[1]
    ordered_stat = row[2]
    for ordered_item in ordered_stat:
        lhs = " ".join(x.strip() for x in ordered_item[0])
        rhs = ' '.join(x.strip() for x in ordered_item[1])
        confidence = ordered_item[2]
        lift = ordered_item[3]
        result_df.loc[index]=[lhs,rhs,support,confidence,lift]
        index += 1
        
        
result_df.loc[result_df.lhs!=""].sort_values(by=['lift'], ascending=False)
result_df.loc[result_df.lhs!=""].sort_values(by=['support'], ascending=False)
result_df.to_csv('연관분석_보수_기사_ver1.csv',encoding='cp949')


result_df = pd.DataFrame(None, columns = ['lhs','rhs','support', 'confidence','lift'])
index=0
for row in results_rpl:
    support = row[1]
    ordered_stat = row[2]
    for ordered_item in ordered_stat:
        lhs = " ".join(x.strip() for x in ordered_item[0])
        rhs = ' '.join(x.strip() for x in ordered_item[1])
        confidence = ordered_item[2]
        lift = ordered_item[3]
        result_df.loc[index]=[lhs,rhs,support,confidence,lift]
        index += 1
        
result_df.loc[result_df.lhs!=""].sort_values(by=['lift'], ascending=False)
result_df.loc[result_df.lhs!=""].sort_values(by=['support'], ascending=False)
result_df.to_csv('연관분석_진보_댓글_ver2.csv',encoding='cp949')

result_df.loc[result_df['lhs']].sort_values(by=['lift'], ascending = False)



#%% 연관분석 그래프로 보여주기
result_df.columns
import plotnine as pn
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.figure(figsize=(12,6))
font_name = fm.FontProperties(fname = "C:/Windows/Fonts/H2GTRM.TTF").get_name()
plt.rc('font',family = font_name)

result_df['logic'] = 


(ggplot(data=result_df.loc[result_df.lhs!=""].loc[result_df.lift>4], mapping=aes(x='reorder(lhs,-lift)', y='lift'))+ geom_col())

#%% 파일로 변환

df = pd.DataFrame(rp_noun_list)
df.to_csv('네이버보수언론댓글.csv',index=False, encoding='cp949')
#list to csv
df=pd.DataFrame(rpl_n_list_cs)
df.to_csv("조선일보댓글.csv", index=False, encoding="cp949")

df2 = pd.DataFrame(rpl_n_list_ja)
df2.to_csv('중앙일보댓글.csv', index=False, encoding='cp949')

df2.loc[df2.contain ]
df2.iloc[0,:].str.contains('백신')

import csv

    
with open('보수언론 댓글.txt', 'r', encoding='cp949') as f:
    rp_text = f.read()
type(rp_text)

rp_text
    #%% 시각화
import networkx as nx
result = list(apriori(rp_noun_list, min_support=0.005))
df= pd.DataFrame(result)
df.columns
df['length']= df['items'].apply(lambda x:len(x))
df = df[(df['length'] ==2)].sort_values(by='support', ascending=False)
df

G=nx.Graph()
ar= df['items']
G.add_edges_from(ar)

pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize -min(nsize)) / (max(nsize)-min(nsize))

pos = nx.circular_layout(G)

plt.figure(figsize=(15,10))
plt.axis('off')
nx.draw_networkx(G, font_family=font_name,
                 font_size=16,
                 pos=pos, node_color = list(pr.values()), node_size=nsize,
                 alpha=0.7, edge_color='.5', cmap=plt.cm.YlGn)