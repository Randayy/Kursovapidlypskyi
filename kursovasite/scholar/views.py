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
from scholar.models import ElsevierModel
import re


def scholar_detail(request, scholar_id):
    scholar = get_object_or_404(MyData, pk=scholar_id)
    return render(request, "scholar_detail.html", {"scholar": scholar})


def elsevier_detail(request, scopus_id):
    scholar = get_object_or_404(ElsevierModel, pk=scopus_id)

    url = f"https://www.scopus.com/author/highchart.uri?authorId={str(scholar.scopus_id)}&apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b"
    headers = {
        "authority": "www.scopus.com",
        "accept": "*/*",
        "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": 'scopus.machineID=98E5C8631A11AE4970CEF278EF483E41.i-0ffe1b23ac93c68ce; _ga=GA1.2.641984540.1698782243; _ga_L74H3WXMBD=GS1.1.1698798295.2.0.1698798295.0.0.0; SCSessionID=9EA74F3A47A5E851AE3BB0CAD039149F.i-03f93d63633b9ec7e; scopusSessionUUID=2d2f9197-8a72-4150-9; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1C68CD6F33C3C1E11F9CED89E404CF80D0541BF47B2121E5E00FB4F7032C4D32610BA32070D9964CEACBAE7C5777723B7FE4E08D6D68E5AAF44618065BF94F058; __cf_bm=roViu8_TSxCURRZ2XBWGBowolJX2aB0GEuLYBhd.5NQ-1702278518-0-Aer1VqIE2YsfrScTCmeEPx7/NKTmaUzE8LEC9t2nbcpjr4vezwlZF66Ho84JKz0oxTpGGCm1v+6Q+ITZY4R29fU=; _cfuvid=yKGUSYMYuxJgZvGkipPg26qqxrVdj.TViM3dPmRBQMY-1702278518483-0-604800000; SCOPUS_JWT=eyJraWQiOiJjYTUwODRlNi03M2Y5LTQ0NTUtOWI3Zi1kMjk1M2VkMmRiYmMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNDM1NTY0ODgiLCJkZXBhcnRtZW50SWQiOiIyODk4MzkiLCJpc3MiOiJTY29wdXMiLCJpbnN0X2FjY3RfaWQiOiIyNzg2NDEiLCJwYXRoX2Nob2ljZSI6ZmFsc2UsImluZHZfaWRlbnRpdHkiOiJSRUciLCJleHAiOjE3MDIyNzk0MjAsImlhdCI6MTcwMjI3ODUyMCwiZW1haWwiOiJyb21hcG9saWNlcnJAZ21haWwuY29tIiwiYW5hbHl0aWNzX2luZm8iOnsiYWNjb3VudE5hbWUiOiJTY29wdXMgUHJldmlldyIsImFjY291bnRJZCI6IjI3ODY0MSIsInVzZXJJZCI6ImFlOjI0MzU1NjQ4OCIsImFjY2Vzc1R5cGUiOiJhZTpSRUc6VV9QOkdVRVNUOiJ9LCJkZXBhcnRtZW50TmFtZSI6IlNjb3B1cyBQcmV2aWV3IiwiaW5zdF9hY2N0X25hbWUiOiJTY29wdXMgUHJldmlldyIsInN1YnNjcmliZXIiOmZhbHNlLCJ3ZWJVc2VySWQiOiIyNDM1NTY0ODgiLCJpbnN0X2Fzc29jX21ldGhvZCI6IiIsImdpdmVuX25hbWUiOiJyb21hbiIsImFjY291bnROdW1iZXIiOiJDMDAwMjc4NjQxIiwiYXVkIjoiU2NvcHVzIiwibmJmIjoxNzAyMjc4NTIwLCJmZW5jZXMiOlsyXSwiaW5kdl9pZGVudGl0eV9tZXRob2QiOiJVX1AiLCJpbnN0X2Fzc29jIjoiR1VFU1QiLCJuYW1lIjoicm9tYW4gcm9tYSIsInVzYWdlUGF0aEluZm8iOiIoMjQzNTU2NDg4LFV8Mjg5ODM5LER8Mjc4NjQxLEF8NzIyMTgsUHwxLFBMKShTQ09QVVMsQ09OfGFlODkyM2Y5MjJkYzIxNDE4NDg5OTAxMmRiNWVmYzIzNzQ2ZGd4cnFhLFNTT3xSRUdfR1VFU1QsQUNDRVNTX1RZUEUpIiwicHJpbWFyeUFkbWluUm9sZXMiOltdLCJhdXRoX3Rva2VuIjoiYWU4OTIzZjkyMmRjMjE0MTg0ODk5MDEyZGI1ZWZjMjM3NDZkZ3hycWEiLCJmYW1pbHlfbmFtZSI6InJvbWEifQ.gUJ75XMLW0EyQz3q317zV8lx-owf3yVtIba4nttoPfgce1qmVJTwlzAS0EgtaYVEDF6tTI2LdzLChNuibT4XkBsykpGiel3uJe-7C5oXtDr8POOL481KwUFp7YBtTYfB-RtwmeVduKnNVhrSF1l0NNvZ2DM9OhsJzyA_crkDQPAuNxyjWbRSAoAkD0zjP4gPJQFapM6N2SxHi7Z5EbNn53qbVTdRSAXV_fd6H0lomIyrwG0-9B4HWNP8sWsvt9UcORw4QRWy-KWEu-iim0KJLi8C2ua4xoQIWGuwWzukqeEMezgXEC4_akpuuOxyk3hTgKpBVQq9TGANFSa1eOHhig; Scopus-usage-key=enable-logging; AT_CONTENT_COOKIE="FEATURE_NEW_CTO_SOURCES:0,FEATURE_NEW_CTO_AUTHOR_SEARCH:0,"; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-2121179033%7CMCIDTS%7C19703%7CMCMID%7C56342726374883315700699718973689906655%7CMCAAMLH-1702883321%7C6%7CMCAAMB-1702883321%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1702285721s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1149339262%7CvVersion%7C5.3.0; __cfruid=783771db48c1daa3108077f0141dc80fe053fb85-1702278523; s_sess=%20e41%3D1%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B%20s_sq%3D%3B; s_pers=%20c19%3Dsc%253Arecord%253Aauthor%2520details%7C1702280322623%3B%20v68%3D1702278521515%7C1702280322627%3B%20v8%3D1702278527788%7C1796886527788%3B%20v8_s%3DLess%2520than%25207%2520days%7C1702280327788%3B; mbox=PC#84cecc337ab9400da3fe4214ce23506d.37_0#1765523338|session#c483e82e06b0401aa600865fd0c8f4f2#1702280399; scopus.machineID=98E5C8631A11AE4970CEF278EF483E41.i-0ffe1b23ac93c68ce',
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEyODExNjEiLCJhcCI6IjMxNDU1OTQ0IiwiaWQiOiIwY2M1Y2I4Y2M4ODg0MzU5IiwidHIiOiI0ZjQ4ZjNmMTlmMWM2NGRjY2M2NTY2MDlmZDBjZDMwMCIsInRpIjoxNzAyMjc4NTM4MTI2LCJ0ayI6IjIwMzgxNzUifX0=",
        "referer": "https://www.scopus.com/authid/detail.uri?authorId=57208674228",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-4f48f3f19f1c64dccc656609fd0cd300-0cc5cb8cc8884359-01",
        "tracestate": "2038175@nr=0-1-1281161-31455944-0cc5cb8cc8884359----1702278538126",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Перевірка наявності помилок у відповіді
        data = response.json()

        # Ваші дані для графіків - приклад
        try:
            docobj = data["docObj"]
            citeobj = data["citeObj"]
            chart_data = {
                "docObj": [x for x in docobj],
                "citeObj": [y for y in citeobj],
            }
            context = {
                "scholar": scholar,
                "chart_data": json.dumps(chart_data),
            }
            return render(request, "result_els.html", context)
        except:
            context = {
                "scholar": scholar,
            }
            return render(request, "result_els.html", context)

    except requests.exceptions.RequestException as err:
        # Обробка помилок у випадку проблеми з запитом
        context = {
            "scholar": scholar,
        }
        return render(request, "result_els.html", context)


class PersonListView(ListView):
    model = MyData
    template_name = "list_authors.html"
    context_object_name = "persons"
    paginate_by = 12


def indexx(request):
    page = request.GET.get("page", 1)
    per_page = 12

    data_list = MyData.objects.order_by("full_name")
    paginator = Paginator(data_list, per_page)

    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, "list_authors.html", {"data": data})


def search_elsevier(request):
    if request.method == "POST":
        form = SearchForm_Elsevier(request.POST)
        if form.is_valid():
            try:
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                search_query = first_name + " " + last_name

                url_scopus_name = f"https://api.elsevier.com/content/search/author?query=authlast({last_name})+AND+authfirst({first_name})&apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b"
                response_scopus_profiles = requests.get(url_scopus_name)
                data_scopus_profiles = json.loads(response_scopus_profiles.text)[
                    "search-results"
                ]["entry"]
                with transaction.atomic():
                    for author in data_scopus_profiles:
                        id_scopus = author.get("dc:identifier", "")
                        clear_id_scopus = re.findall(r"\d+", id_scopus)[0]
                        url_all_info = f"https://api.elsevier.com/content/author/author_id/{clear_id_scopus}?apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b&view=ENHANCED"
                        headers = {
                            "Accept": "application/json",
                        }
                        response_all_info = requests.get(url_all_info, headers=headers)
                        print(response_all_info.text)
                        data_all_info = json.loads(response_all_info.text)

                        try:
                            author_name = (
                                data_all_info["author-retrieval-response"][0][
                                    "author-profile"
                                ]["preferred-name"]["given-name"]
                                + " "
                                + data_all_info["author-retrieval-response"][0][
                                    "author-profile"
                                ]["preferred-name"]["surname"]
                            )
                            print(author_name)
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            sub_title = data_all_info["author-retrieval-response"][0][
                                "subject-areas"
                            ]["subject-area"][0]["$"]
                            print(sub_title)
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            url = data_all_info["author-retrieval-response"][0][
                                "coredata"
                            ]["link"][0]["@href"]
                            print(url)
                        except Exception as e:
                            print(f"Error processing author name or image: {e}")
                            continue
                        try:
                            orcid_id = data_all_info["author-retrieval-response"][0][
                                "coredata"
                            ]["orcid"]
                            print(orcid_id)
                        except Exception as e:
                            orcid_id = ""
                            print(f"No orcid_id")
                        try:
                            orcid_id = data_all_info["author-retrieval-response"][0][
                                "coredata"
                            ]["orcid"]
                            print(orcid_id)
                        except Exception as e:
                            orcid_id = ""
                            print(f"No orcid_id")
                        try:
                            eid = data_all_info["author-retrieval-response"][0][
                                "coredata"
                            ]["eid"]
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
                            document_count = data_all_info["author-retrieval-response"][
                                0
                            ]["coredata"]["document-count"]
                            print(document_count)
                        except Exception as e:
                            document_count = ""
                            print(f"No document_count")
                        try:
                            citation_count = data_all_info["author-retrieval-response"][
                                0
                            ]["coredata"]["citation-count"]
                            print(citation_count)

                        except Exception as e:
                            citation_count = ""
                            print(f"No citation_count")

                        try:
                            h_index = data_all_info["author-retrieval-response"][0][
                                "h-index"
                            ]
                            print(h_index)
                        except Exception as e:
                            h_index = ""
                            print(f"No h_index")
                        try:
                            coauthor_count = data_all_info["author-retrieval-response"][
                                0
                            ]["coauthor-count"]
                            print(coauthor_count)

                        except Exception as e:
                            coauthor_count = ""
                            print(f"No coauthor_count")
                        try:
                            affiliation_count = data_all_info[
                                "author-retrieval-response"
                            ][0]["affiliation-history"]["affiliation"].__len__()
                            print(affiliation_count)
                        except Exception as e:
                            affiliation_count = ""
                            print(f"No affiliation_count")

                        try:
                            list_of_interests = []
                            for interest in data_all_info["author-retrieval-response"][
                                0
                            ]["subject-areas"]["subject-area"]:
                                interess = f'{interest["$"]}, '
                                list_of_interests.append(interess)
                            interests = "".join(list_of_interests)
                            print(interests)
                        except Exception as e:
                            print(f"Error processing interests or author name: {e}")
                            continue

                        try:
                            affiliation_current = data_all_info[
                                "author-retrieval-response"
                            ][0]["author-profile"]["affiliation-current"][
                                "affiliation"
                            ][
                                "ip-doc"
                            ][
                                "afdispname"
                            ]
                            print(affiliation_current)
                        except Exception as e:
                            affiliation_current = ""
                            print(f"No affiliation_current")

                        try:
                            date_created = (
                                data_all_info["author-retrieval-response"][0][
                                    "author-profile"
                                ]["date-created"]["@day"]
                                + "."
                                + data_all_info["author-retrieval-response"][0][
                                    "author-profile"
                                ]["date-created"]["@month"]
                                + "."
                                + data_all_info["author-retrieval-response"][0][
                                    "author-profile"
                                ]["date-created"]["@year"]
                            )
                            print(date_created)
                        except Exception as e:
                            date_created = ""
                            print(f"No date_created")

                        elsevier_model = ElsevierModel(
                            first_name=first_name,
                            last_name=last_name,
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
                            date_created=date_created,
                        )
                        elsevier_model.save()
                    results = ElsevierModel.objects.filter(
                        author_name__icontains=search_query
                    )
                    # results+=ElsevierModel.objects.filter(first_name__icontains=search_query)
                    # results+=ElsevierModel.objects.filter(last_name__icontains=search_query)
                    return render(
                        request,
                        "search_results_els.html",
                        {"results": results, "form": form},
                    )
            except:
                results = ElsevierModel.objects.filter(
                    author_name__icontains=search_query
                )
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
            try:
                url_profiles = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={search_query}&api_key=a6fe3b9302932eb9b97260c0f4b6e9a025183b1345d8a853a5918f774678f00b"
                response_profiles = requests.get(url_profiles)
                data_profiles = json.loads(response_profiles.text)["profiles"]

                with transaction.atomic():
                    for author in data_profiles:
                        try:
                            author_id = author.get("author_id", "")
                            url_author = f"https://serpapi.com/search.json?author_id={author_id}&engine=google_scholar_author&hl=en&api_key=a6fe3b9302932eb9b97260c0f4b6e9a025183b1345d8a853a5918f774678f00b"
                            response_author = requests.get(url_author)
                            data_author = json.loads(response_author.text)

                            list_of_interests = []

                            for interest in data_author["author"]["interests"]:
                                list_of_interests.append(interest["title"])

                        except Exception as e:
                            print(f"Error processing interests or author name: {e}")
                            continue

                        list_of_articles = []
                        list_of_articles_url = []
                        try:
                            for article in data_author["articles"]:
                                list_of_articles.append(article["title"])
                                list_of_articles_url.append(article["link"])
                        except:
                            print("No articles")
                            articles = ""

                        try:
                            h_index = data_author["cited_by"]["table"][1]["h_index"][
                                "all"
                            ]

                        except Exception as e:
                            print(f"Error processing h-index: {e}")

                        try:
                            print(
                                data_author["cited_by"]["table"][2]["i10_index"]["all"]
                            )
                            i10_index = data_author["cited_by"]["table"][2][
                                "i10_index"
                            ]["all"]
                        except Exception as e:
                            print(f"Error processing i10: {e}")

                        try:
                            citations = data_author["cited_by"]["table"][0][
                                "citations"
                            ]["all"]

                        except Exception as e:
                            print(f"Error processing citation: {e}")

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
                            article_list=",".join(list_of_articles),
                            article_url_list=",".join(list_of_articles_url),
                            h_index=h_index,
                            i10_index=i10_index,
                            citations=citations,
                        )
                        my_data_object.save()

                        print(MyData.objects.all().values())

                    results = MyData.objects.filter(full_name__icontains=search_query)
                    zipped_data = zip(list_of_articles, list_of_articles_url)
                    return render(
                        request,
                        "search_results.html",
                        {
                            "results": results,
                            "form": form,
                            "zipped_data": zipped_data,
                        },
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
