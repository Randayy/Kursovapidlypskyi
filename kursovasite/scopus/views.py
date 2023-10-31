from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scopus import get_data


def scopus(request):
    name = get_data.name
    return HttpResponse(f"name : {name}")
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
