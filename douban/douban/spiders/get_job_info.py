import scrapy
import bs4
from ..items import Class14Item

class Spider_GetJobInfo(scrapy.Spider):
#定义一个爬虫类Spider_GetJobInfo
    name = 'GetJobsInfo'
    #定义爬虫的名字为GetJobs
    allowed_domains = ['www.jobui.com']
    #定义允许爬虫爬取网址的域名——职友集网站的域名
    start_urls = ['https://www.jobui.com/rank/company/']
    #定义起始网址——职友集企业排行榜的网址

    def parse(self, response):
    #parse是默认处理response的方法
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        #用BeautifulSoup解析response（企业排行榜的网页源代码）
        ul_list = bs.find_all('ul',class_="textList flsty cfix")
        #用find_all提取<ul class_="textList flsty cfix">标签
        for ul in ul_list:
        #遍历ul_list
            a_list = ul.find_all('a')
            #用find_all提取出<ul class_="textList flsty cfix">元素里的所有<a>元素
            for a in a_list:
            #再遍历a_list
                company_id = a['href']
                #提取出所有<a>元素的href属性的值，也就是公司id标识
                url = 'https://www.jobui.com{id}jobs'.format(id=company_id)
                #构造出包含公司名称和招聘信息的网址链接的list
                yield scrapy.Request(url, callback=self.parse_GetJobInfo)
    # 用yield语句把构造好的request对象传递给引擎。用scrapy.Request构造request对象。callback参数设置调用parse_GetJobInfo方法。

    def parse_GetJobInfo(self, response):
        # 定义新的处理response的方法parse_GetJobInfo（方法的名字可以自己起）
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        # 用BeautifulSoup解析response(公司招聘信息的网页源代码)
        company = bs.find(class_="company-banner-name").text
        # 用find方法提取出公司名称
        datas = bs.find_all('div', class_="job-simple-content")
        # 用find_all提取<div class_="job-simple-content">标签，里面含有招聘信息的数据
        for data in datas:
            # 遍历datas
            item = Class14Item()
            # 实例化Class14Item这个类
            item['company'] = company
            # 把公司名称放回Class14Item类的company属性里
            item['position'] = data.find_all('div', class_="job-segmetation")[0].find('h3').text
            # 提取出职位名称，并把这个数据放回Class14Item类的position属性里
            item['address'] = data.find_all('div', class_="job-segmetation")[1].find_all('span')[0].text
            # 提取出工作地点，并把这个数据放回Class14Item类的address属性里
            item['detail'] = data.find_all('div', class_="job-segmetation")[1].find_all('span')[1].text
            # 提取出招聘要求，并把这个数据放回Class14Item类的detail属性里
            yield item
            # 用yield语句把item传递给引擎