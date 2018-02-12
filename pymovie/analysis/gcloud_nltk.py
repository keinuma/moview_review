"""
2018/02/11
GCPから映画レビューの翻訳および感情分析を行う
"""


from google.cloud import bigquery
from google.cloud import translate
from google.cloud import language


def load_data(query):
    """
    BigQueryからデータをロードする
    :param str query: 発行するクエリ
    :return:
    """
    client = bigquery.Client()
    job = client.query(query=query)
    data = job.result()
    return data


def translate_review(jp_text):
    """
    GCPから映画レビューの翻訳を行う
    :param str jp_text: 日本語レビュー文章
    :return str en_content: 英語に翻訳後の文章
    """
    client = translate.Client()
    translation = client.translate(
        jp_text,
        target_language="en"
    )
    return translation["translatedText"]


def analysis_review(content):
    """
    英語の映画レビューの感情分析を行う
    :param str content: 英語レビュー文章
    :return list sentiment: 感情分析結果(JSON)
    """
    client = language.LanguageServiceClient()
    document = language.types.Document(
        content=content,
        language="en",
        type="PLAIN_TEXT"
    )
    response = client.analyze_entity_sentiment(
        document=document,
        encoding_type="UTF32"
    )
    sentiments = [
        (x.name, x.mentions[0].sentiment) for x in response.entities
        if x.mentions[0].sentiment.score != 0.
    ]
    return sentiments


def main():
    """
    メイン処理
    :return:
    """
    query = """
    select code, content from moviereview.review limit 10
    """
    data = load_data(query)
    result = []
    for _, content in data:
        en_text = translate_review(content)
        analyzed = analysis_review(en_text)
        result.append(analyzed)
    return result


if __name__ == "__main__":
    main()
