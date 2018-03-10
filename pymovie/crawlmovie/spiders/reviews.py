"""
2018/02/25
reviewページのスクレイピング
"""

import re
from scrapy import Spider, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..settings import DATABASE
from ..models import Movie
from ..items import ReviewPage


ENGINE = create_engine(
    DATABASE,
    encoding='utf8',
    echo=True
)

# session作成
SESSION = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)


class ReviewsSpider(Spider):
    name = 'reviews'
    allowed_domains = ['eiga.com']
    start_urls = ['http://eiga.com/movie/review/ranking/']
    review_url = 'http://eiga.com/movie/{}/review/all/'

    def __init__(self):
        session = SESSION()
        self.movie_code = (
            str(x[0]) for x
            in session.query(Movie.movie_code).all()
        )

    def parse(self, response):
        """
        映画コードからレビューページに移動
        :param response:
        :return:
        """
        for code in self.movie_code:
            url = self.review_url.format(str(code))
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
            if review.css("p > em::text").extract_first():
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

