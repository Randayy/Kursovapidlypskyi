from django.urls import path
from . import views

urlpatterns = [
    path("scholar/", views.scholar, name="scholar"),
    # path("/", views.index, name="index"),
    path("search/", views.search_scholar, name="search_scholar"),
    path('scholar_detail/<int:scholar_id>/', views.scholar_detail, name='scholar_detail'),
]
