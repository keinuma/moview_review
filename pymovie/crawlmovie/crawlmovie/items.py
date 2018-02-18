"""
2018/02/18 numata
クローリングのItemクラス
"""

from scrapy import Item
from scrapy import Field


class MoviePage(Item):
    """
    映画.comの映画情報
    """

    code = Field()
    title = Field()
    open_date = Field()


class ReviewPage(Item):
    """
    映画.comのレビュー情報
    """

    code = Field()
    movie_code = Field()
    points = Field()
    content = Field()
    empathy = Field()
