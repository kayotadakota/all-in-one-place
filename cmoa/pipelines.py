# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from datetime import date

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from database.db import Session
from database.models import Title


class CmoaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('release_date'):
            id = adapter.get('id')
            url = adapter.get('url')
            img_url = adapter.get('img_url')
            release_date = re.match(r'^(?:\d{1,2}\/\d{1,2})', adapter.get('release_date').strip())

            if not release_date:
                raise DropItem('Missing release date')
            
            month, day = (int(_) for _ in release_date.group(0).split('/'))
            year = date.today().year
            
            title = Title(id=id, url=url, img_url=img_url, release_date=date(year, month, day))
            
            with Session.begin() as session:
                print(session)
                session.add(title)

        return item
