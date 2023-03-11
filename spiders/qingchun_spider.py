# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from MeiZhi.items import MeizhiItem
import time
import random
from MeiZhi.tools.tool import Judge
from MeiZhi.tools.tool import Judge1

class QingchunSpiderSpider(scrapy.Spider):
    name = 'qingchun_spider'
    # allowed_domains = ['www.v2ph.com']
    start_urls = ['https://www.v2ph.com/category/pure']
    x1="本程序功能旨在学习，请不要有过多想法，禁止用作商业用途"
    x2="程序说明注意事项如下"
    x3="图片的页面大概有一百来页，每页大概上百张图"
    x4="有三种插图模式，当程序提示'请输入你想爬取的页数时:'，只需如如一个数字（注意是数字,但千万别是负数）即可获得对饮页数的图片"
    x5="当你输入的页数大于100时，会给你随机返回一个页面的图片，虽然我知道你硬盘空间大，但还是要节制"
    x6="如果你想爬取某几页的图片，可以在上一步骤输数字时输入0，这时会弹出'输入你想爬取的页面:'这时你可以输入一个列表"
    x7="列表的格式一定要像这样：[1,4,9,...]（记得用英文输入法）,这样你就可以获取第1，4，9和列表中其他数字对应的页面了"
    x8="大致就是这样，一些小的bug是在改不过来了，还是开始吧禽兽！！！"
    x9="作者--别人家的孩子他爹"
    print("{0:*^60}\n{1:*^60}\n{2:*^60}\n{3:*^60}\n{4:*^60}\n{5:*^60}\n{6:*^60}\n{7:*^60}\n{8:*^60}".format(x1,x2,x3,x4,x5,x6,x7,x8,x9))
    time.sleep(10)
    print("5秒后开始程序,爬取到的图片会自动保存到你d盘根目录下一个名为'meizi'的文件中，如果中涂想退出，可以连按两次'ctrl+c'")
    time.sleep(5)
    next_url_list = []
    x=1
    c=Judge()
    if c==0:
        b=Judge1()
    if c>100:
        print("正在随机爬取一页图片")
        h=random.randint(1,100)



    def parse(self, response):
        # time.sleep()
        self.x += 1
        image_element =response.css(".col-12")
        # page_element=response.css(".pagination.justify-content-center a")
        for v in image_element:
            name=v.css(".h6 a::text").extract_first("")
            list_url=v.css(".h6 a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,list_url),meta={"name":name},callback=self.parse_forward)
        if self.c>100:
            page_next_url = "https://www.v2ph.com/category/pure?page={}".format(self.h)
            yield Request(url=parse.urljoin(response.url, page_next_url), callback=self.parse)
        elif self.x<=self.c+1 and self.c!= 0:
            page_next_url = "https://www.v2ph.com/category/pure?page={}".format(self.x)
            yield Request(url=parse.urljoin(response.url, page_next_url), callback=self.parse)
        elif self.c==0 and self.x<=len(self.b)+1:
            page_next_url = "https://www.v2ph.com/category/pure?page={}".format(self.b[self.x-2])
            yield Request(url=parse.urljoin(response.url, page_next_url), callback=self.parse)




    def parse_forward(self,response):
        # time.sleep(5)
        name=response.meta.get("name","")
        item_loader=ItemLoader(item=MeizhiItem(),response=response)
        image_list=response.css(".photos-list.text-center img")
        image_node=response.css(".pagination.justify-content-center a")
        for w in image_list:
            image_url=w.css("::attr(data-src)").extract_first("")
            item_loader.add_value("name",name)
            item_loader.add_value("image_url",[image_url])
            item=item_loader.load_item()
            yield item

        next_url=image_node.css("::attr(href)").extract()[-2]
        self.next_url_list.append(next_url)
        if (next_url)and(next_url not in self.next_url_list):
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse_forward)

    # def parse_forward_next(self,response):
    #     # time.sleep(3)
    #     name = response.meta.get("name", "")
    #     image_list = response.css(".photos-list.text-center img")
    #     item_loader = ItemLoader(item=MeizhiItem(), response=response)
    #     for w in image_list:
    #         image_url=w.css("::attr(src)").extract_first("")
    #         item_loader.add_value("name",name)
    #         item_loader.add_value("image_url",image_url)
    #         item=item_loader.load_item()
    #         yield item



