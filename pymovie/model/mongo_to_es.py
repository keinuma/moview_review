"""
2018/03/02
"""

from elasticsearch import Elasticsearch

from ..helper import mongo_conn
from ..config import ELASTIC


def define_index(es):
    """
    elasticsearchのindexを作成
    :param es: elasticsearch.Elasticsearch
    :return:
    """
    response = es.indices.create(
        index='movies',
        ignore=400,
        body={
            "mappings": {
                "movie": {
                    # _allは全フィールドを結合
                    "_all": {
                        "analyzer":
                            "kuromoji_analyzer"
                    },
                    "properties": {
                        "code": {
                            "type": "integer",
                        },
                        "title": {
                            "type": "string",
                            "analyzer": "kuromoji_analyzer"
                        },
                        "director": {
                            "type": "string",
                            "analyzer": "kuromoji_analyzer"
                        },
                        "description": {
                            "type": "string",
                            "analyzer": "kuromoji_analyzer"
                        }
                    }
                }
            }
        }
    )
    return response


def mongo_setting():
    """
    json型の映画データをMongoから取得
    :return dict data: 映画データ
    """
    col = mongo_conn('movie')
    return col.find(
        {},
        {
            'title': 1,
            'director': 1,
            'description': 1,
            'code': 1,
            '_id': 0
        }
    )


def load_to_es(data, es):
    """
    dataをElasticsearchに投入
    :param dict data: 辞書型データ
    :param es:
    :return:
    """
    for i in data:
        result = es.index(
            index='movies',
            doc_type='movie',
            body=i
        )
        print(result)


def main():
    es = Elasticsearch([ELASTIC['CONN']])
    temp = define_index(es)
    print('define es index: {}'.format(temp))
    data = mongo_setting()
    load_to_es(data, es)


if __name__ == '__main__':
    main()
