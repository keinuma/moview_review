from django.db import models


class Movie(models.Model):
    """
    映画モデル:
        code: int - 主キー
        title: string - 映画タイトル
        open_date: datetime - 公開日
        created: datetime - 作成日
    """
    movie_code = models.IntegerField('映画コード', primary_key=True)
    title = models.CharField('映画タイトル', max_length=500)
    open_date = models.CharField('公開日', max_length=20)
    description = models.CharField('概要', max_length=1000)
    director = models.CharField('監督', max_length=30)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    レビューモデル:
        code: int - 主キー
        movie_code: int - 映画モデルのキー
        points: int - 映画の評価点
        content: sting - 映画レビュー
        empathy: string - レビューの共感度
        created: datetime - 作成日
    """
    review_code = models.IntegerField('レビューコード', primary_key=True)
    movie_code = models.ForeignKey(Movie, on_delete=models.CASCADE)
    points = models.FloatField('評価点', default=0.0)
    content = models.CharField('レビュー', max_length=500)
    empathy = models.FloatField('共感点', default=0.0)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.review_code


class Analyzed(models.Model):
    """
    レビューモデル:
        code: int - 主キー
        magnitude: float - 感情の振れ幅
        score: float - 感情
    """
    review_code = models.ForeignKey(Review, on_delete=models.CASCADE)
    magnitude = models.FloatField('感情振幅', default=0.0)
    score = models.FloatField('感情指数', default=0.0)
