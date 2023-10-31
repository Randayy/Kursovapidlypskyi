import requests



input_name = input("Enter name: ")



url = f"https://serpapi.com/search.json?engine=google_scholar_profiles&mauthors={input_name}&api_key=bd3485996532e2797df4c04369f4d9719bf0b095b32af9f92ec39fd44172939e"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

for author in response.json()["profiles"]:
    print(author["name"])
    name = author["name"]
    print('Дані про автора:')
    print(' - ' + author["name"])
    print(' - ' + author["author_id"])
    google_scholar_id = author["author_id"]
    list_of_interests = []
    print('Interests:')
    for interests in author["interests"]:
        print(' - ' + interests["title"])
        list_of_interests.append(interests["title"])
        
    print('\n')

