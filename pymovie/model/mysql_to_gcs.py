"""
2018/02/11
MysqlデータベースからGCSにアップロード
"""

import os
import json
import datetime
from google.cloud import storage
from .model import Review
from .setting import SESSION


def select_review_json():
    """
    mysqlから映画レビューデータを抽出
    :return None:
    """
    session = SESSION()
    column = (Review.code, Review.movie_code, Review.content,
              Review.points, Review.empathy)
    data = [{
        "code": review[0],
        "movie_code": review[1],
        "content": review[2],
        "points": review[3],
        "empathy": review[4]
    } for review in session.query(*column).all()]
    data_str = json.dumps(data).encode("utf-8")
    return data_str


def upload_gs(name, file_name, data):
    """
    jsonファイルをgcsにアップロード
    :param str data:
    :param str name:
    :param file file_name:
    :return None:
    """
    client = storage.Client()
    bucket = client.get_bucket(name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(data=data, content_type="text/json")
    return None


def main():
    """
    メイン処理
    :return:
    """
    now = datetime.datetime.now().strftime("%Y%m%d")
    file_name = now + ".json"

    data = select_review_json()
    upload_gs("pynltk/movie_review", file_name, data)


if __name__ == "__main__":
    main()
