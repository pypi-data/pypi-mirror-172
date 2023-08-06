import datetime 
import requests
import time
import schedule
import functools
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception as e :
                import traceback
                print(traceback.format_exc())
                traceback.print_stack()
                print("error ",e)
                info = traceback.format_exc()
                send_email(info,e)
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@catch_exceptions(cancel_on_failure=True)
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



def send_email(msg,title):
	

	# 发件人
	from_name = "gdd_0001_下载任务_rz"
	# 发件邮箱
	from_addr = "252992499@qq.com"
	# 发件邮箱授权码，注意不是QQ邮箱密码
	from_pwd = "fuitzhzgvylsbigj"
	# 收件邮箱
	to_addr = "252992499@qq.com"

	# 邮件标题
	my_title = from_name + "-融资实盘错误-" + str(title)
	# 邮件正文
	my_msg = msg

	# MIMEText三个主要参数
	# 1. 邮件内容
	# 2. MIME子类型，plain表示text类型
	# 3. 邮件编码格式，使用"utf-8"避免乱码
	msg = MIMEText(str(my_msg), 'plain', 'gbk')
	msg['From'] = formataddr([from_name, from_addr])
	# 邮件的标题
	msg['Subject'] = my_title

	# SMTP服务器地址，QQ邮箱的SMTP地址是"smtp.qq.com"
	smtp_srv = "smtp.qq.com"

	try:
		# 不能直接使用smtplib.SMTP来实例化，第三方邮箱会认为它是不安全的而报错
		# 使用加密过的SMTP_SSL来实例化，它负责让服务器做出具体操作，它有两个参数
		# 第一个是服务器地址，但它是bytes格式，所以需要编码
		# 第二个参数是服务器的接受访问端口，SMTP_SSL协议默认端口是465
		srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)

		# 使用授权码登录QQ邮箱
		srv.login(from_addr, from_pwd)

		# 使用sendmail方法来发送邮件，它有三个参数
		# 第一个是发送地址
		# 第二个是接受地址，是list格式，可以同时发送给多个邮箱
		# 第三个是发送内容，作为字符串发送
		srv.sendmail(from_addr, [to_addr], msg.as_string())
		print('发送成功')
	except Exception as e:
		print('发送失败')
		print("error ",e)
	finally:
		# 无论发送成功还是失败都要退出你的QQ邮箱
		srv.quit()


name = "下载任务"
schedule.every().day.at("09:10").do(down_load_file, name)
schedule.every().day.at("09:12").do(down_load_file, name)
schedule.every().day.at("09:14").do(down_load_file, name)
schedule.every().day.at("09:50").do(down_load_file, name)
schedule.every().day.at("12:04").do(down_load_file, name)
schedule.every().day.at("12:50").do(down_load_file, name)
schedule.every().day.at("15:05").do(down_load_file, name)
schedule.every().day.at("17:22").do(down_load_file, name)

while True:
    schedule.run_pending()
    time.sleep(1)
