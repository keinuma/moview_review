"""
2017/11/19 numata
crawling movie review and save in database.
"""

import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


class Movielib(object):
    """
    code: primary key for each movie
    name: movie title
    rank: movie ranking
    date: open date
    """

    def __init__(self, code, title, rank, date):
        self.movie = {"code": code,
                      "title": title,
                      "rank": rank,
                      "date": date,
                      "reviews": []}

    def __repr__(self):
        return "Movie name: {}.".format(self.movie["title"])

    def review_url(self, baseurl):
        """make review url"""
        url = baseurl + self.movie["code"] + "/review/all/"
        return url

    def set_review(self, code, points, content, empathy):
        """
        code: review code
        points: evalution
        content: review text
        empathy: number of empathy
        """
        review = {"code": code,
                  "points": points,
                  "content": content,
                  "empathy": empathy}
        codes = {x["code"] for x in self.movie["reviews"]}
        if code not in codes:
            self.movie["reviews"].append(review)


def scrape_ranking(base_url, page_number):
    """
    base_url: base url for crawling
    page_number: page number integer
    """
    for page in range(1, page_number + 1):
        url = base_url + str(page)
        session = requests.Session()
        response = session.get(url)
        if response.status_code >= 400:
            raise Exception(response.status_code)
        # ランキングの集合を取得
        rankboxes = BeautifulSoup(response.text,
                                  "html5lib").find_all("div", class_="rankBox")
        for rankbox in rankboxes:
            head4 = rankbox.find("h4")
            movie = Movielib(
                head4.a.get("href").split("/")[2],
                head4.a.text,
                head4.span.text,
                rankbox.p.text)
            yield movie


def scrape_review(movie, page_num):
    """
    movie: Movielib()
    """
    review_url = movie.review_url("http://www.eiga.com/movie/")
    for page in range(1, page_num + 1):
        url = review_url + str(page)
        session = requests.Session()
        response = session.get(url)
        if response.status_code >= 400:
            raise Exception(response.status_code)
        content = BeautifulSoup(response.text, "html5lib")
        reviews = content.find_all("div", class_="review")
        reviewboxes = content.find_all("div", class_="review pro") + reviews

        for review in reviewboxes:
            reviewer_m = review.find("div", class_="reviewer_m")
            empathy = reviewer_m.find("li", class_="btEmpathy").find("span")
            movie.set_review(
                review.h3.a.get("href").split("/")[4],
                reviewer_m.dl.find("strong").text,
                review.find("p").text,
                empathy.text.split(" ")[1]
            )
            print(movie.movie["reviews"])
            time.sleep(1)


def main():
    """
    クローラのメイン
    """
    # MongoDBのクライアント取得
    client = MongoClient("localhost", 27017)
    collection = client.nltk.eiga  # nltkデータベースのeigaコレクションを得る
    collection.create_index("code", unique=True)

    # ランキングページをクローリングする
    base_url = "http://www.eiga.com/movie/review/ranking/"
    movies_gene = scrape_ranking(base_url, 1)

    # レビューページをクローリングする
    for movie in movies_gene:
        time.sleep(1)
        scrape_review(movie, 5)
        collection.insert_one(movie.movie)
        print(movie)


if __name__ == "__main__":
    main()
