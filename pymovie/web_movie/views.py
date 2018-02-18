"""
2018/02/18
アプリケーションのVIEW定義
"""


from flask import request, redirect, url_for,render_template, flash
from ..web_movie import app, session
from ..model import Movie, Review, Analyzed


@app.route('/', methods=['GET', 'POST'])
def search():
    word = request.args.get('word')
    if word is 'None':
        word = ''
    return render_template('search_form.html', word=word)
