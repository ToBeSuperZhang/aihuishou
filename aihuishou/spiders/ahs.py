# -*- coding: utf-8 -*-
import scrapy


class AhsSpider(scrapy.Spider):
    name = 'ahs'
    allowed_domains = ['aihuishou.com']
    start_urls = ['http://aihuishou.com/']

    def parse(self, response):
        print('first')
        first_title_list = response.xpath('//div[@id="category-pop"]/ul/li//a/text()').extract()
        first_link_list = response.xpath('//div[@id="category-pop"]/ul/li//a/@href').extract()

        # for i in range(len(first_title)):
        for i in range(1):
            first_link = response.url[:-1] + first_link_list[i]
            first_title = first_title_list[i]
            print(first_link)
            request = scrapy.Request(first_link, callback=self.parse_second_level, dont_filter=True)
            request.meta['first_title'] = first_title

            yield request

    def parse_second_level(self, response):
        print('second')
        second_title_list = response.xpath('//div[@class="main-right"]//li/a/@title').extract()
        second_link_list = response.xpath('//div[@class="main-right"]//li//a/@href').extract()
        print(second_title_list)
        # for i in range(len(second_title)):
        for i in range(1):
            second_link = 'http://aihuishou.com' + second_link_list[i]
            second_title = second_title_list[i]
            request = scrapy.Request(second_link, callback=self.parse_third_level, dont_filter=True)
            request.meta['first_title'] = response.meta['first_title']
            request.meta['second_title'] = second_title
            print(request.meta['first_title'], request.meta['second_title'], second_link)
            yield request

        pass

    def parse_third_level(self, response):
        print('third')

        third_title_list = response.xpath('//div[@class="product-list-wrapper"]//li/a/@title').extract()
        third_link_list = response.xpath('//div[@class="product-list-wrapper"]//li/a/@href').extract()
        print(third_link_list)
        print(third_title_list)

        for i in range(1):
            third_title = third_title_list[i]
            third_link = 'http://aihuishou.com' + third_link_list[i]
            print(third_link)
            request = scrapy.Request(third_link, callback=self.parse_last, dont_filter=True)
            request.meta['first_title'] = response.meta['first_title']
            request.meta['second_title'] = response.meta['second_title']
            request.meta['third_title'] = third_title
            print(response.meta['first_title'])
            print(response.meta['second_title'])
            print(third_title)
            yield request
        pass

    def parse_last(self, response):
        print('last')
        model_name = response.xpath('//div[@class="left"]/h1/text()')
        recycle_num = response.xpath('//div[@class="left"]/ul/li/text()').extract()[0].split()
        max_price = response.xpath('//div[@class="left"]/ul/li/text()').extract()[1].split()
        print(model_name,recycle_num,max_price)
        with open('price.txt','wb') as f:
            f.write(response.body)
            f.flush()
            f.close()
        pass


'5883692440607911115'
'2307851754145590917'
'8720613330200450328'