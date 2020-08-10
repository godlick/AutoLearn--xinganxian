# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
import json


#变量声明区域
num = 20	#弹窗接受次数
complate = 0  #完成学习标志 0：未完成 1：完成
course = [] #已学课程列表
Ctrue = 0
Credits = 0
CurrentStrc = '' #当前课程类别

def login():
		#完成登录
#	driver.find_element_by_id('loginname').send_keys("账号")
#	driver.find_element_by_id('loginpwd').send_keys("密码")
#	driver.find_element_by_id('submit').click()
#	time.sleep(2)

#	if(driver.title == "登录系统"):
#		print("login success!")
#		cookies = driver.get_cookies()
#		with open("cookies.txt", "w") as fp:
#			json.dump(cookies, fp)
#	else:
#		print("login false!")
#		time.sleep(20)
#		driver.quit()
		
#cookies 登陆
	driver.delete_all_cookies()
	with open("cookies.txt", "r") as fp:
		data = json.load(fp)
		cookiesNum = len(data)
		while(cookiesNum):
			cookies = data[cookiesNum - 1]
		#	print(cookies)
			driver.add_cookie(cookies)
			cookiesNum = cookiesNum - 1

	driver.refresh()
	doc = BeautifulSoup(driver.page_source, 'html.parser')
	success_L = doc.find_all(name='div',attrs={"class":"title"})
	success = ''.join(re.findall('[\u4e00-\u9fa5]',success_L[0].get_text()))
	if(success == "在线学习系统"):
		studentName = doc.find_all(name='p',attrs={"class":"name"})[0].string
		with open("任务进程.txt","a+") as f:
			f.write(studentName+'\n')
	else:
		print("登陆失败")
		with open("任务进程.txt","a+") as f:
			f.write("登陆失败"+'\n')
	
def handlcourse():
	
	##在线学习系统 or 学时管理系统
	#学时管理系统 https://pro.learning.gov.cn/study/ 
	driver.get("https://pro.learning.gov.cn/study/")
	article = driver.find_element_by_link_text("更多")
	article.click()
	time.sleep(0.5)
#	print(driver.page_source)
		#取出有几页
	doc = BeautifulSoup(driver.page_source, 'html.parser')
	span_list = doc.find_all(name='span',attrs={"class":"text"})
#	print(span_list)
	number = 0
	for span in span_list:
		#print(span.string)  #共X页
		ss = span.string.replace('共','')
		ss = ss.replace('页','')
		number = int(ss)
#	print(number)
	with open("新干线已学课程.txt","w") as f:
		f.write('')

	while(number):
		number = number - 1
		doc = BeautifulSoup(driver.page_source, 'html.parser')
#		print(doc)
		a_list = doc.find_all(name='tr',attrs={"class":"listTd"})
		for a in a_list :
		    for soccer in a:
			    if(soccer.string == '0.50'):
				    Credits = 0.5
				    with open("新干线已学课程.txt","a+") as f:
					    f.write('0.5   ')
			    if(soccer.string == '1.00'):
				    Credits = 1.0
				    with open("新干线已学课程.txt","a+") as f:
					    f.write('1.0   ')

		    a_title = a.find_all(name='a',attrs={"style":"text-align:left"})
		    for title in a_title:
			    ##判断课程类型
			    global ProCredits #专业学分
			    global OthCredits #其他学分
			    p =r'[[][\W\w]+[]]'
			    strc = re.findall(p, title.string)#strc[0] == '[专业课程]'
			    if(strc[0] == '[专业课程]'):
				    ProCredits += Credits
			    else:
				    OthCredits += Credits
			    
			    course.append(title["title"])
			    with open("新干线已学课程.txt","a+") as f:
				    f.write(strc[0])
				    f.write(title["title"] + '\n')

		    
		article = driver.find_element_by_link_text("下一页")
		article.click()
		time.sleep(0.5)

	
def newWinacp():
	wins1 = driver.window_handles
	driver.switch_to.window(wins1[-1])
#        print(driver.current_url)
	complate = 0
	while(1):
		result = EC.alert_is_present()(driver)    #检测是否有弹窗
		if result:
			print(driver.switch_to.alert.text)
	#		print(driver.title)
			global ProCredits
			global OthCredits
			ss = re.sub(r'\D', "",driver.switch_to.alert.text)
			if(CurrentStrc == "专业课程"):
				ProCredits += int(ss)/100
			else:
				OthCredits += int(ss)/100
			with open("任务进程.txt","a+") as f:
				f.write(driver.switch_to.alert.text+'\n')
			result2 = "您的学习时间已达到要求，获得学分:" in driver.switch_to.alert.text
			if result2:
				complate = 1
			time.sleep(1)
			driver.switch_to.alert.accept()
			with open("任务进程.txt","a+") as f:
				f.write("接受"+'\n')
			print("接受")
		if complate:
			complate = 0
			wins1 = driver.window_handles
			driver.close()
			driver.switch_to.window(wins1[1])
			print(driver.current_url)
			driver.close()
			driver.switch_to.window(wins1[0])
			print(driver.current_url)
			selectCourse()
		

def selectCourse():
	with open("任务进程.txt","a+") as f:
		f.write("已学专业课程学分："+str(ProCredits)+'\n')
		f.write("已学其他课程学分："+str(OthCredits)+'\n')
		f.write("当前课程类型："+CurrentStrc+'\n')
#	print(ProCredits)
#	print(OthCredits)
#	print(CurrentStrc)
	if(ProCredits > 60 and CurrentStrc == '专业课程'):
		if(OthCredits < 31):
			GoStudy(2)
		else:
			driver.quit()
	elif(OthCredits > 30):
		driver.quit()  
			
	doc = BeautifulSoup(driver.page_source, 'html.parser')
	li_list = doc.find_all(name='li',attrs={"class":"item-box c"})
	for li in li_list:
		global Ctrue
		Ctrue = 0
		a = li.find_all(name='a',attrs={"target":"_blank"})
		for aa in a:
			if(aa.string != None and aa.string != '[工学]' and aa.string != '[艺术学]'):
				for c in course:
					if(c.strip().find(aa.string) != -1):#代表存在
						Ctrue = 1
	      
				if(Ctrue == 0): #代表没有出现过
					Ctrue = 4
				#        with open("新干线已学课程.txt","a+") as f:
				#            f.write(aa.string+'\n')
					course.append(aa.string+'\n')
					print("正在学习..."+ aa.string)
					with open("任务进程.txt","a+") as f:
						f.write("正在学习..."+ aa.string+'\n')
					article = driver.find_element_by_link_text(aa.string)
					article.click()
				     
					wins1 = driver.window_handles
					driver.switch_to.window(wins1[-1])
					driver.find_element_by_xpath('/html/body/div/div[3]/table[2]/tbody/tr[2]/td/div/button[1]').click()
 #                                       driver.close()
					newWinacp()
					break
		if(Ctrue == 4):
			break
	if(Ctrue == 1):
		driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[4]/div/a[7]').click()
		time.sleep(0.1)
		selectCourse()

def GoStudy(j):
	##在线学习系统 or 学时管理系统
	#在线学习系统 https://pro.learning.gov.cn/
	driver.get("https://pro.learning.gov.cn/")
#	print(driver.page_source)
	driver.find_element_by_link_text("网络课程").click()
	time.sleep(0.5)
	driver.find_element_by_xpath('//*[@id="coursetype_chosen"]/a/div').click()
	time.sleep(0.1)
	global CurrentStrc
	if(j == 0):
		CurrentStrc = '专业课程'
		driver.find_element_by_xpath('//*[@id="coursetype_chosen"]/div/ul/li[2]').click()
	elif(j == 1):
		CurrentStrc = '行业公需'
		driver.find_element_by_xpath('//*[@id="coursetype_chosen"]/div/ul/li[3]').click()
	else:
		CurrentStrc = '一般公需'
		driver.find_element_by_xpath('//*[@id="coursetype_chosen"]/div/ul/li[4]').click()
	time.sleep(0.1)
	driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/button').click()
	time.sleep(0.1)
	####开始选课
	selectCourse()

if __name__ == "__main__":
	
	ProCredits = 0
	OthCredits = 0
	#打开浏览器进入新干线登陆网址
	option = webdriver.ChromeOptions()
	option.add_argument('headless')  #设置不弹出浏览器界面
	driver = webdriver.Chrome(options=option)
#	driver = webdriver.Chrome()
#	driver.get("https://puser.zjzwfw.gov.cn/sso/usp.do?acti\
#				on=ssoLogin&servicecode=xxxgx") #账号密码登陆的网址

	driver.get("https://pro.learning.gov.cn")#cookies登陆网址

	with open("任务进程.txt","w") as f:  ##清空一下进程文件信息
		f.write("")

	login()
	
	handlcourse()  ##进入学时管理取出已学课程
#	print(ProCredits)
#	print(OthCredits)
	GoStudy(0) #进入学习系统
#	print("1111")
	

	
#	while(1):
#		print(driver.current_url)
#		time.sleep(5)
'''		
		if(driver.current_url == "https://pro.learning.gov.cn/study/login.php?act=go"):
			#学时管理系统 https://pro.learning.gov.cn/study/ 
			#在线学习系统 https://pro.learning.gov.cn/
			option = webdriver.ChromeOptions()
			option.add_argument('headless')  #设置不弹出浏览器界面
			driver = webdriver.Chrome(options=option)
			driver.get("https://pro.learning.gov.cn/study/") 
			wins = driver.window_handles
			print(wins)
'''			
'''	
	while(num):
		result = EC.alert_is_present()(driver)  #检测是否有弹窗
		if result：
			#弹窗字符中存在以下字符串，说明已经完成学习
			result2 = "您的学习时间已达到要求，获得学分:" in driver.switch_to.alert.text
			if result2:
				complate = 1
			time.sleep(0.5)
			driver.switch_to.alert.accept()							  #点击弹窗的确定按钮
			num=num-1
			print(num)  #将剩余次数打印显示
			
		if complate:
			complate = 0  #将完成标志取消
			driver.close() #关闭当前页面
'''

