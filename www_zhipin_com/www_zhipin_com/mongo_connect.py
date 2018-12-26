import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
import datetime
from bson import binary

headers = {
    'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43c0-aad4-37fce8e3ff39",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'dnt': "1",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
    # 'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
    'cache-control': "no-cache",
    'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831"
}
conn = MongoClient('127.0.0.1', 27017)
db = conn.jobs  # 连接mydb数据库，没有则自动创建


def init():
    items = db.jobs_python.find().sort('pid')
    for item in items:
        if 'detail' in item.keys():  # 在爬虫挂掉再此爬取时，跳过已爬取的行
            continue
        detail_url = "https://www.zhipin.com/job_detail/%s.html?ka=search_list_1" % item['pid']
        print(detail_url)
        result = requests.Session()
        html = result.get(detail_url, headers=headers)
        if html.status_code == 404:
            item['detail'] = 'job has been taken'
            item['location'] = '-'
            res = update(item)  # 保存数据
            print(res)
            print('job has been taken')
            continue
        # 302验证码
        elif html.history:
            print('please input verify code to continue.')
            break
        elif html.status_code != 200:  # 爬的太快网站返回403，这时等待解封吧
            print('status_code is %d,please wait and slow down' %
                  html.status_code)
            break

        soup = BeautifulSoup(html.text, "html.parser")
        job = soup.select(".job-sec .text")
        if len(job) < 1:
            continue
        item['detail'] = job[0].text.strip()  # 职位描述
        location = soup.select(".job-sec .job-location .location-address")
        item['location'] = location[0].text.strip()  # 工作地点
        item['updated_at'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())  # 实时爬取时间
        # logo_url = soup.find('a', attrs={"ka": "job-detail-company"}).find('img').attrs['src']  # 爬取公司图标
        # data = requests.get(logo_url, timeout=10).content
        # item['logo'] = binary.Binary(data)
        res = update(item)  # 保存数据
        print(res)
        time.sleep(5)  # 停停停


# 保存数据到 MongoDB 中
def update(item):
    return db.jobs_python.update_one({"_id": item['_id']}, {"$set": item})


def clear_time():
    items = db.jobs_python.find({})
    for item in items:
        # print(item['time'])
        if not item['time'].find('布于'):
            continue
        item['time'] = item['time'].replace('发布于', '2018-')
        item['time'] = item['time'].replace("月", "-")
        item['time'] = item['time'].replace("日", "")
        if item['time'].find('昨天') > 0:
            item['time'] = str(datetime.date.today() -
                               datetime.timedelta(days=1))
        elif item['time'].find(':') > 0:
            item['time'] = str(datetime.date.today())
        update(item)
    print("clearTime OK")


def clear_salary():
    items = db.jobs_python.find({})
    for item in items:
        if type(item['salary']) == type({}):
            continue
        salary_list = item['salary'].lower().replace("k", "000").split("-")
        if len(salary_list) != 2:
            print(salary_list)
            continue
        try:
            salary_list = [int(x) for x in salary_list]
        except:
            print(salary_list)
            continue
        item['salary'] = {
            'low': salary_list[0],
            'high': salary_list[1],
            'avg': int((salary_list[0] + salary_list[1]) / 2)
        }
        # item['salary']['avg'] = int((item['salary']['low']+item['salary']['high'])/2)
        update(item)
    print('clearSalary OK')


def update_work_year():
    items = db.jobs_python.find({})
    for item in items:
        if item['workYear'] == '应届毕业生':
            item['workYear'] = '应届生'
        elif item['workYear'] == '1年以下':
            item['workYear'] = '1年以内'
        elif item['workYear'] == '不限':
            item['workYear'] = '经验不限'
        update(item)
    print('update work year OK')


# 设置招聘的水平，分两次执行
def set_level():
    items = db.jobs_python.find({})
    for item in items:
        if item['workYear'] == '应届生':
            item['level'] = 1
        elif item['workYear'] == '1年以内':
            item['level'] = 2
        elif item['workYear'] == '1-3年':
            item['level'] = 3
        elif item['workYear'] == '3-5年':
            item['level'] = 4
        elif item['workYear'] == '5-10年':
            item['level'] = 5
        elif item['workYear'] == '10年以上':
            item['level'] = 6
        elif item['workYear'] == '经验不限':
            item['level'] = 10
        update(item)
    print('set level OK')


init()
set_level()
update_work_year()
clear_salary()
clear_time()
