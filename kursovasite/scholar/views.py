from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scholar import get_data


def scholar(request):
    name = get_data.name
    return HttpResponse(f"name : {name}")
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
