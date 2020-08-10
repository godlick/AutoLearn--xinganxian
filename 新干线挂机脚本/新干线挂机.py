# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()
driver.get("https://pro.learning.gov.cn/study/container.htm?courseid=37944&coursetitle=%E6%95%B0%E5%AD%97%E7%BB%8F%E6%B5%8E%E6%B2%BB%E7%90%86%E4%BD%93%E7%B3%BB%E7%9A%84%E5%BB%BA%E8%AE%BE%E4%B8%8E%E5%8F%91%E5%B1%95%EF%BC%88%E4%B8%8A%EF%BC%89&delay=1200000") #输入你要的网址
#driver.switch_to.frame("iframeResult")
click = 1
login = 0
complate = 0
newWindowsTitle = ""
num=15
course = []
Ctrue = 0

with open("新干线已学课程.txt", "r") as f: #打开文件
    course = f.readlines() #读取文件
#    print(course)

while(num):
#    print(driver.page_source)
#    time.sleep(10)
    result = EC.alert_is_present()(driver)    #检测是否有弹窗
   # print(EC)
    if result:								  #当有弹窗时
#        al = driver.switch_to_alert()		  #获取弹窗的位置
        print(driver.switch_to.alert.text)
        if driver.switch_to.alert.text == "请先登录！":
            login = 1  #准备登录标志
        result2 = "您的学习时间已达到要求，获得学分:" in driver.switch_to.alert.text
        if result2:
            complate = 1
#        print(driver)
        time.sleep(1)
        driver.switch_to.alert.accept()							  #点击弹窗的确定按钮
        num=num-1
        print(num)
        if login == 1:
#            print(driver.page_source) 
            login = 0
#    driver.minimize_window()
    if complate:
        complate = 0
        driver.close()
        driver.switch_to.window(wins1[0])
        doc = BeautifulSoup(driver.page_source, 'html.parser')
#        print(doc)
        li_list = doc.find_all(name='li',attrs={"class":"item-box c"})
        for li in li_list:
            Ctrue = 0
            a = li.find_all(name='a',attrs={"target":"_blank"})
            for aa in a:
                if(aa.string != None and aa.string != '[工学]'):
                    for c in course:
                   #     print(c)
                   #     print(aa.string)
                   #     print(c.strip().find(aa.string))
                        if(c.strip().find(aa.string) != -1):#代表存在
                            Ctrue = 1
                    if(Ctrue == 0): #代表没有出现过
                        Ctrue = 4
                        with open("新干线已学课程.txt","a+") as f:
                            f.write(aa.string+'\n')
                        course.append(aa.string+'\n')    
                        article = driver.find_element_by_link_text(aa.string)
                        article.click()
                        wins1 = driver.window_handles
                        newWindowsTitle = wins1[-1]
                        driver.switch_to.window(wins1[-1])
                        print(driver.current_url)
                        print(driver.page_source)
                        url = driver.current_url.replace('/course','/study')
                        url = url.replace('index.php?act=detail&','container.htm?')
                        url = url + "&coursetitle=" + aa.string + "&delay=1200000"
                        driver.get(url)
                   #     driver.minimize_window()
                        wins1 = driver.window_handles
                        newWindowsTitle = wins1[-1]
                        driver.switch_to.window(wins1[-1])
                        driver.minimize_window()
                        print(driver.current_url)
                        print(driver.title)
    #                    print(url)
    #                    print(article)
                        break
            if(Ctrue == 4):
                break
    wins1 = driver.window_handles
    if(newWindowsTitle != wins1[-1]):
        newWindowsTitle = wins1[-1]
        driver.switch_to.window(wins1[-1])
        print(driver.current_url)
        print(driver.title)
'''
    if(driver.current_url == "https://pro.learning.gov.cn/study/"):
#        print(driver.title)
        if driver.title == "学时管理系统":

            if(click == 1):
                click = 0
            
#            print(doc)
                article = driver.find_element_by_link_text("更多")
#                print(article)
                article.click()
#            print(driver.page_source)
                doc = BeautifulSoup(driver.page_source, 'html.parser')
#            print(doc)
                a_list = doc.find_all(name='tr',attrs={"class":"listTd"})
#            a_list = doc.find_all(name='div',attrs={"class":"tex02 tex"})
#            print(a_list)
                for a in a_list :
                    a = a.find_all(name='a',attrs={"style":"text-align:left"})
                    for title in a:
                        course.append(title['title'])
                        with open("新干线已学课程.txt","a+") as f:
                            f.write(title['title']+'\n')
                        #print(title['title'])
                article = driver.find_element_by_link_text("下一页")
                article.click()
                doc = BeautifulSoup(driver.page_source, 'html.parser')
                a_list = doc.find_all(name='tr',attrs={"class":"listTd"})
                for a in a_list :
                    a = a.find_all(name='a',attrs={"style":"text-align:left"})
                    for title in a:
                        course.append(title['title'])
                        with open("新干线已学课程.txt","a+") as f:
                            f.write(title['title']+'\n') #这句话自带文件关闭功能，不需要再写f.close()
#                print(course)
'''








#        print(driver.page_source) 
#    driver.switch_to.window(wins1[-1])
#    driver.minimize_window()
#    print(driver.current_url)
#    time.sleep(5)
#    print(driver.current_url)
#    driver.get(driver.current_url)
#    if(driver.current_url == "https://pro.learning.gov.cn/course/index.php"):
#    time.sleep(10)
#        if(click == 1):
#            print(driver.page_source)
        
#            article = driver.find_element_by_link_text("打造全国数字经济示范区，做强数字经济产业园（上）")
#            print(article)
#            article.click()
#            wins1 = driver.window_handles
#            driver.switch_to.window(wins1[-1])
#            print(driver.current_url)
#            article = driver.find_element_by_link_text("立即学习")
#            article.click()
#            wins1 = driver.window_handles
#            driver.switch_to.window(wins1[-1])
#            print(driver.current_url)
#            click = click - 1
