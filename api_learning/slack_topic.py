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

# Slack set topic URL
topic_url = 'https://slack.com/api/conversations.setTopic'
# Slack post message URL
post_message_url = 'https://slack.com/api/chat.postMessage'
# Slack token
slack_token = os.environ.get('SLACK_TOKEN')
# #it-support channel
slack_channel = 'G0125J6V866'

# list of IT Support members
it_list = ['hayden', 'adeel', 'alex']

it_dict = {
    'hayden': ['DEPF8CW2G', 'UEPH6G519'],
    'adeel': ['DHNT8FJ8G', 'UHNT8DGGY'],
    'alex': ['D0123FPLCE9', 'U011VK4K44S']
}

mention_dict = {
    'hayden': 'UEPH6G519',
    'adeel': 'UHNT8DGGY',
    'alex': 'U011VK4K44S'
}

# txt file which stores the schedule for the week
schedule_file = 'weekly_schedule.txt'

# list to store the weekly schedule
weekly_list = []

# grabs the current day
current_time = datetime.datetime.now()
# returns the current day in Monday, Tuesday etc format
current_day = current_time.strftime("%A")


def max_shifts(remove_from, how_many):
    # Ensures that no IT Member is placed on more than 2 shifts a week
    # https://stackoverflow.com/questions/38599066/removing-some-of-the-duplicates-from-a-list-in-python
    counts = Counter()
    for item in remove_from:
        counts[item] += 1
        if counts[item] > how_many:
            weekly_list.remove(item)


def fill_schedule():
    # Fills the weekly_list schedule and calls the max_shifts function to ensure
    # that no IT Member is placed on more than 2 shifts a week
    while len(weekly_list) != 5:
        weekly_list.append(choice(list(it_dict.keys())))
        max_shifts(weekly_list, 2)


def write_schedule(today):
    # If the day is Sunday, the schedule gets wiped
    if today == 'Sunday':
        with open(schedule_file, 'w') as file_object:
            for element in weekly_list:
                file_object.write(element + '\n')
        del weekly_list[:]
    else:
        print('Not re-writing schedule today.')


def read_schedule():
    with open(schedule_file) as file_object:
        lines = file_object.readlines()
        for line in lines:
            weekly_list.append(line.rstrip())
            # print(line)
    # print(weekly_list)


def compare_day_schedule():
    # Compares the schedule that was created by the fill_schedule function against the current day of the week
    # and returns the IT Member whose shift it is for the day
    for day in week_dict:
        if current_day == day:
            shift_member = week_dict[day]
            return shift_member
        else:
            continue


def get_shift_member_channel_id():
    name = f'{compare_day_schedule()}'
    # print(name)
    for key, value in it_dict.items():
        if name == key:
            # print(f'{key} + {value}')
            shift_member_id = value[0]
            return shift_member_id
        else:
            continue


def get_shift_member_user_id():
    name = f'{compare_day_schedule()}'
    # print(name)
    for key, value in it_dict.items():
        if name == key:
            # print(f'{key} + {value}')
            shift_member_id = value[1]
            return shift_member_id
        else:
            continue


def set_topic():
    # Post to Slack with the below topic, data to the channel above
    topic_post = requests.post(topic_url, data=topic_data)
    print(f'Topic POST response: {topic_post.status_code}')

    message_post = requests.post(post_message_url, data=message_data)
    print(f'Topic POST response: {message_post.status_code}')


# place content of this function into name == main
def saturday_deletion():
    # Clears weekly_list schedule on a Saturday or Sunday, if not weekend then set topic in Slack
    if current_day == 'Saturday' or current_day == 'Sunday':
        # del weekly_list[:]
        print(f'It is {current_day}')
    else:
        write_schedule(current_day)
        read_schedule()
        set_topic()

# get_date()
fill_schedule()

# Assigns a day to an IT Member
week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

topic = f'The #it-support shift member for the day is <@{get_shift_member_user_id()}>.'
topic_data = {
    'token': slack_token,
    'channel': slack_channel,
    'topic': topic
}

message_data = {
    'token': slack_token,
    'channel': get_shift_member_channel_id(),
    'text': f'<@{get_shift_member_user_id()}> you smell like beans'
}

# set_topic()
# saturday_deletion()
'''
NEED TO POTENTIALLY WRITE TO A FILE - SEND DMS BASED ON THIS FILE - CLEAR FILE ON SAT, RERUN SCRIPT/REPOPULATE ON SUN
'''
# write_schedule(current_day)
# read_schedule()
saturday_deletion()
# message_it_member()