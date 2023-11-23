import requests
from scholar.models import MyData
import json


def save_data_from_json(name):
    url = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={name}&api_key=bd3485996532e2797df4c04369f4d9719bf0b095b32af9f92ec39fd44172939e"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)["profiles"]

    list_of_interests = []

    for author in data:
        try:
            for interest in author.get("interests", []):
                list_of_interests.append(interest["title"])
        except Exception as e:
            print(f"Error processing interests: {e}")
            continue

        try:
            author_name = author["name"]
        except Exception as e:
            print(f"Error processing author name: {e}")
            continue

        my_data_object = MyData(
            full_name=author_name,
            google_scholar_id=author.get("author_id", ""),
            interest_list="\n".join(list_of_interests),
        )
        my_data_object.save()

    print(MyData.objects.all().values())


# input_name = input("Enter name: ")
# save_data_from_json(input_name)
