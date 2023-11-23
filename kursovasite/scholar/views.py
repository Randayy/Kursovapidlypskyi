from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scholar import get_data
from scholar.models import MyData
from .forms import SearchForm
from django.shortcuts import render, get_object_or_404

def scholar_detail(request, scholar_id):
    scholar = get_object_or_404(MyData, pk=scholar_id)
    return render(request, 'scholar_detail.html', {'scholar': scholar})


def search_scholar(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["full_name"]
            results = MyData.objects.filter(full_name__icontains=search_query)
            return render(
                request,
                "search_results.html",
                {"results": results, "form": form},
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
