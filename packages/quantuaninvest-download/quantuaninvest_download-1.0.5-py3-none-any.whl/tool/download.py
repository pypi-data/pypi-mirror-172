import datetime
import requests
import os


def mkdir_if_not_exist(save_file_path):
    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)


def get_last_work_day():
    date = datetime.datetime.today()  # 今天
    # print(date.today())
    w = date.weekday() + 1
    # print(w) #周日到周六对应1-7
    if w == 1:  # 如果是周一，则返回上周五
        lastworkday = (date + datetime.timedelta(days=-3)).strftime("%Y%m%d")
    elif 1 < w < 7:  # 如果是周二到周五，则返回昨天
        lastworkday = (date + datetime.timedelta(days=-1)).strftime("%Y%m%d")
    elif w == 7:  # 如果是周日
        lastworkday = (date + datetime.timedelta(days=-2)).strftime("%Y%m%d")
    return lastworkday


lastworkday = get_last_work_day()


def save_file_to_ref_path(respose, save_path):
    if respose.status_code == 200:
        print("现在时间是 ", datetime.datetime.now())
        file_path = get_save_file_path(save_path)
        mkdir_if_not_exist(save_path)
        # 保存
        with open(file_path, 'wb') as f:
            f.write(respose.content)


def download_file_from_ref_url(url_path):
    r = requests.get(url_path)  # 发送请求
    return r


def get_download_path(download_url_path):
    lastworkday = get_last_work_day()
    url = download_url_path + lastworkday + '.xlsx'  # 目标下载链接
    return url


def get_save_file_path(save_file_path):
    file_path = save_file_path + lastworkday + '.xlsx'
    return file_path


def down_load_file(download_url, save_file_path):
    try:
        print("down_load_file 执行 ", datetime.datetime.now())
        url_path = get_download_path(download_url)
        res = download_file_from_ref_url(url_path)
        file_path = get_save_file_path(save_file_path)
        print("code is ", res.status_code)
        save_file_to_ref_path(res, file_path)
        return res.status_code
    except Exception as e:
        print("error ", e)
        return 500


