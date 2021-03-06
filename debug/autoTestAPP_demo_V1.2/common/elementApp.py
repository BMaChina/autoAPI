# coding:utf-8
from appium import webdriver
import time, os
from common import readexcel as reader, writeexcel as writer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from common.Log import MyLog as Log
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
from conf.conf import dataDir,reportDir,pageDir,imageDir
from conf import conf


"""
实现功能
V1.0
1.定位元素
2.操作，click,clear,input
3.其他操作
4.截图
5.失败重试3次

v：1.1
1.app定位元素，批量
2.assertequals,单个元素校验
3.assertequals_all，多个元素校验
4.调用模块封装go_func()
5.tanchuang(),id
6.存在就操作，is_exists()
7.assertin,单个存在，多个存在
8.assertin_all,单个存在，多个存在
9.backs,多次返回
10.多次滑动,swiptest("right",num)
11.

v1.2
1.随机点击taprandom,不能是边界值
2.坐标点击tappoint（x,y)
3.获取当前activity,get_package()
4.根据source判断,source_assert
5.校验notequal,notin
6.批量校验notequal,notin


"""

# 保存图片
resultfile = os.path.join(reportDir, 'screenshot/screenshot_')

number = 0  # 保存图片序号用

# 保存元素
elements = {}
saveelements={}
saveelements_array={}

# 保存上一个操作的元素定位
e = ""

# 保存值
saveValue = {}
# url
url = "http://localhost:4723/wd/hub"
timeout = 30
driver = ""

#保存定位元素值，如x=500,@x1
saveJson={}





#log
#log = Log.get_log()
#logger = log.get_logger()
#

# 设备参数
desired_caps = {
    'platformName': 'Android',
    'deviceName': '722347d6',  # 6EB0217518004226  #722347d6
    'platformVersion': '6.0',
    # 'app': PATH(r'E:\download\385.apk'), #安装目录
    'appPackage': 'com.ishugui',
    'appActivity': 'com.dzbook.activity.LogoActivity',
    #'unicodeKeyboard': False,    #使用unicode编码方式发送字符串
    #'resetKeyboard': False,      #隐藏键盘
    #'noReset':False,         # 在会话前是否重置app状态。默认是false
    #'fullReset':'true',
    # 'autoLaunch'：'false',     #Appium是否要自动启动或安装app，默认true
    'newCommandTimeout':1800,    #设置未接收到新命令的超时时间，默认60s,
    'automationName': 'UiAutomator2',
    #'dontStopAppOnReset': True,   # 不关闭应用
    'autoGrantPermissions': True,  # 自动获取权限
}

# 写入结果
def wirte_result(result, value):
    if reader.rr>0:
        writer.write(reader.rr - 1, 7, result)
        writer.write(reader.rr - 1, 8, value)
        #log
        #logger.info(result+value)
    
# 配置设备
def update_capability(key,value):
    global desired_caps
    
    if key == 'newCommandTimeout':
        value = int(value)
    try:
        desired_caps[key] = value
        #print(desired_caps["appPackage"],type(desired_caps["appPackage"]))        
        #取获取的包名
        if desired_caps["appPackage"]=="":
            print('包名为空时，取配置-------------------',conf.appPackage)                
            desired_caps["appPackage"]= conf.appPackage         

        if  desired_caps["appActivity"]=="":
            print('启动页为空时，取配置-------------------',conf.appActivity)
            desired_caps["appActivity"]=conf.appActivity

        # 写入
        #wirte_result('PASS', value)

    except Exception as err:
        print(err)
        #err_run(err,update_capability,key,value)

# 启动设备
def start(adddress, t):
    global url, timeout, driver
    url = adddress
    timeout = int(t)
    try:
        driver = webdriver.Remote(url, desired_caps)
        driver.implicitly_wait(timeout)

        # 写入
        wirte_result('PASS', "设备已经启动,wait%d" % timeout)
    except Exception as err:
        print('启动失败了，错误', err)
        print('请检查是否启动appium')
        rerun(start,adddress, t)


# 定位元素：index,取一组中[] name保存值,单个元素
def get_element(method, element, index="", name="", casename=""):
    global driver
    global saveelements
    global e
    global number

    print('定位---%s------%s-----' % (method, element))
    try:
        if method == "id":
            e = driver.find_element_by_id(element)
        elif method == "class":
            e = driver.find_element_by_class_name(element)

        elif method == "css":
            e = driver.find_element_by_css_selector(element)

        elif method == "xpath":
            e = driver.find_element_by_xpath(element)
        #text    
        elif method == "name":
            e = driver.find_element_by_name(element)

        elif method == "linktext":
            e = driver.find_element_by_link_text(element)

        elif method == "partiallinktext":
            e = driver.find_element_by_partial_link_text(element)
 
        elif method=="content-desc":
            e = driver.find_element_by_accessibility_id(element)
       
        elif method == "text":
            new = 'new UiSelector().text(\"' + element + '\")'
            e = driver.find_element_by_android_uiautomator(new)

        elif method == "textContains":
            new = 'new UiSelector().textContains(\"' + element + '\")'
            e = driver.find_element_by_android_uiautomator(new)

        elif method == "textStartsWith":
            new = 'new UiSelector().textStartsWith(\"' + element + '\")'
            e = driver.find_element_by_android_uiautomator(new)         

        elif method == "textMatches":
            new = 'new UiSelector().textMatches(\"' + element + '\")'
            e = driver.find_element_by_android_uiautomator(new)  

        elif method == "resourceId":
            new = 'new UiSelector().resourceId(\"' + element + '\")'
            e = driver.find_element_by_android_uiautomator(new) 

        elif method == "resourceIdMatches":
            new = 'new UiSelector().resourceIdMatches(\"' + element + '\")'
            e = driver.find_element_by_android_uiautomator(new) 

        print('定位元素--------------------------')
        print('e:', e)
        # 写入信息
        re = "PASS"
        value = element

        if name != "":
            saveelements[name] = e

    # 异常
    except Exception as err:
        print("定位报错了:", err)
        number = number + 1
        get_screenshot(resultfile, "_error_%s_%d.png" % (casename, number))
        # 写入信息
        re = "FAIL"
        value = str(err)
        #重试
        rerun(get_element,method,element,index,name,casename)

    # 写入
    wirte_result(re, value)

#定位一批元素,同单个元素定位，
def get_elements(method, element, index="", name="", casename=""):
    global driver
    global saveelements_array
    global e
    global number

    print('定位---%s------%s-----' % (method, element))
    try:
        if method == "id":
            e = driver.find_elements_by_id(element)
        elif method == "class":
            e = driver.find_elements_by_class_name(element)

        elif method == "css":
            e = driver.find_elements_by_css_selector(element)

        elif method == "xpath":
            e = driver.find_elements_by_xpath(element)
        #text    
        elif method == "name":
            e = driver.find_elements_by_name(element)

        elif method == "linktext":
            e = driver.find_elements_by_link_text(element)

        elif method == "partiallinktext":
            e = driver.find_elements_by_partial_link_text(element)
 
        elif method=="content-desc":
            e = driver.find_elements_by_accessibility_id(element)
       
        elif method == "text":
            new = 'new UiSelector().text(\"' + element + '\")'
            e = driver.find_elements_by_android_uiautomator(new)

        elif method == "textContains":
            new = 'new UiSelector().textContains(\"' + element + '\")'
            e = driver.find_elements_by_android_uiautomator(new)

        elif method == "textStartsWith":
            new = 'new UiSelector().textStartsWith(\"' + element + '\")'
            e = driver.find_elements_by_android_uiautomator(new)         

        elif method == "textMatches":
            new = 'new UiSelector().textMatches(\"' + element + '\")'
            e = driver.find_elements_by_android_uiautomator(new)  

        elif method == "resourceId":
            new = 'new UiSelector().resourceId(\"' + element + '\")'
            e = driver.find_elements_by_android_uiautomator(new) 

        elif method == "resourceIdMatches":
            new = 'new UiSelector().resourceIdMatches(\"' + element + '\")'
            e = driver.find_elements_by_android_uiautomator(new) 

        print('定位元素--------------------------')
        print('e:', e)
        # 写入信息
        re = "PASS"
        value = element

        if name != "":
            saveelements_array[name] = e

    # 异常
    except Exception as err:
        print("定位报错了:", err)
        number = number + 1
        get_screenshot(resultfile, "_error_%s_%d.png" % (casename, number))
        # 写入信息
        re = "FAIL"
        value = str(err)
        #重试
        rerun(get_element,method,element,index,name,casename)

    # 写入
    wirte_result(re, value)

# 操作集合
def clicks(act, element, value="", name="", casename=""):
    global saveelements, driver
    global e
    global number
    print('正在执行%s操作--------------------------' % act)
    print(element)

    # 不为空，提取保存的值；为空点击上一个定位元素
    #调取元素
    el=get_element_of(element)

    try:
        # 根据act执行不同到操作
        if act == "click":
            result = el.click()
        elif act == "clear":
            result = el.clear()
        elif act == "input":

            value=str(value)            
            result= el.send_keys(value)
            print('正在输入内容',value)
            
        # name保存操作
        if name != "":
            saveValue[name] = result
        # 写入值
        re = "PASS"
        value = "执行成功"

    # 异常
    except Exception as err:
        print("报错了:", err)
        number = number + 1
        get_screenshot(resultfile, "_error_%s_%d.png" % (casename, number))

        re = "FAIL"
        value = str(err)
        #重试
        rerun(clicks,act,element,value, name,casename)
    # 写入
    wirte_result(re, value)

# 定位元素，不为空取保存值，为空取上一个定位元素；
# 引用，get_value,clicks
def get_element_of(element):
    global saveelements, driver
    global e
    # print(element)
    # 不为空，提取保存的值；为空点击上一个定
    if element != "":
        el = saveelements[element]
    else:
        el = e
    print('操作的元素是：%s-------------------------' % el)	   
    return el
#---------------------------------------------------------------
# quit
def quit():
    global driver
    try:
        driver.quit()
        # 写入
        wirte_result("PASS", "操作成功")
    except Exception as err:
        #调用方法
        err_run(err,quit)

# back,点击返回键
def back():
    global driver
    try:
        driver.back()   
        # 写入
        wirte_result("PASS", "操作成功")
    except Exception as err:
        #调用方法
        err_run(err,back)

# back,多次点击
def backs(number):
    global driver
    try:
        n=0
        for i  in range(int(number)):
            driver.back() 
            n = n+1
     
        if n==int(number):
                # 写入
            wirte_result("PASS", "操作成功")
        else:
                # 写入
                wirte_result("FAIL", "操作失败")       
  
    except Exception as err:
        #调用方法
        err_run(err,back)

# sleep
def sleep(t,*args,**kwargs):
    global driver
    tt = int(t)
    try:
        time.sleep(tt)
        # 写入
        value = "等待%s秒" % tt
        wirte_result("PASS", value)

    except Exception as err:
        #调用方法
        err_run(err,sleep)

# 保存图片到指定文件夹
def get_screenshot(filepath, file):
    global driver
    filename = filepath + file
    print('正在保存图片', filename)
    try:
        driver.get_screenshot_as_file(filename)
        # 写入
        wirte_result("PASS",file)

    except Exception as err:
        #调用方法
        err_run(err,get_screenshot,filepath,file)
        
#校验属性值
attributes=["resourceId","className","text","name","checkable","checked","clickable","enabled","focusable","focused","scrollable","selected","bounds"]
alls=["text","tag_name","size","loaction"]
#定位元素e获取属性，元素不为空取值，为空取上一次操作
def get_value(name,element):
	global alls,attributes
	global driver
	print('正在取值----------------------------------------------------------',name,element)
	#取定位元素属性
	el=get_element_of(element)
	print(el)

	if name in attributes:
		t=el.get_attribute(name)
		print(t)

	elif name in alls:
		if name=="text":
			t=el.text
		elif name=="tag_name":
			t=el.tag_name
		elif name=="size":
			t=el.size
		elif name=="loaction":
			t=el.location
		print(t)
	else:
		print("输入未找到：",name)
		t="FAIL"
	return t
'''
#assert,name校验结果，value取值,e定位元素
def assert_equals(name,value,el):
	global driver
	print('正在进行校验-----------------------------------------------------------------')
	print('本次校验的期望结果是：%s,取值:%s'%(name,value))
	#调用取值
	values=get_value(value,el)

	#进行判断
	if name==values:
		print('校验正确,校验结果：%s'%name)
		re="PASS"
		result=name
		
	else:
		print('校验不正确，要校验的值为%s,取值:%s'%(value,values))
		re="FAIL"
		result="校验的值:"+values

	# 写入
	wirte_result(re,result)
'''
#-------------------------------
#assert 统一调用
#assert,name校验结果，value取值,e定位元素
#根据不同方法调用不同判断
def assert_method(method,name,value,el):
    global driver
    print('正在进行校验-----------------------------------------------------------------')
    print('本次校验%s,期望结果是：%s,取值:%s'%(method,name,value))
    #调用取值
    values=get_value(value,el)
    if method=="equal":
        #进行判断
        if name==values:
            print('校验正确,校验结果：%s'%name)
            re="PASS"
            result=method+"，校验的值:"+name+",取值："+values
        else:
            print('校验不正确，要校验的值为%s,取值:%s'%(value,values))
            re="FAIL"
            result=method+"，校验的值:"+name+",取值是："+values
   
    elif method=="in":
        #进行判断
        if name in values:
            print('校验正确,校验结果：%s'%name)
            re="PASS"
            result = method + "，校验的值:" + name + ",取值：" + values
        else:
            print('校验不正确，要校验的值为%s,取值:%s' % (value, values))
            re = "FAIL"
            result = method + "，校验的值:" + name + ",取值是：" + values
 
    elif method=="notequal":
        #进行判断
        if name != values:
            print('校验正确,校验结果：%s'%name)
            re="PASS"
            result = method + "，校验的值:" + name + ",取值：" + values
        else:
            print('校验不正确，要校验的值为%s,取值:%s' % (value, values))
            re = "FAIL"
            result = method + "，校验的值:" + name + ",取值是：" + values
   
    elif method=="notin":
        #进行判断
        if name not in  values:
            print('校验正确,校验结果：%s'%name)
            re="PASS"
            result = method + "，校验的值:" + name + ",取值：" + values
        else:
            print('校验不正确，要校验的值为%s,取值:%s' % (value, values))
            re = "FAIL"
            result = method + "，校验的值:" + name + ",取值是：" + values
    
    # 写入
    wirte_result(re,result)
'''	
#assert多个,
def assert_equals_all(names,values,els):
	global driver
	print('正在进行校验-----------------------------------------------------------------')	
	print('本次校验的多个期望结果是：%s,取值:%s'%(names,values))
	
	#调用拆分
	n=get_split(names)
	v=get_split(values)
	el=get_split(els)

	#依次校验每个值
	r=[]
	result=[]

	for i in range(len(n)):
		#调用取值
		values=get_value(v[i],el[i])
		#进行判断
		if n[i]==values:
			r.append("PASS")			
			result.append(n[i])
			
		else:			
			r.append("FAIL")
			result.append(values)

	#都为PASS时结果PASS,只要有一个FAIL就FAIL
	re="PASS"
	for i in range(len(r)):
		if r[i]=="FAIL":
			re="FAIL"
		
	if re!="FAIL":
		print('校验正确,校验结果：%s'%names)
	else:
		print('校验不正确，要校验的值为:%s,取值%s'%(names,result))
	
	#将result加,传给excel写入
	s=""
	for i in range(len(result)):
		s=s+result[i]+","
	print(s)
	# 写入
	wirte_result(re,s)
'''
#拆分多个参数,以逗号拆分，去除前后空格
def  get_split(names):
	n=[]
	name=names.split(',')
	for i in range(len(name)):
		#去掉空格
		n.append(name[i].strip())   
	return n
    
#assert多个,
def assert_all_method(method ,names,values,els):
    global driver
    print('正在进行多个校验-----------------------------------------------------------------')
    print('本次校验的多个%s,期望结果是：%s,取值:%s'%(method,names,values))
    
    #调用拆分
    n=get_split(names)
    v=get_split(values)
    el=get_split(els)

    #依次校验每个值
    r=[]
    result=[]
    for i in range(len(n)):
        #调用取值
        values=get_value(v[i],el[i])
        #根据method
        if method=="equal":
            #进行判断
            if n[i]== values:
                r.append("PASS")
                result.append(n[i])

            else:
                r.append("FAIL")
                result.append(values)
        elif method == "in":
            # 进行判断
            if n[i] in values:
                r.append("PASS")
                result.append(n[i])

            else:
                r.append("FAIL")
                result.append(values)
        elif method == "notin":
            # 进行判断
            print('正在校验',method,"校验值",n[i],"取值",values,'-----------------------------------------')
            print(n[i] not in values)
            if n[i] not in values:
                r.append("PASS")
                result.append(n[i])

            else:
                r.append("FAIL")
                result.append(values)
        elif method == "notequal":
            # 进行判断
            if n[i] != values:
                r.append("PASS")
                result.append(n[i])

            else:
                r.append("FAIL")
                result.append(values)

    #都为PASS时结果PASS,只要有一个FAIL就FAIL
    re="PASS"
    for i in range(len(r)):
        if r[i]=="FAIL":
            re="FAIL"
        
    if re!="FAIL":
        print('校验正确,校验结果：%s'%names)
    else:
        print('校验不正确，要校验的值为:%s,取值%s'%(names,result))
    
    #将result加分隔,传给excel写入
    s=""
    for i in range(len(result)):
        s=s+result[i]+","
    print(s)
    # 写入
    wirte_result(re,s)

#-------------------------------------------------------未调试
# 保存图片到本文件夹,暂时不用
def save_screenshot(filename):
    global driver
    driver.save_screenshot(filename)
    # 写入
    wirte_result("PASS", filename)

   
# 获取当前页元素，未可用
def get_page(*args,**kwargs):
    global  driver
    ret = driver.find_element_by_xpath(".//*")
    return ret


# scroll
def scroll(ori_el, des_el):
    global  driver
    deriver.scroll(ori_el, des_el)

# current_context
def current_context():
    global driver
    driver.current_context
# 获得所有contexts
def contexts():
    global driver
    driver.contexts
#-----------------------------------------------待调试
# 获取当前界面activity
def get_current_activity():
    global driver
    ac = driver.current_activity
    print('当前的activity:----------------',ac)

    # 写入
    wirte_result("PASS","当前activity是%s"%ac)
    return ac
#-----------------------------------------------   
#根据sourcepage判断
def source_assert(*args):
    global driver
    #先获取当前pagesource
    source = driver.page_source

    if args=="":
        print("未传入有效内容")
        re="FAIL"
        value="未传入有效内容"        

    elif len(args) > 1:
        n=len(args)
        i=0
        for x in args:
            if x in source:
                print(x + "存在")
                i=i+1
            else:
                print(x + "不存在")

        if i==n:
            re="PASS"
            value="都存在"
        else:
            re="FAIL"
            value="不是都存在"
    elif len(args) == 1 :
        if args[0] in source:
            print(args[0] + "存在")
            re="PASS"
            value="存在"            
        else:
            print(args[0] + "不存在")
            re="PASS"
            value="不存在"

    # 写入
    wirte_result(re,value)
#-----------------------------------------------
#返回坐标
def get_xy(radiox,radioy):
    #坐标
    coordinate=[]
    radiox=str(radiox)
    radioy=str(radioy)
    #如果输入小于1的，按比例提取，如果输入实际数    
    if radiox<'1':
        radio=float(radiox)
        radiox = int(SIZE()[2]*radio)

    if radioy<'1':
        radio=float(radioy)
        radioy = int(SIZE()[3]*radio)
    
    #print(str(radiox),str(radioy))
    coordinate.append(radiox)
    coordinate.append(radioy)


    # 写入
    #wirte_result('PASS','坐标为%s,%s'%(str(radiox),str(radioy))) 

    return coordinate
#-----------------------------------------------
#随机点击
def tap_random():
    R = []
    #生成2个随机数
    for i in range(2):
        r = random.randint(1, 9)/10
        R.append(r)
    print(R)
    x = int(SIZE()[2]*R[0])
    y = int(SIZE()[3]*R[1])
    #print(str(x),str(y))
    try:
        print("即将随机点击：" + str(x),str(y))
        driver.tap([(x,y)])
        re="PASS"
        value="随机点击坐标%s,%s"%(str(x),str(y))       

    except BaseException as e:
        print("随机点击出错了%s"%str(e))
        re="FAIL"
        value="随机点击出错了%s"%str(e)

    # 写入
    wirte_result(re,value)

#-----------------------------------------------        
#坐标点击
def tap_point(x,y):
    #如果输入坐标小于0，按比例提取坐标
    #如果传入是str类型，判断
    if type(x)==str:
        if x<'1':
            re=get_xy(x,y)
            x=re[0]
    elif x<1:
        re=get_xy(x,y)
        x=re[0]

    if type(y)==str:
        if y<'1':
            re=get_xy(x,y)
            y=re[1]
    elif x<1:
        re=get_xy(x,y)
        y=re[1]
 
        
    #print(str(x),str(y))
    print("即将点击坐标:" + str(x),str(y))
    try:
        driver.tap([(x,y)])
        re="PASS"
        value="点击坐标%s,%s"%(str(x),str(y))          

    except BaseException as e:
        
        print("点击出错了%s"%str(e))

        re="FAIL"
        value="点击出错了%s"%str(e)

    # 写入
    wirte_result(re,value)

#-----------------------------------------------
# 滑动多次
def swiptest(method,num):
    if num!="":
        num = int(num)

    else:
        num=1
    i = 0
    while i < num:
        if method == "left":
            swipeLeft()
        elif method == "right":
            swipeRight()
        elif method == "up":
            swipeUp()
        elif method == "down":
            swipeDown()
        i = i + 1

    # 写入
    value = method + ":" + str(num)
    wirte_result("PASS", value)


# 获取尺寸
def SIZE():
    global start_x, start_y, end_x, end_y
    start_x = 0
    start_y = 0
    end_x = driver.get_window_size()['width']
    end_y = driver.get_window_size()['height']
    return (start_x, start_y, end_x, end_y)

# 上划
def swipeUp():
    try:
        x1 = int(SIZE()[2] * 0.5)
        y1 = int(SIZE()[3] * 0.2)
        y2 = int(SIZE()[3] * 0.8)
        driver.swipe(x1, y2, x1, y1)

        value = "up"
        key = "PASS"
    except BaseException as err:
        print(err)
        value = str(err)
        key = "FAIL"

    # 写入
    wirte_result(key, value)


# 下划
def swipeDown():
    try:
        x1 = int(SIZE()[2] * 0.5)
        y1 = int(SIZE()[3] * 0.2)
        y2 = int(SIZE()[3] * 0.8)
        driver.swipe(x1, y1, x1, y2)

        value = "down"
        key = "PASS"
    except BaseException as err:
        print(err)
        value = str(err)
        key = "FAIL"

    # 写入
    wirte_result(key, value)


# 左划
def swipeLeft():
    try:
        x1 = int(SIZE()[2] * 0.2)
        x2 = int(SIZE()[2] * 0.8)
        y1 = int(SIZE()[3] * 0.5)
        driver.swipe(x2, y1, x1, y1)

        value = "left"
        key = "PASS"
    except BaseException as err:
        print(err)
        value = str(err)
        key = "FAIL"

    # 写入
    wirte_result(key, value)

# 右划
def swipeRight():
    try:
        x1 = int(SIZE()[2] * 0.2)
        x2 = int(SIZE()[2] * 0.8)
        y1 = int(SIZE()[3] * 0.5)
        driver.swipe(x1, y1, x2, y1)

        value = "right"
        key = "PASS"
    except BaseException as err:
        print(err)
        value = str(err)
        key = "FAIL"

    # 写入
    wirte_result(key, value)

#----------------------------------------------------------------------
#error时执行
def err_run(err,func,*args,**kwargs):
    print(err)
    value = str(err)
    key = "FAIL"

    # 写入
    wirte_result(key, value)
    #重试
    rerun(func,*args,**kwargs)
    

#重试（三次）
count = 1
def rerun(func,*args,**kwargs):
    global count
    if count <= 3:
        print("重试第%d次" % count)
        count = count + 1
        func(*args,**kwargs)
    else:
        print("结束成功")
        count = 1
        return count
#----------------------------------------------------------------------
#弹窗点击关闭，id=com.ishugui:id/imageview_cloud_sysch_close,
def  tanchuang(id):
    global driver
    try:
        #存在就关闭，不存在就不操作
        source=driver.page_source
        if id in source:
            el=driver.find_element_by_id(id)
            el.click()
            print('关闭了弹窗')
        else:
            print('弹窗不存在')
            
    except Exception as  err:
            print('弹窗报错了',err)


#----------------------------------------------
#弹窗关闭
def tanchuang_all():
    #从配置文件中取参数,id
    ids=conf.tanchuang_close_id
    for x in ids:
        source=driver.page_source
        if x in source:
            el=driver.find_element_by_id(x)
            el.click()
            print('关闭了弹窗')            
            
        else:
            print('不存在弹窗id',x)

#-------------------------------------------------------未调试    
# 获取当前页所有元素
#取source
def get_pagesource(file=""):
        global driver
        r=driver.page_source
      
        try:
            #有返回值
            if r:
                print('pagesource:',r[:10])
                if file=="":
                    filename=pageDir+"page_%s.xml"%(number)

                #file不为空，保存文件    
                else:
                    #存储文件名
                    filename=pageDir+"%s_page_%s.xml"%(file,number)
                                                                              
            else:
                    print("pagesource空-----------------------------------------------")

            if len(r)>10:
                print("保存文件：",filename)
                #调用写入xml文件
                write_xml_to_file(filename,r)
            #写入
            wirte_result("PASS", file)    
        
        except Exception as err:
            print(err) 
            #写入
            wirte_result("FAIL", file)

#-----------------------------------------------------------
#xml 存到文件中
def write_xml_to_file(filename,content):
    with open(filename,"w+",encoding='utf-8') as f:
        f.write(content)
        print("写入xml到文件")

#-----------------------------------------------------------    
#判断元素是否存在，text
def is_exist_text(name):
        try:
            #el = driver.find_element_by_android_uiautomator("text(\"%s\")" %name)
            xpath_value='//*[contains(@text, %s)]'%name
            el=driver.find_element_by_xpath(xpath_value)
            return True
            print("元素定位成功")
        except BaseException as e:
            print(e.args)
            print("元素定位失败")
            return False

#-----------------------------------------------------------
#判断source中存在就点击
def xpath_exist(method,name):
    #根据text包含值，点击
    source=driver.page_source
    print('正在判断是否存在元素----------------------------------------------------',method,name)
    if name in source:
        x="//*[contains(@%s,%s)]"%(method,name)
        print(x)
        el=driver.find_element_by_xpath(x)          
        el.click()
        print('已经点击了',name)   

    else:
        print('不存在',name)


#----------------------------------------------------------------------

if __name__ == "__main__":
    pass
