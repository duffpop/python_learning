import requests
import os
from dotenv import load_dotenv
from random import choice
import datetime
from collections import Counter

# get path to current directory
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# prepend the .env file with current directory
load_dotenv(os.path.join(BASEDIR, '.env'))

url = 'https://slack.com/api/conversations.setTopic'
slack_token = os.environ.get('SLACK_TOKEN')
slack_channel = 'G0125J6V866'

it_list = ['hayden', 'adeel', 'alex']
random_it_member = choice(it_list)

weekly_list = []

current_time = datetime.datetime.now()
current_day = current_time.strftime("%A")


def max_shifts(remove_from, how_many):
    # https://stackoverflow.com/questions/38599066/removing-some-of-the-duplicates-from-a-list-in-python
    counts = Counter()
    for item in remove_from:
        counts[item] += 1
        if counts[item] > how_many:
            weekly_list.remove(item)


def fill_schedule():
    while len(weekly_list) != 5:
        weekly_list.append(choice(it_list))
        max_shifts(weekly_list, 2)


def compare_day_schedule():
    for day in week_dict:
        if current_day == day:
            shift_member = week_dict[day]
            return shift_member
        else:
            continue


def set_topic():
    r = requests.post(url, data=data)
    print(r.status_code)


def saturday_deletion():
    if current_day == 'Saturday' or current_day == 'Sunday':
        # del weekly_list[:]
        print(f'It is {current_day}')
    else:
        set_topic()


# get_date()
fill_schedule()

week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

topic = f'The #it-support shift member for the day is {compare_day_schedule().title()}.'

data = {'token': slack_token,
        'channel': slack_channel,
        'topic': topic}

# set_topic()
saturday_deletion()
'''
NEED TO POTENTIALLY WRITE TO A FILE - SEND DMS BASED ON THIS FILE - CLEAR FILE ON SAT, RERUN SCRIPT/REPOPULATE ON SUN
'''