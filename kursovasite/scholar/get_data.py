# import requests
# import json
# from django.db import transaction
# # from scholar.models import MyData
# import re


# def save_data_from_json(name,surname):
#     # try:
#     url_scopus_name = f"https://api.elsevier.com/content/search/author?query=authlast({surname})+AND+authfirst({name})&apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b"
#     response_scopus_profiles = requests.get(url_scopus_name)
#     data_scopus_profiles = json.loads(response_scopus_profiles.text)["search-results"]["entry"]
#     # with transaction.atomic():
#     for author in data_scopus_profiles:
#         id_scopus = author.get("dc:identifier", "")
#         clear_id_scopus = re.findall(r'\d+', id_scopus)[0]
#         url_all_info = f"https://api.elsevier.com/content/author/author_id/{clear_id_scopus}?apiKey=7b03208d6f2a586392c25c8d59933d43&insttoken=ace1a9b7e5d8b0336204845e7e6c393b&view=ENHANCED"
#         headers = {
#         'Accept': 'application/json',
#         }
#         response_all_info = requests.get(url_all_info, headers=headers)
#         print(response_all_info.text)
#         data_all_info = json.loads(response_all_info.text)

#         try:
#             author_name = data_all_info["author-retrieval-response"][0]["author-profile"]["preferred-name"]["given-name"] + " " + data_all_info["author-retrieval-response"][0]["author-profile"]["preferred-name"]["surname"]
#             print(author_name)
#         except Exception as e:
#             print(f"Error processing author name or image: {e}")
#             continue
#         try:
#             sub_title = data_all_info["author-retrieval-response"][0]["subject-areas"]["subject-area"][0]["$"]
#             print(sub_title)
#         except Exception as e:
#             print(f"Error processing author name or image: {e}")
#             continue
#         try:
#             url = data_all_info["author-retrieval-response"][0]["coredata"]["link"][0]["@href"]
#             print(url)
#         except Exception as e:
#             print(f"Error processing author name or image: {e}")
#             continue
#         try:
#             orcid_id = data_all_info["author-retrieval-response"][0]["coredata"]["orcid"]
#             print(orcid_id)
#         except Exception as e:
#             orcid_id = ""
#             print(f"No orcid_id")
#         try:
#             orcid_id = data_all_info["author-retrieval-response"][0]["coredata"]["orcid"]
#             print(orcid_id)
#         except Exception as e:
#             orcid_id = ""
#             print(f"No orcid_id")
#         try:
#             eid = data_all_info["author-retrieval-response"][0]["coredata"]["eid"]
#             print(eid)
#         except Exception as e:
#             eid = ""
#             print(f"No eid")
#         try:
#             scopus_id = clear_id_scopus
#             print(scopus_id)
#         except Exception as e:
#             scopus_id = ""
#             print(f"No scopus_id")
#         try:
#             document_count = data_all_info["author-retrieval-response"][0]["coredata"]["document-count"]
#             print(document_count)
#         except Exception as e:
#             document_count = ""
#             print(f"No document_count")
#         try:
#             citation_count = data_all_info["author-retrieval-response"][0]["coredata"]["citation-count"]
#             print(citation_count)

#         except Exception as e:
#             citation_count = ""
#             print(f"No citation_count")

#         try:
#             h_index = data_all_info["author-retrieval-response"][0]["h-index"]
#             print(h_index)
#         except Exception as e:
#             h_index = ""
#             print(f"No h_index")
#         try:
#             coauthor_count = data_all_info["author-retrieval-response"][0]["coauthor-count"]
#             print(coauthor_count)

#         except Exception as e:
#             coauthor_count = ""
#             print(f"No coauthor_count")
#         try:
#             affiliation_count = data_all_info["author-retrieval-response"][0]["affiliation-history"]["affiliation"].__len__()
#             print(affiliation_count)
#         except Exception as e:
#             affiliation_count = ""
#             print(f"No affiliation_count")


#         try:
#             list_of_interests = []
#             for interest in data_all_info["author-retrieval-response"][0]["subject-areas"]["subject-area"]:
#                 interess = f'{interest["$"]}, '
#                 list_of_interests.append(interess)
#             interests = "".join(list_of_interests)
#             print(interests)
#         except Exception as e:
#             print(f"Error processing interests or author name: {e}")
#             continue

#         try:
#             affiliation_current = data_all_info["author-retrieval-response"][0]["author-profile"]["affiliation-current"]["affiliation"]["ip-doc"]["afdispname"]
#             print(affiliation_current)
#         except Exception as e:
#             affiliation_current = ""
#             print(f"No affiliation_current")

#         try:
#             date_created = data_all_info["author-retrieval-response"][0]["author-profile"]["date-created"]["@day"]+"."+data_all_info["author-retrieval-response"][0]["author-profile"]["date-created"]["@month"]+"."+data_all_info["author-retrieval-response"][0]["author-profile"]["date-created"]["@year"]
#             print(date_created)
#         except Exception as e:
#             date_created = ""
#             print(f"No date_created")

        

#     # except:
#     #     print("Error")


            

# input_name = input("Enter name: ")
# input_surname = input("Enter surname: ")
# save_data_from_json(input_name,input_surname)
