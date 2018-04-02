"""
2018/03/10 numata
import movie data by jsonlines
"""

import json
from django.core.management.base import BaseCommand

from ...models import Movie


class Command(BaseCommand):

    help = 'Create movie data from json lines'

    def remove_null(self, value, default):
        """
        Null値をデフォルトに変換
        :param value: 検証値
        :param default: デフォルト値
        :return :
        """
        if value is None:
            return default
        return value

    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):
        """
        コマンド実行時にcallされる
        :param args: コマンドライン引数
        :param options: キーワード引数
        """
        filename = ''.join(args)
        count = 0
        with open(filename, 'r') as f:
            txt_data = f.readlines()
        for txt_obj in txt_data:
            movie_obj = json.loads(txt_obj)

            # コードがない場合は保存しない
            if not movie_obj['code']:
                continue

            # movie保存処理
            print(len(movie_obj['description']))
            movie = Movie()
            movie.movie_code = movie_obj['code']
            movie.title = movie_obj['title']
            movie.open_date = movie_obj['open_date']
            movie.description = movie_obj['description']
            movie.director = movie_obj['director']
            movie.save()

            count += 1
            print('Create Item: {0}: {1}'.format(movie.movie_code, movie.title))
        print('{} movies have been created.'.format(count))
