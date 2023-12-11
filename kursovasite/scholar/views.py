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
        "cookie": 'scopus.machineID=D8A4EEDF1A39955DA4E1898C25BEDA11.i-0d1e8ac190485b248; Scopus-usage-key=enable-logging; AT_CONTENT_COOKIE="FEATURE_NEW_CTO_SOURCES:0,FEATURE_NEW_CTO_AUTHOR_SEARCH:0,"; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; SLG_G_WPT_TO=uk; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; SCSessionID=E843925E7532B9721E11BA4506972B9C.i-03360355e35b57722; scopusSessionUUID=4c9753a7-a167-430b-b; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1C338B9C081E1792D11733262768A63DA199899D6E1740BF9E29DCB6CA40B345C10BA32070D9964CEACBAE7C5777723B791094ABE2A1B0134753403F22A84CB2A; __cf_bm=hzgNIpxKHCf.OEUUWUZTPg3DaODsAqM7AgR6_eSEp6g-1702237600-0-AQfFtJsLVyzi2PthInZp/9yPhyo0fP9Xi1xGio7Mz3I/vVFeiUjdjRuGruI47w7MjwHCFXXR2FjPj809Gylth4U=; _cfuvid=7tfWUd4MyrAHLiRS7V3n1XI.X6fh8wBFlby_bI1CJmc-1702237600926-0-604800000; SCOPUS_JWT=eyJraWQiOiJjYTUwODRlNi03M2Y5LTQ0NTUtOWI3Zi1kMjk1M2VkMmRiYmMiLCJhbGciOiJSUzI1NiJ9.eyJhbmFseXRpY3NfaW5mbyI6eyJhY2NvdW50SWQiOiIyNzg2NDEiLCJ1c2VySWQiOiJhZToxMzM0MTI1MyIsImFjY2Vzc1R5cGUiOiJhZTpBTk9OOjpHVUVTVDoiLCJhY2NvdW50TmFtZSI6IlNjb3B1cyBQcmV2aWV3In0sImRlcGFydG1lbnROYW1lIjoiU2NvcHVzIFByZXZpZXciLCJzdWIiOiIxMzM0MTI1MyIsImluc3RfYWNjdF9uYW1lIjoiU2NvcHVzIFByZXZpZXciLCJzdWJzY3JpYmVyIjpmYWxzZSwid2ViVXNlcklkIjoiMTMzNDEyNTMiLCJkZXBhcnRtZW50SWQiOiIyODk4MzkiLCJpc3MiOiJTY29wdXMiLCJpbnN0X2FjY3RfaWQiOiIyNzg2NDEiLCJpbnN0X2Fzc29jX21ldGhvZCI6IiIsImFjY291bnROdW1iZXIiOiJDMDAwMjc4NjQxIiwicGF0aF9jaG9pY2UiOmZhbHNlLCJhdWQiOiJTY29wdXMiLCJuYmYiOjE3MDIyMzc2MDEsImZlbmNlcyI6WzJdLCJpbmR2X2lkZW50aXR5X21ldGhvZCI6IiIsImluc3RfYXNzb2MiOiJHVUVTVCIsImluZHZfaWRlbnRpdHkiOiJBTk9OIiwidXNhZ2VQYXRoSW5mbyI6IigxMzM0MTI1MyxVfDI4OTgzOSxEfDI3ODY0MSxBfDcyMjE4LFB8MSxQTCkoU0NPUFVTLENPTnwwZjRkMzQ1MTlhYzljMDQzN2YyYWY4MTI0YWZiZWVjNjNkNWVneHJxYSxTU098QU5PTl9HVUVTVCxBQ0NFU1NfVFlQRSkiLCJwcmltYXJ5QWRtaW5Sb2xlcyI6W10sImV4cCI6MTcwMjIzODUwMSwiYXV0aF90b2tlbiI6IjBmNGQzNDUxOWFjOWMwNDM3ZjJhZjgxMjRhZmJlZWM2M2Q1ZWd4cnFhIiwiaWF0IjoxNzAyMjM3NjAxfQ.rM8tBoghdRsJ3OJvAP535dtXfAMZPoCI_e3TNhToiemTVZn49NZXLBU_AwpLxUcpNvu3wpVtYOQXs2xEZExMYKm7TqnU-IAvse1CigDLoSmBJTnwITpwBN1BsxiSRG2pRlhXw6m8P52n-VlIjTlTbR9SSQfAvh-6lsmr4ORhd_cA905WVmes4GwLqy1IhW34SWAPDL6PMcwxkD7haZoOW7BXSSRWrMccR3mACW8A7o8kl2TWgdU-Wm0geAemOw6sUR_7ZUuFbFjuvfuPmXEI11mpNe23sRR1vCCE7S_0CqvycGPpgGNBKkmD6NZw6eUKCcMjFDsvlgcQc9j_reIB9A; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-2121179033%7CMCIDTS%7C19702%7CMCMID%7C45395599887568057390871668566450418887%7CMCAAMLH-1702842439%7C6%7CMCAAMB-1702842439%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1702244839s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-947642174%7CvVersion%7C5.3.0; __cfruid=a4bc7cb034156488bf49db22eb8852a785b31fb6-1702237646; s_sess=%20s_cpc%3D0%3B%20c21%3Dlastname%253Dkit%2526firstname%253Divan%3B%20e13%3Dlastname%253Dkit%2526firstname%253Divan%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20e41%3D1%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Arecord%25253Aauthor%252520details%252C100%252C100%252C875%252C1844%252C875%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25253Aauthor%252520details%252C100%252C100%252C875%252C825%252C875%252C1920%252C1080%252C1%252CL%3B; s_pers=%20c19%3Dsc%253Arecord%253Aauthor%2520details%7C1702239451230%3B%20v68%3D1702237650617%7C1702239451240%3B%20v8%3D1702237653084%7C1796845653084%3B%20v8_s%3DMore%2520than%25207%2520days%7C1702239453084%3B; mbox=session#90f4b8f8af9e4833b20b0287ca1da8e3#1702239520; scopus.machineID=D8A4EEDF1A39955DA4E1898C25BEDA11.i-0d1e8ac190485b248',
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEyODExNjEiLCJhcCI6IjMxNDU1OTQ0IiwiaWQiOiJiZDcxOTUyMmNkODIxZDY1IiwidHIiOiIzYjRlZmFjZThkMGZmZmMzYTI4Y2NlYjVjOTU0YTMwMCIsInRpIjoxNzAyMjM3NjU5ODYyLCJ0ayI6IjIwMzgxNzUifX0=",
        "referer": "https://www.scopus.com/authid/detail.uri?authorId=57208674228",
        "sec-ch-ua": '"Opera";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-3b4eface8d0fffc3a28cceb5c954a300-bd719522cd821d65-01",
        "tracestate": "2038175@nr=0-1-1281161-31455944-bd719522cd821d65----1702237659862",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
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
