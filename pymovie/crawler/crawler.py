"""
2017/11/19 numata
crawling movie review and save in database.
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from ..model import setting, model


def scrape_ranking(base_url, page_number):
    """
    :param base_url: 映画の見出しページ
    :param page_number: スクレイピングするページ数

    :return movie: dict - 映画ディクショナリのジェネレータ
    """
    for page in range(1, page_number + 1):
        url = base_url + str(page)
        session = requests.Session()
        response = session.get(url)
        if response.status_code >= 400:
            raise Exception(response.status_code)
        # ランキングの集合を取得
        rank_boxes = BeautifulSoup(
            response.text,
            "html5lib"
        ).find_all("div", class_="rankBox")
        for rank_box in rank_boxes:
            head4 = rank_box.find("h4")
            movie = dict(
                code=head4.a.get("href").split("/")[2],
                title=head4.a.text,
                rank=head4.span.text,
                open_date=rank_box.p.text)
            yield movie


def scrape_review(movie, base_url, page_num=0):
    """
    :param movie: dict - 映画ディクショナリ
    :param base_url: str - レビューの詳細ページ
    :param page_num: int - スクレイピングを行うページ数

    :return review: dict - レビューのジェネレータ
    """
    for page in range(1, page_num + 1):
        url = os.path.join(base_url + str(page))
        session = requests.Session()
        response = session.get(url)
        if response.status_code >= 400:
            raise Exception(response.status_code)
        content = BeautifulSoup(response.text, "html5lib")
        reviews = content.find_all("div", class_="review")
        review_boxes = content.find_all("div", class_="review pro") + reviews

        for review in review_boxes:
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
            time.sleep(1)
            yield movie_review


def save_movie(data, session):
    """
    :param data: dict - 映画ディクショナリ
    :param session: sqlalchemy.session - データベースセッション
    :return: None
    """
    movie = model.Movie(**data)
    session.add(movie)
    session.commit()
    return None


def save_reviews(data, session):
    """
    :param data: generator(dict) - レビューのジェネレータ
    :param session: sqlalchemy.session - データベースセッション
    :return: None
    """
    reviews = []
    for review_dic in data:
        review = model.Review(**review_dic)
        reviews.append(review)
    session.add_all(reviews)
    session.commit()
    return None


def main():
    """
    クローラのメイン処理
    """
    # ランキングページをクローリングする
    base_url_rank = "http://www.eiga.com/movie/review/ranking/"
    base_url_review = "http://www.eiga.com/movie/"

    # データベースのセッション作成
    session = setting.SESSION()
    # すでに登録されている映画のコードを取得
    movie_code_saved = session.query(model.Movie.code).all()
    movies_gene = scrape_ranking(base_url_rank, 2)

    # レビューページをクローリングする
    for movie in movies_gene:
        print("=" * 20)
        print("start movie: {}".format(movie))
        # 映画がmasterに登録されていなければ、insert
        if movie['code'] not in movie_code_saved:
            save_movie(movie, session)
        time.sleep(1)
        reviews = scrape_review(movie, base_url_review, 1)
        save_reviews(reviews, session)


if __name__ == "__main__":
    main()
