from django.urls import path
from . import views

urlpatterns = [
    path("scholar/", views.scholar, name="scholar"),
    # path("/", views.index, name="index"),
    path("search/", views.search_scholar, name="search_scholar"),
]
