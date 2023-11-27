from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scholar import get_data
from scholar.models import MyData
from .forms import SearchForm
from django.shortcuts import render, get_object_or_404

import requests
import json
from django.db import transaction
from scholar.models import MyData


def scholar_detail(request, scholar_id):
    scholar = get_object_or_404(MyData, pk=scholar_id)
    return render(request, "scholar_detail.html", {"scholar": scholar})


def search_scholar(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["full_name"]
            try:
                url_profiles = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={search_query}&api_key=02d4ff946a4f8aa3550e3ba77eef2cc9138b31f78e735c25a1124cb81772a0e6"
                response_profiles = requests.get(url_profiles)
                data_profiles = json.loads(response_profiles.text)["profiles"]
                with transaction.atomic():
                    for author in data_profiles:
                        try:
                            author_id = author.get("author_id", "")
                            url_author = f"https://serpapi.com/search.json?author_id={author_id}&engine=google_scholar_author&hl=en&api_key=02d4ff946a4f8aa3550e3ba77eef2cc9138b31f78e735c25a1124cb81772a0e6"
                            response_author = requests.get(url_author)
                            data_author = json.loads(response_author.text)

                            list_of_interests = []
                            for interest in data_author["author"]["interests"]:
                                list_of_interests.append(interest["title"])
                        except Exception as e:
                            print(f"Error processing interests or author name: {e}")
                            continue
                        try:
                            image = data_author["author"]["thumbnail"]
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            author_name = data_author["author"]["name"]
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            sub_title = data_author["author"]["affiliations"]
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            email = data_author["author"]["email"]
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue

                        my_data_object = MyData(
                            full_name=author_name,
                            google_scholar_id=author_id,
                            interest_list="\n".join(list_of_interests),
                            sub_title=sub_title,
                            email=email,
                            image=image,
                        )
                        my_data_object.save()

                        print(MyData.objects.all().values())

                    results = MyData.objects.filter(full_name__icontains=search_query)
                    return render(
                        request,
                        "search_results.html",
                        {"results": results, "form": form},
                    )
            except:
                results = MyData.objects.filter(full_name__icontains=search_query)
                return render(
                    request, "search_results.html", {"results": results, "form": form}
                )
    else:
        form = SearchForm()

    return render(request, "search_template.html", {"form": form})


def scholar(request):
    name = MyData.objects.all().values()[2]["full_name"]
    id_ = MyData.objects.all().values()[2]["google_scholar_id"]
    interests = MyData.objects.all().values()[2]["interest_list"]
    response = ""
    for x in range(1, 10):
        response += (
            f'name : {MyData.objects.all().values()[x]["full_name"]}, scholar_id : {MyData.objects.all().values()[x]["google_scholar_id"]}, interests : {MyData.objects.all().values()[x]["interest_list"]}'
            + "\n"
        )

    return HttpResponse(response)
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
