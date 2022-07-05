from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.MoviesListApi.as_view(), name='movies'),
    path('movies/<uuid:pk>', views.MoviesDetailApi.as_view(), name='movie-detail'),
]
