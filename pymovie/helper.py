"""
2018/02/18 numata
ヘルパー関数定義
"""

from pymongo import MongoClient
from .config import MONGO


def init_getter(session, column):
    """
    column一つの結果を一次元リストに変更
    :param session: DBのsessionインスタンス
    :param column: DBのカラム
    :return list data:
    """
    data = (x[0] for x in session.quey(column).all())
    return data


def mongo_conn(collection):
    """
    MongoDBから指定のコレクションを取得する
    :param str collection: MongDBのコレクション文字列
    :return:
    """
    params = {
        'host': MONGO['HOST'],
        'port': MONGO['PORT']
    }
    client = MongoClient(**params)
    db = client[MONGO['DB']]
    if collection == 'movie':
        col = db[MONGO['COLLECTION_M']]
    elif collection == 'review':
        col = db[MONGO['COLLECTION_R']]
    else:
        raise Exception('Not found mongo collection')
    return col
