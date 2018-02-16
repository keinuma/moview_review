"""
2018/02/16 numata
感情分析の解析結果をレポーティングする
"""

from ..model.model import Analyzed, Review
from ..model.setting import SESSION

def get_data():
    """
    MySQLから自然言語処理解析結果の集計を行う
    :return:
    """
    session = SESSION()
    data = session.query(Analyzed.code, Analyzed.score)
    return data

