"""
2018/02/17
ヘルパー関数
"""

import json
import pathlib


def load_config(path=pathlib.os.getcwd(), filename='config.json'):
    """
    認証情報の読み込み
    :param pathlib.Path path: 認証情報のJSONが保持されているディレクトリ
    :param str filename: 認証データのJSONファイル名
    :return:
    """
    path = pathlib.Path(path)
    file_path = path.joinpath(filename)
    with open(file_path, 'r') as f:
        auth = json.load(f)
    return auth
