"""
2018/02/23
クローリング結果をデータベースに接続する
"""

from ..model import SESSION
from ..model import Movie, Review


class CrawlmoviePipeline(object):
    """
    データベースにデータを保存するクラス
    """
    def __init__(self):
        """
        スパイダー開始時にデータベース接続
        :return:
        """
        self.session = SESSION()

    def close_spider(self):
        """
        スパイダー終了時に実行
        :return:
        """
        self.session.close()

    def process_item(self, item, spider):
        return item
