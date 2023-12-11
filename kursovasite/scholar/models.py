from django.db import models


class MyData(models.Model):
    full_name = models.CharField(max_length=100)
    google_scholar_id = models.CharField(max_length=100)
    interest_list = models.CharField(max_length=1000)
    sub_title = models.CharField(max_length=1000, default="", blank=True)
    email = models.CharField(max_length=1000, default="", blank=True)
    image = models.URLField(blank=True, null=True)
    h_index = models.CharField(max_length=100, default="", blank=True, null=True)
    article_list = models.CharField(max_length=5000, default="", blank=True, null=True)
    article_url_list = models.CharField(
        max_length=5000, default="", blank=True, null=True
    )
    citations = models.CharField(max_length=100, default="", blank=True, null=True)
    i10_index = models.CharField(max_length=100, default="", blank=True, null=True)


class ElsevierModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=200, unique=True)
    sub_title = models.CharField(max_length=1000, default="", blank=True)
    url = models.URLField(blank=True, null=True)
    orcid_id = models.CharField(max_length=100, default="", blank=True)
    scopus_id = models.CharField(max_length=100, default="", blank=True)
    eid = models.CharField(max_length=1000, default="", blank=True)
    date_created = models.CharField(max_length=100, default="", blank=True)
    affiliation_current = models.CharField(max_length=1000, default="", blank=True)
    interests = models.CharField(max_length=1000, default="", blank=True)
    affiliation_count = models.CharField(max_length=100, default="", blank=True)
    coauthor_count = models.CharField(max_length=100, default="", blank=True)
    h_index = models.CharField(max_length=100, default="", blank=True)
    document_count = models.CharField(max_length=100, default="", blank=True)
    citation_count = models.CharField(max_length=100, default="", blank=True)
