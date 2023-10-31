from django.urls import path
from . import views

urlpatterns = [
    path('scholar/', views.scholar, name='scholar'),
]
