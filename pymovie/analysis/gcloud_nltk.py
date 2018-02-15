"""
2018/02/11
GCPから映画レビューの翻訳および感情分析を行う
"""


import time
from google.cloud import bigquery
from google.cloud import translate
from google.cloud import language

from ..model.model import Analyzed
from ..model.setting import SESSION


def load_data(client, query):
    """
    BigQueryからデータをロードする
    :param google.cloud client:
    :param str query: 発行するクエリ
    :return:
    """
    job = client.query(query=query)
    data = job.result()
    return data


def translate_review(client, jp_text):
    """
    GCPから映画レビューの翻訳を行う
    :param google.cloud client:
    :param str jp_text: 日本語レビュー文章
    :return str en_content: 英語に翻訳後の文章
    """
    translation = client.translate(
        jp_text,
        target_language="en"
    )
    return translation["translatedText"]


def analysis_review(client, content):
    """
    英語の映画レビューの感情分析を行う
    :param google.cloud client:
    :param str content: 英語レビュー文章
    :return list sentiment: 感情分析結果(JSON)
    """
    document = language.types.Document(
        content=content,
        language="en",
        type="PLAIN_TEXT"
    )
    response = client.analyze_sentiment(
        document=document,
        encoding_type="UTF32"
    )
    sentiments = response.document_sentiment
    return sentiments


def save_analysis(data_set):
    """
    :param list data_set: 感情分析結果のリスト
    :return:
    """
    session = SESSION()
    saved = session.query(Analyzed.code).all()
    analyzed_list = []
    for code, score in data_set:
        if int(code) in saved:
            continue
        temp = {
            "code": code,
            "magnitude": score.magnitude,
            "score": score.score
        }
        analyzed = Analyzed(**temp)
        analyzed_list.append(analyzed)
    session.add_all(analyzed_list)
    session.commit()
    return None


def main():
    """
    メイン処理
    :return:
    """
    query = """
    select code, content from moviereview.review limit 50
    """
    big_client = bigquery.Client()
    data = load_data(big_client, query)
    result = []
    trans_client = translate.Client()
    lang_client = language.LanguageServiceClient()
    for i, code_content in enumerate(data):
        print(code_content[1])
        if len(code_content[1]) > 500:
            continue
        en_text = translate_review(trans_client, code_content[1])
        analyzed = analysis_review(lang_client, en_text)
        result.append((code_content[0], analyzed))
        print(analyzed)
        if i > 10:
            break
        time.sleep(1)
    save_analysis(result)
    return result


if __name__ == "__main__":
    main()
