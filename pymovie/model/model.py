"""
2018/01/21 numata
データベースのORM
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Unicode, DateTime, Float
from .setting import BASE


class Movie(BASE):
    """
    映画モデル:
        code: int - 主キー
        title: string - 映画タイトル
        open_date: datetime - 公開日
        created: datetime - 作成日
    """
    __tablename__ = 'm_movie'
    code = Column(Integer, primary_key=True)
    title = Column(Unicode(30))
    open_date = Column(Unicode)
    description = Column(Unicode)
    director = Column(Unicode)
    created = Column(DateTime)

    def __init__(self, code, title=None, open_date=None,
                 description=None, director=None):
        self.code = code
        self.title = title
        self.open_date = open_date
        self.description = description
        self.director = director
        self.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __repr___(self):
        return '<Movie: %r>' % self.title


class Review(BASE):
    """
    レビューモデル:
        code: int - 主キー
        movie_code: int - 映画モデルのキー
        points: int - 映画の評価点
        content: sting - 映画レビュー
        empathy: string - レビューの共感度
        created: datetime - 作成日
    """
    __tablename__ = 't_review'
    code = Column(Integer, primary_key=True)
    movie_code = Column(Integer)
    points = Column(Integer)
    content = Column(Unicode)
    empathy = Column(Integer)
    created = Column(DateTime)

    def __init__(self, code, movie_code=None, points=None,
                 content=None, empathy=None):
        self.code = code
        self.movie_code = movie_code
        self.points = points
        self.content = content
        self.empathy = empathy
        self.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Review: %r>' % self.content


class Analyzed(BASE):
    """
    レビューモデル:
        code: int - 主キー
        magnitude: float - 感情の振れ幅
        score: float - 感情
    """
    __tablename__ = 't_analyzed'
    code = Column(Integer, primary_key=True)
    magnitude = Column(Float)
    score = Column(Float)

    def __init__(self, code, magnitude=None, score=None):
        self.code = code
        self.magnitude = magnitude
        self.score = score

    def __repr__(self):
        return '<Score: %r, Magnitude: %r>' % (self.score, self.magnitude)
