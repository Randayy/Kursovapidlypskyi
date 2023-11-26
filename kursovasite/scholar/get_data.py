# import requests
# import json
# from django.db import transaction
# from scholar.models import MyData


# def save_data_from_json(name):
#     url_profiles = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={name}&api_key=1b4ec107a259ec05310f5913f71cfddd39e4d6d0e415936c4b230fa31ccfa0d5"
#     response_profiles = requests.get(url_profiles)
#     data_profiles = json.loads(response_profiles.text)["profiles"]

#     with transaction.atomic():
#         for author in data_profiles:
#             try:
#                 author_id = author.get("author_id", "")
#                 url_author = f"https://serpapi.com/search.json?author_id={author_id}&engine=google_scholar_author&hl=en&api_key=1b4ec107a259ec05310f5913f71cfddd39e4d6d0e415936c4b230fa31ccfa0d5"
#                 response_author = requests.get(url_author)
#                 data_author = json.loads(response_author.text)

#                 list_of_interests = []
#                 for interest in data_author["author"]["interests"]:
#                     list_of_interests.append(interest["title"])
#             except Exception as e:
#                 print(f"Error processing interests or author name: {e}")
#                 continue
#             try:
#                 image = data_author["author"]["thumbnail"]
#             except Exception as e:
#                 print(f"Error processing author name or image: {e}")
#                 continue
#             try:
#                 author_name = data_author["author"]["name"]
#             except Exception as e:
#                 print(f"Error processing author name or image: {e}")
#                 continue
#             try:
#                 sub_title = data_author["author"]["affiliations"]
#             except Exception as e:
#                 print(f"Error processing author name or image: {e}")
#                 continue
#             try:
#                 email = data_author["author"]["email"]
#             except Exception as e:
#                 print(f"Error processing author name or image: {e}")
#                 continue

#             my_data_object = MyData(
#                 full_name=author_name,
#                 google_scholar_id=author_id,
#                 interest_list="\n".join(list_of_interests),
#                 sub_title=sub_title,
#                 email=email,
#                 image=image,
#             )
#             my_data_object.save()

#     print(MyData.objects.all().values())


# Запит користувача
# MyData.objects.all().delete()

# input_name = input("Enter name: ")
# save_data_from_json(input_name)
