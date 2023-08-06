import datetime 
import requests
import time
import schedule
import functools
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class download_tool():


    def down_load_file(name):
        print("down_load_file 执行 ",datetime.datetime.now(),name)
        date=datetime.datetime.today() #今天
        #print(date.today())
        w=date.weekday()+1
        #print(w) #周日到周六对应1-7
        if w==1: #如果是周一，则返回上周五
            lastworkday=(date+datetime.timedelta(days=-3)).strftime("%Y%m%d")
        elif 1<w<7: #如果是周二到周五，则返回昨天
            lastworkday=(date+datetime.timedelta(days=-1)).strftime("%Y%m%d")
        elif w==7: #如果是周日
            lastworkday=(date+datetime.timedelta(days=-2)).strftime("%Y%m%d")

        print("w ",w)
        print("lastworkday ",lastworkday)

        url = 'https://www.quantuaninvest.cn/shipan/12/'+lastworkday+'.xlsx' # 目标下载链接
        r = requests.get(url) # 发送请求
        print("code is ",r.status_code)
        if r.status_code == 200:
            print("现在时间是 ",datetime.datetime.now())
            save_path = 'C:/data/pa_qmt/dk_sp/25505/'+lastworkday+'.xlsx'
            # 保存
            with open (save_path, 'wb') as f:
                f.write(r.content)



