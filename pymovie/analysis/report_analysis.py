"""
2018/02/16 numata
感情分析の解析結果をレポーティングする
"""

import pandas as pd
from ..model.model import Analyzed, Review, Movie
from ..model.setting import SESSION


def get_data():
    """
    MySQLから自然言語処理解析結果の集計を行う
    :return list data: クエリ結果
    """
    session = SESSION()
    data = session.query(
        Analyzed.score, Review.code, Movie.code, Movie.title
    ).join(
        Review, Analyzed.code == Review.code
    ).join(
        Movie, Movie.code == Review.movie_code
    ).all()
    data = pd.DataFrame(
        data,
        columns=['score', 'review_code', 'movie_code', 'movie_title']
    )
    return data


def sep_by_movie(data):
    """
    各映画ごとの感情分析のグラフを作成
    :param pd.DataFrame data: 映画データ
    :return:
    """
    movies = {x for x in data['movie_code']}
    for movie_code in movies:
        yield data[data['movie_code'] == movie_code]


def make_graph():
    """
    映画ごとに集計結果を可視化
    :return:
    """
    data_set = get_data()
    data = sep_by_movie(data_set)
    return data
