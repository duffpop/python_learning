import requests
import json
import os
from dotenv import load_dotenv

# get path to current directory
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# prepend the .env file with current directory
load_dotenv(os.path.join(BASEDIR, '.env'))
bob_token = os.environ.get('BOB_TOKEN')

people_url = "https://api.hibob.com/v1/people"

headers = {
    'accept': 'application/json',
    'authorization': bob_token
}

response = requests.request("GET", people_url, headers=headers)

full_employee_avatar_list = []
list_of_avatar_url = 'avatar_url_list.txt'

json_data = json.loads(response.text)

for employee in json_data['employees']:
    # print(employee['avatarUrl'])
    if employee['avatarUrl'] is None:
        continue
    else:
        full_employee_avatar_list.append(employee['avatarUrl'])

# print(full_employee_avatar_list)

with open(list_of_avatar_url, 'w') as file_object:
    for element in full_employee_avatar_list:
        file_object.write(element + '\n')
