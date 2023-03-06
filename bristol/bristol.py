import os
from os import kill
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pandas as pd
import numpy as np
import tqdm

# TODO 크롬 드라이버 경로 설정해두기
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome("C:/chromedriver", options=options)  #브라우저 켜기
driver.get('https://pubmed.ncbi.nlm.nih.gov/') # pubmed

# https://choihyuunmin.tistory.com/82

# 고급검색
toAdvance = driver.find_element(By.CSS_SELECTOR, 'a.search-input-link')
toAdvance.click()

# title과 abstract으로 설정
title_abstrac = driver.find_element(By.CSS_SELECTOR, 'select#field-selector')
title_abstrac.click()
opt = driver.find_element(By.CSS_SELECTOR, '#field-selector > option:nth-child(39)')
opt.click()

# Input Keywords
search = driver.find_element(By.CSS_SELECTOR, 'input#id_term')
search.click()

# TODO 찾고자 하시는 키워드를 아래와 같이 [Title/Abstract]가 포함된 형태로 입력하셔야 합니다.
search.send_keys('''(bristol stool scale[Title/Abstract]) AND ((gastrointestinal[Title/Abstract]) OR (disease[Title/Abstract]) OR (diagnosis[Title/Abstract]) OR
         (prediction[Title/Abstract]) OR 
         (clinical[Title/Abstract]) OR 
         (implication[Title/Abstract]))''')
search.send_keys(Keys.ENTER)


searchBtn = driver.find_element(By.CSS_SELECTOR, '#search-form > div > div > div.query-box-section-wrapper > div.button-wrapper > button')
searchBtn.click()

title_arr = []
author_arr = []
journal_arr = []
link_arr = []
abstract_arr = []

titles = driver.find_elements(By.CSS_SELECTOR, 'a.docsum-title')

cnt = 0

result = int(driver.find_element(By.CSS_SELECTOR, 'div.results-amount > span.value').text)

for _ in range(result):
    titles = driver.find_elements(By.CSS_SELECTOR, 'a.docsum-title')
    num = driver.find_element(By.CSS_SELECTOR, '#search-results > section > div.search-results-chunks > div > article:nth-child(2) > div.item-selector-wrap.selectors-and-actions.first-selector > label > span').text

    if len(titles) > 10:
        titles2 = driver.find_elements(By.CSS_SELECTOR, 'a.docsum-title')
        titles2[10].click()
        driver.back()
        
    elif len(titles) <= 10:
        for i in range(len(titles)):
            titles2 = driver.find_elements(By.CSS_SELECTOR, 'a.docsum-title')
            author_check = driver.find_elements(By.CSS_SELECTOR,'span.docsum-authors.full-authors')
            temp = author_check[i].text
            print(temp.count(','))
            if temp.count(',')>=100:
                continue
            else:
                titles2[i].click()
            #title
            title = driver.find_element(By.CSS_SELECTOR, 'h1.heading-title')
            title_arr.append(title.text)

            #authors
            authors = driver.find_elements(By.CSS_SELECTOR, '.inline-authors > .authors > .authors-list > span.authors-list-item > a.full-name')
            author_arr.append(authors[0].text)
            
            # journals
            journal = driver.find_element(By.CSS_SELECTOR, '#full-view-heading > div.article-citation > div > div > button') 
            journal_arr.append(journal.text)

            # abstract
            try:
                abstract = driver.find_element(By.CSS_SELECTOR, 'div.abstract-content')
            except:
                abstract = None
            else:
                abstract_arr.append(abstract.text)

            #link
            try:
                link = driver.find_elements(By.CSS_SELECTOR, 'a.id-link')
                href= link[-1].get_attribute('href')
            
            except IndexError:
                href = None
            link_arr.append(href)

            driver.back()
            cnt += 1
            
            if i == 9:
                ## Show More
                more = driver.find_element(By.CSS_SELECTOR, '#search-results > section > div.search-results-paginator.next-results-paginator.has-nav > button > span')
                more.click()
                time.sleep(1.2)
        print(f"Article Count: {cnt}, Proceeding rate: {round(cnt/int(result) * 100, 2)}%")
        if len(abstract_arr) == result:
            bristol_df = pd.DataFrame(np.c_[title_arr, journal_arr, author_arr, link_arr, abstract_arr], columns=['title','journal','authors','links','abstract'])
            bristol_df.to_csv('crawl_result.csv', encoding='utf8')
            print('Done!')
            break



