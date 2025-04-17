import scrapy
import redis
import json
import time
import re

from datetime import date

from database.db import Session
from database.models import Title

r = redis.Redis('localhost', port=6379)

class CmoaSpider(scrapy.Spider):
    name = 'cmoa'
    start_urls = [
        'https://www.cmoa.jp/newrelease/schedule/?page=1',
        'https://www.cmoa.jp/newrelease/schedule/?page=2',
        'https://www.cmoa.jp/newrelease/schedule/?page=3',
        'https://www.cmoa.jp/newrelease/schedule/?page=4',
        'https://www.cmoa.jp/newrelease/schedule/?page=9',
    ]

    def parse(self, response):
        for title in response.css('li.title_wrap'):
            if title.css('div.vol_num::text').re(r'^1(?:-\d+)?\D.*$'):
                item = {
                    'img': f'https:{title.css('img::attr(src)').get()}',
                    'id': title.css('a::attr(href)').re_first(r'/title/(\d+)/')
                }

                r.set('update_timestamp', time.time())
                r.rpush('titles', json.dumps(item))


class CmoaAdditionalInfoSpider(scrapy.Spider):
    name = 'cmoa_additional_info'

    def parse(self, response):
        date_str = response.css('div.nextReleaseBox.this p.date::text').get()

        yield {
            'id': self.id,
            'url': response.request.url,
            'img_url': self.img_url,
            'release_date': date_str
        }


        
