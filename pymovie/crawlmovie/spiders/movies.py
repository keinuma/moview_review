"""
2018/02/20
movieページのspiderクラス
"""

import re
import scrapy

from ..items import MoviePage


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['eiga.com']
    start_urls = ['http://eiga.com/movie/review/ranking/']
    movie_url = 'http://eiga.com/'

    def parse(self, response):
        """
        映画ランキングページ一覧を取得する
        :param response:
        :return:
        """
        for i in range(1, 11):
            i = str(i)
            yield scrapy.Request(response.urljoin(i), self.parse_rank)

    def parse_rank(self, response):
        """
        映画ランキングページ欄からリンクを取得する
        :param response:
        :return:
        """
        for movie in response.css("div.rankBox h4 a::attr('href')").re(r'/movie/\d+/$'):
            url = self.movie_url + movie
            yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        """
        映画の詳細ページの取得
        :param response:
        :return:
        """
        item = MoviePage()
        item['code'] = re.search('\d+', response.url)[0]
        item['title'] = response.css('div.moveInfoBox > h1::text').extract_first()
        item['open_date'] = response.css('span.opn_date > strong::attr("content")').extract_first()
        item['description'] = response.css('div.outline > p::text').extract_first()
        item['director'] = response.css('dd.f > a > span::text').extract_first()
        yield item
