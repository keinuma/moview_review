"""
2017/11/19 numata
crawling movie review and save in database.
"""

import os
import time
import requests
from bs4 import BeautifulSoup

from ..model import SESSION
from ..model import Movie, Review
from ..helper import init_getter


def scrape_ranking(base_url, movie_num=1, init_page=1):
    """
    :param base_url: string 基本URL
    :param movie_num: int スクレピングする映画数
    :param init_page: int スクレイピング開始のページ

    :return movie: dict - 映画ディクショナリのジェネレータ
    """
    # 1ページあたり映画数10
    page_num = movie_num // 10
    page_range = range(init_page, init_page + page_num + 1)
    last = movie_num % 10

    for page in page_range:
        url = os.path.join(base_url, str(page))
        session = requests.Session()
        response = session.get(url)
        if response.status_code >= 400:
            raise Exception(response.status_code)
        # ランキングの集合を取得
        rank_boxes = BeautifulSoup(
            response.text,
            "html5lib"
        ).find_all("div", class_="rankBox")
        for i, rank_box in enumerate(rank_boxes):
            # 目標の映画数を取得したら終了
            if page == max(page_range) and i == last:
                break
            head4 = rank_box.find("h4")
            movie = dict(
                code=head4.a.get("href").split("/")[2],
                title=head4.a.text,
                open_date=rank_box.p.text)
            yield movie


def scrape_review(movie, base_url, review_num=1, init_page=1):
    """
    :param movie: dict - 映画ディクショナリ
    :param base_url: str - レビューの詳細ページ
    :param review_num: int - スクレイピングをするレビュー数
    :param init_page: int - スタートページ

    :return review: dict - レビューのジェネレータ
    """
    temp_url = os.path.join(base_url, movie['code'])
    # 1ページあたりのレビュー数20
    page_num = review_num // 20
    page_range = range(init_page, init_page + page_num + 1)
    last = review_num % 20

    for page in page_range:
        url = os.path.join(temp_url, 'review/all', str(page))
        session = requests.Session()
        response = session.get(url)
        if response.status_code >= 400:
            raise Exception(response.status_code)
        content = BeautifulSoup(response.text, "html5lib")
        reviews = content.find_all("div", class_="review")

        for i, review in enumerate(reviews):
            if page == max(page_range) and i == last:
                break
            reviewer_m = review.find("div", class_="reviewer_m")
            empathy = reviewer_m.find("li", class_="btEmpathy").find("span")
            # ネタバレページはjavascriptのためスキップ
            if "本文にネタバレがあります。" in review.find("p").text:
                continue
            movie_review = dict(
                code=review.h3.a.get("href").split("/")[4],
                movie_code=movie["code"],
                points=reviewer_m.dl.find("strong").text,
                content=review.find("p").text,
                empathy=empathy.text.split(" ")[1]
            )
            if movie_review['points'] == '-':
                movie_review['points'] = 0
            time.sleep(1)
            yield movie_review


def save_movie(data, session):
    """
    :param data: dict - 映画ディクショナリ
    :param session: sqlalchemy.session - データベースセッション
    :return: None
    """
    movie = Movie(**data)
    session.add(movie)
    session.commit()
    return None


def save_reviews(data, session, saved=None):
    """
    :param data: generator(dict) - レビューのジェネレータ
    :param session: sqlalchemy.session - データベースセッション
    :param saved: list - すでに登録されてあるレビューコードのリスト
    :return: None
    """
    reviews = []
    for review_dic in data:
        if int(review_dic['code']) in saved:
            continue
        review = Review(**review_dic)
        reviews.append(review)
    session.add_all(reviews)
    session.commit()
    return None


def main(start=(1, 3), movie_num=5, review_num=10):
    """
    クローラのメイン処理
    """
    # ランキングページをクローリングする
    base_url_rank = "http://www.eiga.com/movie/review/ranking/"
    base_url_review = "http://www.eiga.com/movie/"

    # データベースのセッション作成
    session = SESSION()
    # 登録されている映画のコードを取得
    movie_code_saved = init_getter(session=session, column=Movie.code)
    review_code_saved = init_getter(session=session, column=Review.code)
    movies_gene = scrape_ranking(base_url_rank,
                                 movie_num=movie_num,
                                 init_page=start[0])

    # レビューページをクローリングする
    for movie in movies_gene:
        print("=" * 20)
        print("start movie: {}".format(movie))
        # 映画がmasterに登録されていなければ、insert
        if int(movie['code']) not in movie_code_saved:
            save_movie(movie, session)
        time.sleep(1)
        reviews = scrape_review(movie,
                                base_url_review,
                                review_num=review_num,
                                init_page=start[1])
        save_reviews(reviews, session, saved=review_code_saved)


if __name__ == "__main__":
    main()
