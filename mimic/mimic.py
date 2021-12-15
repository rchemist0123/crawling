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


driver = webdriver.Chrome("C:/chromedriver")  #브라우저 켜기

driver.get('https://pubmed.ncbi.nlm.nih.gov/') # 페이지 이동

# Advanced Search -----------------------------------
toAdvance = driver.find_element_by_css_selector('a.search-input-link')
toAdvance.click()

# title과 abstract으로 설정
title_abstrac = driver.find_element_by_css_selector('select#field-selector')
title_abstrac.click()
opt = driver.find_element_by_css_selector('#field-selector > option:nth-child(39)')
opt.click()

# Input Keywords
search = driver.find_element_by_css_selector('input#id_term')
search.click()
search.send_keys('mimic-iii')
search.send_keys(Keys.ENTER)

option = driver.find_element_by_css_selector('button#add-arrow-button')
option.click()

options = driver.find_elements_by_css_selector('a.boolean-selector-link')
options[1].click()

search.click()
search.send_keys('mimic-iv')
search.send_keys(Keys.ENTER)

searchBtn = driver.find_element_by_css_selector('#search-form > div > div > div.query-box-section-wrapper > div.button-wrapper > button')
searchBtn.click()

# title, Data, Year, Author, Journal, Link

title_arr = []
authors_arr = []
journal_arr = []
links = []
years = []


# title
titles = driver.find_elements_by_css_selector('a.docsum-title')

# authors
authors = driver.find_elements_by_css_selector('div.docsum_citation > span.short-authors')
authors_arr.append(authors)



# Article Information
while True:
    titles = driver.find_elements_by_css_selector('a.docsum-title')
    num = driver.find_element_by_css_selector('#search-results > section > div.search-results-chunks > div > article:nth-child(2) > div.item-selector-wrap.selectors-and-actions.first-selector > label > span').text
    print("lenght: ", len(titles))
    print("num:", num)
    if len(titles) == 10:
        print('case1')
        for i in range(len(titles)):
            titles2 = driver.find_elements_by_css_selector('a.docsum-title')
            titles2[i].click()
            title_arr.append(titles2)

            # journals
            journal = driver.find_element_by_css_selector('#full-view-heading > div.article-citation > div > div > button') 
            journal_arr.append(journal.text)

            # year
            year = driver.find_element_by_css_selector('span.cit')
            years.append(year.text[0])

            #link
            try:
                link = driver.find_element_by_css_selector('#full-view-identifiers > li:nth-child(3) > span > a')
            except:
                link = driver.find_element_by_css_selector('#full-view-identifiers > li:nth-child(2) > span > a')
            links.append(link.get_attribute('href'))
                
            driver.back()
            if i==9:
                more = driver.find_element_by_css_selector('#search-results > section > div.search-results-paginator.next-results-paginator.has-nav > button > span')
                more.click()
                time.sleep(1)
    ## more을 눌러서 20이 된 경우
    elif len(titles) != 10:
        print('case11')
        titles2 = driver.find_elements_by_css_selector('a.docsum-title')
        titles2[10].click()
        title_arr.append(titles2)

        # journals
        journal = driver.find_element_by_css_selector('#full-view-heading > div.article-citation > div > div > button') 
        journal_arr.append(journal.text)

        # year
        year = driver.find_element_by_css_selector('span.cit')
        years.append(year.text[0])

        #link
        try:
            link = driver.find_element_by_css_selector('#full-view-identifiers > li:nth-child(3) > span > a')
        except:
            link = driver.find_element_by_css_selector('#full-view-identifiers > li:nth-child(2) > span > a')
        links.append(link.get_attribute('href'))
        driver.back()

    # 뒤돌아왔지만 1이 아닌 경우 즉 11 이상인 경우
    elif num != 1:
        print('case3')
        for i in range(1,len(titles)):
            titles2 = driver.find_elements_by_css_selector('a.docsum-title')
            titles2[i].click()
            title_arr.append(titles2)

            # journals
            journal = driver.find_element_by_css_selector('#full-view-heading > div.article-citation > div > div > button') 
            journal_arr.append(journal.text)

            # year
            year = driver.find_element_by_css_selector('span.cit')
            years.append(year.text[0])

            #link
            try:
                link = driver.find_element_by_css_selector('#full-view-identifiers > li:nth-child(3) > span > a')
            except:
                link = driver.find_element_by_css_selector('#full-view-identifiers > li:nth-child(2) > span > a')
            links.append(link.get_attribute('href'))
                
            driver.back()
            if i==9:
                more = driver.find_element_by_css_selector('#search-results > section > div.search-results-paginator.next-results-paginator.has-nav > button > span')
                more.click()
                time.sleep(1)
    else:
        break


x= pd.DataFrame()

    

    



    



