# -*- coding: utf-8 -*-
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['eiga.com']
    start_urls = ['http://eiga.com/movie/review/ranking/']

    def parse(self, response):
        """
        映画ランキングページ欄からリンクを取得する
        :param response:
        :return:
        """
        # rank01 > h4 > a
        for url in response.css('#rank01 > h4 > a').re(r'/movie/\d+$'):
            yield scrapy.Request(response.urljoin(url), self.parse_rank)

    def parse_rank(self, response):
        """
        映画の詳細ページの取得
        :param response:
        :return:
        """
        pass
