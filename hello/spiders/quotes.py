# -*- coding: utf-8 -*-

""" 
scarpy
    安装依赖库：
    pip install wheel
    pip install lxml  也可以下载lxml whl文件  运行这个文件
    pip install PyOpenSSL  步骤也可同上
    Twisted  https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted  下载whl文件
    Pywin32  pip install pywin32
    Scrapy   pip install scrapy
 

 scrapy 使用：
    # 创建了一个名为test的项目
    scrapy startproject test 
    #进入项目
    cd test
    # 创建一个模块
    scrapy genspider  quotes quotes.toscrape.com  


 在此界面运行  scrapy crawl quotes  则请求地址

 scrapy shell quotes.toscrape.com 调出命令行交互界面

 scrapy crawl quotes -o quotes.json 保存到quotes.json文件中

 保存到jsonline
 scrapy crawl quotes -o quotes.jl  一条数据一行  没有中括号[]

  scrapy crawl quotes -o quotes.csv
  scrapy crawl quotes -o quotes.xml
  scrapy crawl quotes -o quotes.pickle
  scrapy crawl quotes -o quotes.marshal

保存到ftp
scrapy crawl quotes -o ftp://user:pass@ftp.example.com/path/quotes.csv 



Tushare是一个免费、开源的python财经数据接口包
pip install tushare
"""
import scrapy
from hello.items import HelloItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    # 默认的回调方法
    def parse(self, response):
        quotes=response.css('.quote')
        for quote in quotes:
            item=HelloItem()
            text=quote.css('.text::text').extract_first() # 输出文本值
            author=quote.css('.author::text').extract_first() # extract_first()第一个
            tags=quote.css('.tags .tag::text').extract() # extract() 所有
            item['text']=text
            item['author']=author
            item['tags']=tags
            yield item
        
        next=response.css('.pager .next a::attr(href)').extract_first()
        url=response.urljoin(next) # 获取绝对的路径
        print(url)
        yield scrapy.Request(url=url,callback=self.parse)
