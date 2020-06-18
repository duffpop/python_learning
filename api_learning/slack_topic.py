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

# topic = f'The #it-support IT guy for the day is {random_it_member.title()}'

weekly_list = []


# def get_date():
current_time = datetime.datetime.now()
current_day = current_time.strftime("%A")
    # return current_day


def max_shifts(remove_from, how_many):
    # https://stackoverflow.com/questions/38599066/removing-some-of-the-duplicates-from-a-list-in-python
    counts = Counter()
    for item in remove_from:
        counts[item] += 1
        if counts[item] > how_many:
            # yield item
            # max_shift_list.append(item)
            weekly_list.remove(item)


def fill_schedule():
    while len(weekly_list) != 5:
        weekly_list.append(choice(it_list))
        max_shifts(weekly_list, 2)


def compare_day_schedule():
    # if week_dict.keys() == current_day:
    #     print(week_dict.keys())
    for day in week_dict:
        if current_day == day:
            # print(week_dict[day])
            shift_member = week_dict[day]
            return shift_member
        else:
            # print("Day incorrect")
            continue


def set_topic():
    r = requests.post(url, data=data)
    print(r.status_code)


# get_date()
fill_schedule()

week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

topic = f'The #it-support IT guy for the day is {compare_day_schedule().title()}.'

data = {'token': slack_token,
        'channel': slack_channel,
        'topic': topic}

# print(week['Monday'].title())
# print(week)

# for day in week.values():
#     print(day)

    # while len(weekly_list) < 6:
    #     weekly_list.append(choice(it_list))
        # print(len(weekly_list))
        # keep_n_dupes(weekly_list, 2)

    # del weekly_list[-1]
    # keep_n_dupes(weekly_list, 2)
    # print(weekly_list)
    # print(max_shift_list)
# print(list(keep_n_dupes(weekly_list, 2)))

# print(len(it_list))

# print(week_dict)
# compare_day_schedule()
# print(compare_day_schedule())
print(topic)