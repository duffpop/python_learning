import requests
from requests.auth import HTTPBasicAuth
import json
import os


get_members_url_page_one = 'https://api.github.com/orgs/depop/members?page=1&per_page=100'
get_members_url_page_two = 'https://api.github.com/orgs/depop/members?page=2&per_page=100'

r_one = requests.get(get_members_url_page_one, auth=HTTPBasicAuth('duffpop', 'a3d38dbbeefdd0725dc507c8b396dbd83ba5f446'))
r_two = requests.get(get_members_url_page_two, auth=HTTPBasicAuth('duffpop', 'a3d38dbbeefdd0725dc507c8b396dbd83ba5f446'))
# print(r.json())

# request_test = r.text
# print(request_test)

# parsed_json = json.loads(r.text)
# print(json.dumps(parsed_json, indent=4, sort_keys=True))

response_json_one = r_one.json()
response_json_two = r_two.json()

count = 0
count_one = 0
count_two = 0

user_list = []

def get_members(url):


for item in response_json_one:
    # print(item['login'])
    # count_one += 1
    # count += 1
    user_list.append(item)

# print(count)

for item in response_json_two:
    # print(item['login'])
    # count_two += 1
    # count += 1
    user_list.append(item)

print(count)
# for key, value in parsed_json.items():
#     print(value)


# for username in response_json.keys():
#     print(username)