import unittest
from pymovie.crawler.crawler import scrape_ranking, scrape_review


class MyTestCase(unittest.TestCase):
    """
    クローリング処理のunittest
    """

    def setUp(self):
        self.movie_url = "http://www.eiga.com/movie/review/ranking/"
        self.review_url = "http://www.eiga.com/movie/"
        self.movies = list(scrape_ranking(self.movie_url,
                                          movie_num=2,
                                          init_page=4))

    def test_scrape_ranking(self):
        """
        映画のクローリング処理テスト
        指定した数だけクロールしているか
        :return:
        """
        self.movies = list(scrape_ranking(self.movie_url,
                                          movie_num=2,
                                          init_page=4))
        self.assertEqual(2, len(self.movies))

    def test_scrape_review(self):
        """
        レビューのクローリング処理テスト
        指定した数だけクロールしているか
        :return:
        """
        reviews = list(scrape_review(self.movies[0],
                                     self.review_url,
                                     review_num=4,
                                     init_page=5))
        self.assertEqual(4, len(reviews))


if __name__ == '__main__':
    unittest.main()
