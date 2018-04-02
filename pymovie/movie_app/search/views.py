from django.template.response import TemplateResponse
from elasticsearch import Elasticsearch

from .models import Movie


def index(request):
    if request.method == 'POST':
        es = Elasticsearch()
        word = request.POST['word']
        search_body = {'query': {'match': {'description': word}}}
        response = es.search(index='movies', body=search_body, size=1000)
        source = [x['_source'] for x in response['hits']['hits'] if x['_score'] > 2.0]
        context = {
            'movies': source,
            'word': word,
            'post': 1,
        }
        return TemplateResponse(request, 'index.html', context=context)
    else:
        context = {'post': 0}
        return TemplateResponse(request, 'index.html', context=context)


def content(request, movie_code):
    movie = Movie.objects.get(movie_code=movie_code)
    context = {'movie': movie}
    return TemplateResponse(request, 'content.html', context=context)
