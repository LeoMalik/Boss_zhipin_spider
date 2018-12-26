# Boss_zhipin_spider
🔎 Boss 直聘 Python 招聘岗位信息爬取和分析🔎 

爬取了[BOSS直聘](https://www.zhipin.com/)上 Python 关键字全国范围内的招聘岗位

部分城市无数据不列入统计，故地区范围为中国101个城市，总共3112条数据，结构如下：

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykig71tp0j20am0873ys.jpg)

字段浅显易懂，其中需要说明的是pid为每个待招岗位的唯一id，在访问页面详情时会用到

例：[](https://www.zhipin.com/job_detail/cd6ff0e8a82db26d1HV-092_F1Y~.html) ，注意爬取不要太快，否则403警告😏

## 项目结构

boss招聘.ipynb -> 生成分析图表

mongo_connect.py -> 数据清洗，存入mongodb

pipelines.py -> 数据过滤的管道

spider -> 爬虫

wordcloud -> 生成词云

settings.py -> scrapy配置文件

middlewares.py -> scrapy中间组件

## 运行方式

```python
pip install -r requirements.txt
scrapy crawl zhipin -o jobs_python
```

使用 Jupyter Notebook 配合 echarts进行绘图（绘图部分由我可爱的girl编写，真的很棒），部分示例图如下所示🔍



![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykj588ghzj20nh0audg2.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykj80pndaj20mc0aljrt.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykj8pdn67j20na0b7mxt.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykj8zir0cj20n40b0wf1.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykj9hlkjej20mh0as3z1.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjcg93adj20mg0aldg7.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjftea2ij20m40asdg5.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082ly1fykk0xnradj20j109kdlo.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjg6bf0xj20b0079mxk.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjgf8e15j20mh0bhq3g.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjgm58arj20la0anglt.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjh34paij20bl07aaa3.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjhewwydj20mh0bet9k.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykji2voywj20lw0b6759.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjirrfd7j20lj0b6q40.jpg)

![](https://ws1.sinaimg.cn/mw690/c364e082gy1fykjjog3jcj20xg0gpacc.jpg)

**如果能帮上你的话，献上一个小小的 Star 👍吧**

## 后续慢慢补充

- [ ] 智能识别302跳转的验证码，并进行输入
- [ ] 多线程爬虫