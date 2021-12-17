import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
from os import kill
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np
import logging
from subwindow import SubWindow

form_class = uic.loadUiType('crawlingbot.ui')[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Crawling Bot')

        self.addKeywordBtn.clicked.connect(self.addKeyword)
        self.search.clicked.connect(self.intialize)
        self.progressBar.setValue(0)

    def addKeyword(self):
        # print(self.keywordInput.text())
        if self.queryBox.toPlainText() == "":
            a = self.keywordInput.text() + "["+self.keywordRange.currentText() +"]"
            self.queryBox.appendPlainText(a)
        else:
            if self.radioBtnAnd.isChecked():
                a = self.radioBtnAnd.text() + " " +self.keywordInput.text() + "["+self.keywordRange.currentText() +"]" 
                self.queryBox.appendPlainText(a)
            else:
                a = self.radioBtnOr.text() + " "+self.keywordInput.text() + "["+self.keywordRange.currentText() +"]" 
                self.queryBox.appendPlainText(a)
        self.keywordInput.clear()

    def printValue(self):
        pass

    
    def article_search(self, key):
        driver = webdriver.Chrome("C:/chromedriver")  #브라우저 켜기
        driver.get('https://pubmed.ncbi.nlm.nih.gov/') 
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
        search.send_keys(key)
        search.send_keys(Keys.ENTER)

        searchBtn = driver.find_element_by_css_selector('#search-form > div > div > div.query-box-section-wrapper > div.button-wrapper > button')
        searchBtn.click()

        title_arr = []
        year_arr = []
        author_arr = []
        journal_arr = []
        link_arr = []
        abstract_arr = []

        titles = driver.find_elements_by_css_selector('a.docsum-title')
        cnt = 0
        resultNum = driver.find_element_by_css_selector('div.results-amount > span.value').text
        if "," in resultNum:
            result = int(resultNum.replace(",",""))
        else:
            result = int(resultNum)

        # print("progressbar:",self.progressBar.value())
        self.progressBar.setRange(0,100)

        for i in range(result):
            titles = driver.find_elements_by_css_selector('a.docsum-title')
            num = driver.find_element_by_css_selector('#search-results > section > div.search-results-chunks > div > article:nth-child(2) > div.item-selector-wrap.selectors-and-actions.first-selector > label > span').text
            self.progressBar.setValue(round(i/result*100,1))
            # print("lenght: ", len(titles))
            # print("num:", num)
            if len(titles) > 10:
                titles2 = driver.find_elements_by_css_selector('a.docsum-title')
                titles2[10].click()
                driver.back()
            elif len(titles) <= 10:
                for i in range(len(titles)):
                    time.sleep(1)
                    titles2 = driver.find_elements_by_css_selector('a.docsum-title')
                    titles2[i].click()

                    #title
                    title = driver.find_element_by_css_selector('h1.heading-title')
                    title_arr.append(title.text)

                    # year
                    try:
                        year = driver.find_element_by_css_selector('#full-view-heading > div.article-citation > div.article-source > span.cit')
                        year_arr.append(year.text)
                    except:
                        year = ""
                        year_arr.append(year)

                    #authors
                    try:
                        authors = driver.find_element_by_css_selector('#full-view-heading > div.inline-authors > div > div > span:nth-child(1) > a')
                        author_arr.append(authors.text)
                    except:
                        author = ""
                        author_arr.append(author)
                    # journals
                    try:
                        journal = driver.find_element_by_css_selector('#full-view-heading > div.article-citation > div > div > button') 
                        journal_arr.append(journal.text)
                    except:
                        journal = ""
                        journal_arr.append(journal)
                    # abstract
                    try:
                        abstract = driver.find_element_by_css_selector('div.abstract-content')
                        abstract_arr.append(abstract.text)
                    except:
                        abstract = ""
                        abstract_arr.append(abstract)

                    #link
                    try:
                        link = driver.find_elements_by_css_selector('a.id-link')
                        href= link[-1].get_attribute('href')
                    
                    except IndexError:
                        href = None
                    link_arr.append(href)

                    driver.back()
                    cnt += 1
                    
                    if i == 9:
                        ## Show More
                        more = driver.find_element_by_css_selector('#search-results > section > div.search-results-paginator.next-results-paginator.has-nav > button > span')
                        more.click()
                        time.sleep(1.2)
                print(f"Article Count: {cnt}, Proceeding rate: {round(cnt/int(result) * 100, 2)}%")
            if len(title_arr) == result:
                df = pd.DataFrame(np.c_[title_arr, year_arr, journal_arr, author_arr, link_arr, abstract_arr], columns=['title','year', 'journal','authors','links','abstract'])
                # df.to_csv(outfile, encoding='utf8')
                
                return "done"

    def intialize(self):
        a= self.queryBox.toPlainText()
        b=" ".join(a.split("\n"))
        x= self.article_search(b)
        win = SubWindow()
        r = win.showModal()

        if x == 'done':
            msg = QMessageBox()
            msg.setWindowTitle("CrawlingBot")
            msg.setText('Crawling이 완료되었습니다!')
            msg.setStandardButtons(QMessageBox.Ok)
            result = msg.exec_()
            if result == QMessageBox.Ok:
                pass        
            self.queryBox.clear()


   
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()