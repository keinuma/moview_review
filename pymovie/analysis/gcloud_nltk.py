"""
2018/02/11
GCPから映画レビューの翻訳および感情分析を行う
"""


from google.cloud import bigquery
from google.cloud import translate
from google.cloud import language


def translate_review(client, jp_text):
    """
    GCPから映画レビューの翻訳を行う
    :param google.cloud client: APIクライアントオブジェクト
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
    :param google.cloud client: APIクライアントオブジェクト
    :param str content: 英語レビュー文章
    :return dict result: 感情分析結果(JSON)
    """
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
        (x["name"], x["sentiment"]) for x in response
    ]
    return sentiments


def main():
    """
    メイン処理
    :return:
    """
    trans_client = translate.Client()
    analyze_client = language.LanguageServiceClient()
