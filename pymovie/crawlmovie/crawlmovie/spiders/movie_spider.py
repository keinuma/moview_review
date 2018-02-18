
"""
2018/02/18 numata
映画.comの映画情報を取得するSpiderクラス
"""


from scrapy import Spider
# from ..items import MoviePage, ReviewPage


class MovieSpider(Spider):

    name = 'movie'
    start_urls = (
        'http://eiga.com/movie/ranking/review/'
    )

    def parse(self, response):
        """
        映画.comのランキングページをパースする
        :param response:
        :return:
        """
        print(response)
