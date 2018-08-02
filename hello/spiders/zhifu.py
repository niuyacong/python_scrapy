# -*- coding: utf-8 -*-
from  scrapy import  Spider ,Request
import json
from hello.items import UserItem
"""
知乎用户
"""

class ZhifuSpider(Spider):
    name = 'zhifu'
    allowed_domains = ['www.zhifu.com']
    start_urls = ['https://www.zhifu.com/']

    start_user="excited-vczh"
    user_url="https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query="allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"
    
    follows_url="https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query="data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"
    
    
    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follow)
    
    def parse_user(self, response):
        result=json.loads(response.text)
        item=UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item
        a=self.follows_url.format(user=result.get('url_token'), include=self.follows_query,offset=0,limit=20)
        print('分页地址：',a)
        yield Request(a,callback=self.parse_follow,dont_filter=True)
   
    def parse_follow(self, response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for item in results.get('data'):
                a=self.user_url.format(user=item.get('url_token'),include=self.user_query)
              
                yield Request(a,callback=self.parse_user,dont_filter=True)

        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            print('下一页：'+results.get('paging').get('next'))
            yield Request(results.get('paging').get('next'),callback=self.parse_follow,dont_filter=True)
