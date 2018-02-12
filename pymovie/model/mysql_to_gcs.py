"""
2018/02/11
MysqlデータベースからGCSにアップロード
"""

import os
import json
import datetime
from google.cloud import storage
from google.cloud import bigquery
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
    data = ({
        "code": review[0],
        "movie_code": review[1],
        "content": review[2],
        "points": review[3],
        "empathy": review[4]
    } for review in session.query(*column).all())
    data_str = ""
    for d in data:
        dj = json.dumps(d)
        data_str += dj + "\n"
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
    return bucket, blob


def load_bq_from_gs(data_set_name, table_name, source):
    """
    GCSからBigqueryへロードする
    :param str data_set_name:
    :param str table_name:
    :param str source:
    :return:
    """
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = "NEWLINE_DELIMITED_JSON"
    job_config.write_disposition = "WRITE_TRUNCATE"

    client = bigquery.Client()
    data_set = client.dataset(data_set_name)
    table = data_set.table(table_name)

    load_job = client.load_table_from_uri(
        source,
        table,
        job_config=job_config
    )

    load_job.result()
    print("Loaded {} rows into {}:{}".format(
        load_job.output_rows, data_set_name, table_name
    ))


def main():
    """
    メイン処理
    :return:
    """
    now = datetime.datetime.now().strftime("%Y%m%d")
    file_name = now + ".json"
    file_path = os.path.join("movie_review", file_name)

    data = select_review_json()
    bucket, blob = upload_gs("pynltk", file_path, data)
    bucket_uri = "gs://{}/{}".format(bucket.name, file_path)

    load_bq_from_gs("moviereview", "review", bucket_uri)


if __name__ == "__main__":
    main()
