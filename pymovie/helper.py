"""
2018/02/18 numata
ヘルパー関数定義
"""


def init_getter(session, column):
    """
    column一つの結果を一次元リストに変更
    :param session: DBのsessionインスタンス
    :param column: DBのカラム
    :return list data:
    """
    data = (x[0] for x in session.quey(column).all())
    return data
