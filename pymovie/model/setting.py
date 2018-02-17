"""
2018/01/21 numata
SQLAlchemyの基本セッティング
"""

import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..helper import load_config


# mysqlのDB設定
DATABASE = 'mysql+pymysql://{username}:{password}@' \
           '{host}/{db_name}?charset=utf8mb4'


CONFIG_PATH = pathlib.Path(__file__)

config = load_config(path=CONFIG_PATH.parents[1])
DATABASE = DATABASE.format_map(config)

ENGINE = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=True
)

# session作成
SESSION = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE))

# modelで使用
BASE = declarative_base()
BASE.query = SESSION.query_property()
