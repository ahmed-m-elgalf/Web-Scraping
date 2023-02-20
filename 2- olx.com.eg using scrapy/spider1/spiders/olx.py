# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import os
from datetime import datetime



now = datetime.now()
month_day_year = now.strftime("%m-%d-%Y, %H-%M")

items = []

class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.com.eg']


    def start_requests(self):

        with open('read.txt') as f:
            links = f.read().split('\n')

        # loop over list of initial links to crawl
        for link in links:
            # initial HTTP request
            yield scrapy.Request(
                url=link,
                callback=self.parse
            )

    def parse(self, response):
        container = response.xpath('//div[contains(@class,"_963450d6")]')
        rows = response.xpath('.//article[contains(@class,"_7e3920c1")]')


        for row in rows :
                title = row.xpath(".//div[contains(@class,'a5112ca8')]/text()").get()
                price = row.xpath(".//div[contains(@class,'_52497c97')]/span/text()").get()

                location = row.xpath(".//span[contains(@class,'_424bf2a8')]/text()").get()
                creation_date = row.xpath(".//span[contains(@aria-label, 'Creation date')]/text()").get()

                link = row.xpath(".//div[contains(@class,'ee2b0479')]/a/@href").get()


                yield response.follow(url=link,callback = self.parse_job ,
                meta={'title':title ,
                    'price':price,
                    'location':location,
                    'creation_date':creation_date,
                    # 'link':response.urljoin(link) ,
                    'link':response.url,
                    }  )

        nxt_page =response.xpath("(//ul[contains(@class,'_92c36ba1')]/li/a)[last()]/@href").get()


        print(nxt_page)
        page_num = int( nxt_page.split('=', 1)[1])
        print(page_num)

        if page_num < 11 :
            yield response.follow(nxt_page , callback=self.parse )


                # item = {
                #         'title': title,
                #         'price': price,
                #         'location': location,
                #         'creation_date': creation_date,
                #         'link': link,
                #         'url': response.url,

                #     }


                # items.append(item)




                # yield {
                #         'title':title,
                #         'price': price,
                # }


            # Return data extracted


    def parse_job(self, response):

        title = response.request.meta['title']
        price = response.request.meta['price']
        location = response.request.meta['location']
        creation_date= response.request.meta['creation_date']
        link= response.request.meta['link']


        publisher = response.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/a/div/div[2]/span/text()').get()

        details = response.xpath('//div[@class="_241b3b1e"]//text()').extract()

        images = response.xpath('//div[@class="image-gallery-slides"]//@src').extract()


        desc  = response.xpath('//div[@class="_0f86855a"]/span/text()').extract()

        ad_num =  response.xpath('//div[@class="_171225da"]/text()').extract()


        it = iter(details)
        res_dct = dict(zip(it, it))


        item = {
                'title': title,
                'price': price,
                'location': location,
                'creation_date': creation_date,
                'link': link,
                'publisher':publisher,
                'details':res_dct,
                'images':images,
                'desc':desc,
                'ad_num':ad_num,
                'date' : str(month_day_year),
                'url': response.url,
            }

        items.append(item)

    def closed(self, reason):
        # create datafrane from the global list 'items'
        df = pd.DataFrame(items)
        # do whatefer operations you want
        df.to_csv(f'olx{month_day_year}.csv', index=False)













