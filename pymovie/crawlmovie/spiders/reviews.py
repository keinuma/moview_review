"""
2018/02/25
reviewページのスクレイピング
"""

import re
from scrapy import Spider, Request
from pymongo import MongoClient

from ..settings import HOST, PORT, DB, COLLECTION_MOVIE
from ..items import ReviewPage


class ReviewsSpider(Spider):
    name = 'reviews'
    allowed_domains = ['eiga.com']
    start_urls = ['http://eiga.com/movie/review/ranking/']
    review_url = 'http://eiga.com/movie/{}/review/all/'

    def __init__(self):
        params = {
            'host': HOST,
            'port': PORT
        }
        client = MongoClient(**params)
        db = client[DB]
        collection = db[COLLECTION_MOVIE]
        self.movie_code = collection.find(
            {},
            {'code': 1, '_id': 0}
        )

    def parse(self, response):
        """
        映画コードからレビューページに移動
        :param response:
        :return:
        """
        for code in self.movie_code:
            url = self.review_url.format(code['code'])
            yield Request(url, self.parse_review)

    def parse_review(self, response):
        """
        レビューページをパース
        :param response:
        :return:
        """
        url = self.review_url.format(re.search('\d+', response.url)[0])
        for i in range(1, 11):
            i = str(i)
            url_ = url + i
            yield Request(url_, self.parse_item)

    def parse_item(self, response):
        """
        レビューページからitemを取得
        :param response:
        :return:
        """
        for review in response.css('div.review'):
            if "本文にネタバレがあります。" in review.css("p > em::text").extract_first():
                continue
            item = ReviewPage()
            item['code'] = review.css('h3 > a::attr(href)').re('\d+')[1]
            item['movie_code'] = re.search('\d+', response.url)[0]
            item['points'] = review.css('ul > li > strong::text').extract_first()
            item['content'] = review.css('p::text').extract_first()
            item['empathy'] = review.css('li.btEmpathy > span > strong::text').extract_first() or 0
            if item['points'] == '-':
                item['points'] = '0'
            yield item

