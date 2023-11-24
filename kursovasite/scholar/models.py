from django.db import models


class MyData(models.Model):
    full_name = models.CharField(max_length=100)
    google_scholar_id = models.CharField(max_length=100)
    interest_list = models.CharField(max_length=1000)
    sub_title = models.CharField(max_length=1000, default="")
    email = models.CharField(max_length=1000, default="")
    image = models.ImageField(upload_to='images/')
    
