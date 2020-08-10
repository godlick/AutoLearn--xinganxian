# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
import json



if __name__ == "__main__":
	
    #打开浏览器进入新干线登陆网址
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  #设置不弹出浏览器界面
#   driver = webdriver.Chrome(options=option)
    driver = webdriver.Chrome()
    driver.get("https://puser.zjzwfw.gov.cn/sso/usp.do?acti\
		    on=ssoLogin&servicecode=xxxgx") #账号密码登陆的网址
    while(1):
        if(driver.current_url == "https://pro.learning.gov.cn/"):  
            cookies = driver.get_cookies()
            with open("cookies.txt", "w") as fp:
                json.dump(cookies, fp)
            driver.quit()
