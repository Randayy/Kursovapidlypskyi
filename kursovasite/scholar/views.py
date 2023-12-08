from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scholar import get_data
from scholar.models import MyData
from scholar.models import ElsevierModel
from .forms import SearchForm
from .forms import SearchForm_Elsevier
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator
import requests
import json
from django.db import transaction
from scholar.models import MyData
import re





def scholar_detail(request, scholar_id):
    scholar = get_object_or_404(MyData, pk=scholar_id)
    return render(request, "scholar_detail.html", {"scholar": scholar})

class PersonListView(ListView):
    model = MyData
    template_name = 'list_authors.html'
    context_object_name = 'persons'
    paginate_by = 12

def indexx(request):
    page = request.GET.get('page', 1)
    per_page = 12

    data_list = MyData.objects.order_by('full_name')
    paginator = Paginator(data_list, per_page)

    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'list_authors.html', {'data': data})

def search_elsevier(request):
    if request.method == 'POST':
        form = SearchForm_Elsevier(request.POST)
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                search_query = first_name + " " + last_name
                url_scopus_name = f"https://api.elsevier.com/content/search/author?query=authlast({last_name})+AND+authfirst({first_name})&apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b"
                response_scopus_profiles = requests.get(url_scopus_name)
                data_scopus_profiles = json.loads(response_scopus_profiles.text)["search-results"]["entry"]
                with transaction.atomic():
                    for author in data_scopus_profiles:
                        id_scopus = author.get("dc:identifier", "")
                        clear_id_scopus = re.findall(r'\d+', id_scopus)[0]
                        url_all_info = f"https://api.elsevier.com/content/author/author_id/{clear_id_scopus}?apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b&view=ENHANCED"
                        headers = {
                        'Accept': 'application/json',
                        }
                        response_all_info = requests.get(url_all_info, headers=headers)
                        print(response_all_info.text)
                        data_all_info = json.loads(response_all_info.text)

                        try:
                            author_name = data_all_info["author-retrieval-response"][0]["author-profile"]["preferred-name"]["given-name"] + " " + data_all_info["author-retrieval-response"][0]["author-profile"]["preferred-name"]["surname"]
                            print(author_name)
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            sub_title = data_all_info["author-retrieval-response"][0]["subject-areas"]["subject-area"][0]["$"]
                            print(sub_title)
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            url = data_all_info["author-retrieval-response"][0]["coredata"]["link"][0]["@href"]
                            print(url)
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            orcid_id = data_all_info["author-retrieval-response"][0]["coredata"]["orcid"]
                            print(orcid_id)
                        except Exception as e:
                            orcid_id = ""
                            print(f"No orcid_id")
                        try:
                            orcid_id = data_all_info["author-retrieval-response"][0]["coredata"]["orcid"]
                            print(orcid_id)
                        except Exception as e:
                            orcid_id = ""
                            print(f"No orcid_id")
                        try:
                            eid = data_all_info["author-retrieval-response"][0]["coredata"]["eid"]
                            print(eid)
                        except Exception as e:
                            eid = ""
                            print(f"No eid")
                        try:
                            scopus_id = clear_id_scopus
                            print(scopus_id)
                        except Exception as e:
                            scopus_id = ""
                            print(f"No scopus_id")
                        try:
                            document_count = data_all_info["author-retrieval-response"][0]["coredata"]["document-count"]
                            print(document_count)
                        except Exception as e:
                            document_count = ""
                            print(f"No document_count")
                        try:
                            citation_count = data_all_info["author-retrieval-response"][0]["coredata"]["citation-count"]
                            print(citation_count)

                        except Exception as e:
                            citation_count = ""
                            print(f"No citation_count")

                        try:
                            h_index = data_all_info["author-retrieval-response"][0]["h-index"]
                            print(h_index)
                        except Exception as e:
                            h_index = ""
                            print(f"No h_index")
                        try:
                            coauthor_count = data_all_info["author-retrieval-response"][0]["coauthor-count"]
                            print(coauthor_count)

                        except Exception as e:
                            coauthor_count = ""
                            print(f"No coauthor_count")
                        try:
                            affiliation_count = data_all_info["author-retrieval-response"][0]["affiliation-history"]["affiliation"].__len__()
                            print(affiliation_count)
                        except Exception as e:
                            affiliation_count = ""
                            print(f"No affiliation_count")


                        try:
                            list_of_interests = []
                            for interest in data_all_info["author-retrieval-response"][0]["subject-areas"]["subject-area"]:
                                interess = f'{interest["$"]}, '
                                list_of_interests.append(interess)
                            interests = "".join(list_of_interests)
                            print(interests)
                        except Exception as e:
                            print(f"Error processing interests or author name: {e}")
                            continue

                        try:
                            affiliation_current = data_all_info["author-retrieval-response"][0]["author-profile"]["affiliation-current"]["affiliation"]["ip-doc"]["afdispname"]
                            print(affiliation_current)
                        except Exception as e:
                            affiliation_current = ""
                            print(f"No affiliation_current")

                        try:
                            date_created = data_all_info["author-retrieval-response"][0]["author-profile"]["date-created"]["@day"]+"."+data_all_info["author-retrieval-response"][0]["author-profile"]["date-created"]["@month"]+"."+data_all_info["author-retrieval-response"][0]["author-profile"]["date-created"]["@year"]
                            print(date_created)
                        except Exception as e:
                            date_created = ""
                            print(f"No date_created")

                        

                        elsevier_model = ElsevierModel(
                            author_name=author_name,
                            sub_title=sub_title,
                            url=url,
                            orcid_id=orcid_id,
                            eid=eid,
                            scopus_id=scopus_id,
                            document_count=document_count,
                            citation_count=citation_count,
                            h_index=h_index,
                            coauthor_count=coauthor_count,
                            affiliation_count=affiliation_count,
                            interests=interests,
                            affiliation_current=affiliation_current,
                            date_created=date_created
                        )
                        elsevier_model.save()
                    results = ElsevierModel.objects.filter(author_name__icontains=search_query)
                    return render(
                        request,
                        "search_results_els.html",
                        {"results": results, "form": form},
                    )
            except:
                results = ElsevierModel.objects.filter(author_name__icontains=search_query)
                return render(
                    request,
                    "search_results_els.html",
                    {"results": results, "form": form},
                )
    else:
        form = SearchForm_Elsevier()

    return render(request, "search_template_els.html", {"form": form})


def search_scholar(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["full_name"]
            search_query = 'Ivan'
            try:
                url_profiles = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={search_query}&api_key=8c1b6999bc3cd362c9c702cd8898f500a889416112c3f501223246127c046166"
                response_profiles = requests.get(url_profiles)
                data_profiles = json.loads(response_profiles.text)["profiles"]



                with transaction.atomic():
                    for author in data_profiles:
                        try:
                            author_id = author.get("author_id", "")
                            url_author = f"https://serpapi.com/search.json?author_id={author_id}&engine=google_scholar_author&hl=en&api_key=8c1b6999bc3cd362c9c702cd8898f500a889416112c3f501223246127c046166"
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
