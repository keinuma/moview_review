from .web_movie import app


if __name__ == '__main__':
    app.run(host='127.0.0.2', port=8000, debug=True)
