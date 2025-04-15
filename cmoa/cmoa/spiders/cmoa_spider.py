import scrapy
import redis
import json
import time

from datetime import date

r = redis.Redis('localhost', port=6379)

class CmoaSpider(scrapy.Spider):
    name = 'cmoa'
    start_urls = [
        'https://www.cmoa.jp/newrelease/schedule/?page=1',
        'https://www.cmoa.jp/newrelease/schedule/?page=2',
        'https://www.cmoa.jp/newrelease/schedule/?page=3',
        'https://www.cmoa.jp/newrelease/schedule/?page=4',
        'https://www.cmoa.jp/newrelease/schedule/?page=5',
    ]

    def parse(self, response):
        for title in response.css('div.h_long_thum_w_4.volume'):
            if title.css('div.vol_num::text').re(r'^1(?:-\d+)?\D.*$'):
                item = {
                    'img': f'https:{title.css('img::attr(src)').get()}',
                    'id': title.css('a::attr(href)').re_first(r'/title/(\d+)/')
                }

                r.set('update_timestamp', time.time())
                r.rpush('titles', json.dumps(item))


class CmoaAdditionalInfoSpider(scrapy.Spider):
    name = 'cmoa_additional_info'

    # ^(?:\d{1,2}\/\d{1,2})
    def parse(self, response):
        date_str = response.css('div.nextReleaseBox.this p.date').re_first(r'^(?:\d{1,2}\/\d{1,2})')
        id = self.id
        img_url = self.img_url
        url = response.request.url

        if date_str:
            year = date.today().year
            month, day = (int(_) for _ in date_str.split('/'))

        # Add the title to the database here

        
