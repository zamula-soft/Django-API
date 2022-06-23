from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.api),
]
