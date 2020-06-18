import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

# get path to current directory
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# prepend the .env file with current directory
load_dotenv(os.path.join(BASEDIR, '.env'))

# github only pulls 100 members at a maximum, so have to list a second page to get all members
get_members_url_page_one = 'https://api.github.com/orgs/depop/members?page=1&per_page=100'
get_members_url_page_two = 'https://api.github.com/orgs/depop/members?page=2&per_page=100'

# set github api token from .env file
github_api_token = os.environ.get('GITHUB_TEAMS_API_TOKEN')
# set team id from .env file
team_id = os.environ.get('TEAM_ID')
# set username from .env file
it_github_username = os.environ.get('USERNAME')
# set username from .env file
org = os.environ.get('ORG')

# GET request
r_one = requests.get(get_members_url_page_one, auth=HTTPBasicAuth(it_github_username, github_api_token))
r_two = requests.get(get_members_url_page_two, auth=HTTPBasicAuth(it_github_username, github_api_token))

# PUT request endpoint - NOTE NEEDS MEMBER USERNAME AT THE END
github_team = (f'https://api.github.com/orgs/{org}/team/{team_id}/memberships/')

user_list = []
test_user_list = ['duffpop']

params = {'role': 'member'}

def get_members(url):
    """
    Get list of all members in the org and append to a list
    Usage: get_members(r_one)
    """
    github_url = url.json()
    for item in github_url:
        user_list.append(item['login'])
    # print(user_list)
    # return user_list


def put_request():
    for user in test_user_list:
        update_team_put_request = requests.put(f'https://api.github.com/orgs/{org}/team/{team_id}/memberships/{user}', auth=HTTPBasicAuth(it_github_username, github_api_token))
        print(update_team_put_request.content)
        # print(user)

def add_members_to_team():
    for member in user_list:
        print(member)


# get_members(r_one)
# get_members(r_two)
# add_members_to_team()
# update_team()
put_request()