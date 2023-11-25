from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("scholar/", views.scholar, name="scholar"),
    # path("/", views.index, name="index"),
    path("search/", views.search_scholar, name="search_scholar"),
    path(
        "scholar_detail/<int:scholar_id>/", views.scholar_detail, name="scholar_detail"
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
