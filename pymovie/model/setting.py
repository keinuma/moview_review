"""
2018/01/21 numata
SQLAlchemyの基本セッティング
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# mysqlのDB設定
DATABASE = 'mysql://{username}:{passwd}@' \
           '{host}/{db_name}?charset=utf8'

ENGINE = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=True
)

# session作成
SESSION = sessionmaker(bind=ENGINE)

# modelで使用
BASE = declarative_base()
BASE.query = SESSION.query_property()