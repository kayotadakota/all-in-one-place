import redis
import json
import time

from crochet import setup, run_in_reactor
setup()

from flask import Blueprint, render_template, jsonify, request, Response

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from cmoa.spiders.cmoa_spider import CmoaSpider, CmoaAdditionalInfoSpider


main_bp = Blueprint('main', __name__)
r = redis.Redis(host='localhost', port=6379)


@run_in_reactor
def run_cmoa():
    process = CrawlerProcess(get_project_settings())
    process.crawl(CmoaSpider)


@run_in_reactor
def get_additional_info(id, img_url):
    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {
            'cmoa.pipelines.CmoaPipeline': 300,
        }
    })
    process.crawl(
        CmoaAdditionalInfoSpider,
        start_urls=[f'https://www.cmoa.jp/title/{id}'],
        id=id,
        img_url=img_url
    )


@main_bp.route('/')
def index():
    cache_timeout = 86400 # 24 hours
    now = time.time()
    last_data_update = r.get('update_timestamp')

    if not last_data_update or now - float(last_data_update) > cache_timeout:
        run_cmoa()

    cmoa_results()
    return render_template('index.html')


@main_bp.route('/cmoa')
def cmoa_results():
    titles = r.lrange('titles', 0, -1)
    if titles:
        titles = [json.loads(title) for title in titles]
        return jsonify({'ready': True, 'data': titles})
    return jsonify({'ready': False})


@main_bp.route('/add', methods=['POST'])
def add_info():
    data = request.get_json()
    title_id = data['id']
    img_url = data['img_url']
    get_additional_info(title_id, img_url)
    return Response('OK', status=201)

# run the script after 12 p.m.
# if a cover looks profitable click on the 'add' button and the app will make a request for additional info and save it to the database.