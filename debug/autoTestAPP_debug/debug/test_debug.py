# coding:utf-8
from common import elementApp as app
from common import readexcel as reader,writeexcel as writer
import json
import jsonpath
import re
import time



srcfile=r"E:\myworkspace\mygit\autoTestAPP_demo\datadir\myApp.xls"
desfile=r"E:\myworkspace\mygit\autoTestAPP_demo\datadir\myApp_result.xls"

resultfile=r"E:\myworkspace\mygit\autoTestAPP_demo\result\screenshot\screenshot__"

#配置data文件目录
filepaht=r"E:\myworkspace\mygit\autoTestAPP_demo\datadir"
srcfile=filepath+"\myApp.xls"
desfile=filepath+"\myApp_result.xls"
resultfile=filepath+"\result\screenshot\screenshot_"



'''
#app.update_capability("appPackage","diankan")
print(app.desired_caps)

url="http://localhost:4723/wd/hub"
timeout=5
print('正在启动...')
app.start(url,timeout)

print('启动客户端.....')

time.sleep(5)

print('打开客户端了')

#启动页向左滑动
app.swip("left","3")



#点击男
print('已经滑动到第3页，正在选择男 女 ...')
app.get_element("id","com.ishugui:id/tv_man","","man")
app.click("man",)
print('选择男生，进入主界面')
'''

'''
driver=app.driver
el=driver.find_element_by_id("com.ishugui:id/tv_man")
result=el.click()

print('定位元素-----------------',el,result)
print('点击结果-----------------',result)
'''

#重试（三次）
count = 0
def rerun(func):
    global count
    count = count + 1
    if count <= 3:
        print("重试第%d次" % count)
        func()
    else:
        print("结束")
        pass
        print("结束成功")
        count = 0
        return count


def run(line):
    try:
        if line[3]=='caps':
            app.update_capability(line[4],line[5])
            return
        if line[3]=='start':
            app.start(line[4],line[5])
            return
        if line[3]=='sleep':
            app.sleep(line[4])
            return
        if line[3]=='swip':
            app.swip(line[4],line[5])
            return
        if line[3]=='id':
            app.get_element("id",line[4],line[5],line[6])
            return
        if line[3]=='name':
            app.get_element("name",line[4],line[5],line[6])
            return
        if line[3]=='text':
            app.get_element("text",line[4],line[5],line[6])
            return
        if line[3]=='css':
            app.get_element("css",line[4],line[5],line[6])
            return
        if line[3]=='xpath':
            app.get_element("xpath",line[4],line[5],line[6])
            return
        if line[3]=='class':
            app.get_element("class",line[4],line[5],line[6])
            return     
        if line[3]=='click':
            app.clicks("click",line[4],line[5],line[6])
            return
        if line[3]=='clear':
            app.clicks("clear",line[4],line[5],line[6])
            return
        if line[3]=='input':
            app.clicks("input",line[4],line[5],line[6])
            return    

        if  line[3]=='assertequals':
            app.assertequals(line[4],line[5])
            return
        if  line[3]=='savephoto':
            app.get_screenshot(resultfile,line[4])
            return

    except BaseException as e:
        print(e.args)
        app.get_screenshot(resultfile+'error_',line[4])
        
        rerun(run)

        
reader.open_excel(srcfile)
writer.copy_open(srcfile,desfile)

for i in range(0,reader.r):
    line=reader.readline()
    print(line)
    if len(line[0])>2 or len(line[1])>2:
        #不去执行的行
        pass
    else:
        #执行
        run(line)
        pass
                                                        
writer.save_close()


