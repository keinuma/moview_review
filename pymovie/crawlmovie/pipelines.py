"""
2018/02/23
クローリング結果をデータベースに接続する
"""

from scrapy.exceptions import DropItem
from pymongo import MongoClient


class ValidationPipeline(object):
    """
    クロールできなかったitem削除
    """
    def process_item(self, item, spider):
        if not item['code']:
            raise DropItem
        return item


class CrawlmoviePipeline(object):
    """
    データベースにデータを保存するクラス
    """
    def open_spider(self, spider):
        """
        スパイダー開始時にデータベース接続
        :return:
        """
        settings = spider.settings
        params = {
            'host': settings.get('HOST', 'localhost'),
            'port': settings.get('PORT', 27017)
        }
        self.client = MongoClient(**params)
        self.db = self.client[settings['DB']]
        self.collection_movie = self.db[settings['COLLECTION_MOVIE']]
        self.collection_review = self.db[settings['COLLECTION_REVIEW']]

    def close_spider(self, spider):
        """
        スパイダー終了時に実行
        :return:
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        itemをデータベースに保存
        :param item:
        :param spider:
        :return:
        """
        if spider.name == 'movies':
            self.collection_movie.update(
                {'code': item['code']},
                {'$set': dict(item)},
                upsert=True
            )
        elif spider.name == 'reviews':
            self.collection_review.update(
                {'code': item['code']},
                {'$set': dict(item)},
                upsert=True
            )
        return item
