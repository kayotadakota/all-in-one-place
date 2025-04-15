import redis
import json
import time

from crochet import setup, run_in_reactor
setup()

from flask import Flask, render_template, jsonify, request

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#import database
from database.db import Session
from database.models import Titles
from cmoa.cmoa.spiders.cmoa_spider import CmoaSpider, CmoaAdditionalInfoSpider


app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)


@run_in_reactor
def run_cmoa():
    process = CrawlerProcess(get_project_settings())
    process.crawl(CmoaSpider)
    # process.start()


@run_in_reactor
def get_additional_info(id, img_url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        CmoaAdditionalInfoSpider,
        start_urls=[f'https://www.cmoa.jp/title/{id}'],
        id=id,
        img_url=img_url
    )


@app.route('/')
def index():
    cache_timeout = 86400 # 24 hours
    now = time.time()
    last_data_update = r.get('update_timestamp')

    if not last_data_update or now - float(last_data_update) > cache_timeout:
        run_cmoa()

    cmoa_results()
    #titles = [json.loads(item) for item in r.lrange('titles', 0, -1)]
    return render_template('index.html')


@app.route('/cmoa')
def cmoa_results():
    titles = r.lrange('titles', 0, -1)

    if titles:
        titles = [json.loads(title) for title in titles]
        return jsonify({'ready': True, 'data': titles})
    return jsonify({'ready': False})
    #titles = [json.loads(item) for item in r.lrange('titles', 0, -1)]


@app.route('/add', methods=['POST'])
def add_info():
    data = request.get_json()
    title_id = data['id']
    img_url = data['img_url']
    get_additional_info(title_id, img_url)

# run the script after 12 p.m.
# if a cover looks profitable click on the 'add' button and the app will make a request for additional info and save it to the database.