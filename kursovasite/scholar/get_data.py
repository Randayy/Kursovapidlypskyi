import requests
from scholar.models import MyData
import json


def save_data_from_json(name):
    url_profiles = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={name}&api_key=bd3485996532e2797df4c04369f4d9719bf0b095b32af9f92ec39fd44172939e"
    response_profiles = requests.get(url_profiles)
    data_profiles = json.loads(response_profiles.text)["profiles"]

    for author in data_profiles:
        try:
            author_id = author.get("author_id", "")
            url_author = f"https://serpapi.com/search.json?author_id={author_id}&engine=google_scholar_author&hl=en&api_key=bd3485996532e2797df4c04369f4d9719bf0b095b32af9f92ec39fd44172939e"
            response_author = requests.get(url_author)
            data_author = json.loads(response_author.text)

            list_of_interests = []
            for interest in data_author.get("interests", [])[:5]:
                list_of_interests.append(interest.get("title", ""))
        except Exception as e:
            print(f"Error processing interests or author name: {e}")
            continue

        try:
            author_name = author["name"]

        except Exception as e:
            print(f"Error processing author name: {e}")
            continue

        my_data_object = MyData(
            full_name=author_name,
            google_scholar_id=author_id,
            interest_list="\n".join(list_of_interests),
        )
        my_data_object.save()

    print(MyData.objects.all().values())


# Запит користувача

# Запиту не буде я в блоці

# input_name = input("Enter name: ")
# save_data_from_json(input_name)
