

from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='movie_index'),

    path('<int:movie_code>/', views.content, name='movie_content'),

]
