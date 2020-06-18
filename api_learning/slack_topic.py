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
url = 'https://slack.com/api/conversations.setTopic'
slack_token = os.environ.get('SLACK_TOKEN')
# #it-support channel
slack_channel = 'G0125J6V866'

# list of IT Support members
it_list = ['hayden', 'adeel', 'alex']

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
        weekly_list.append(choice(it_list))
        max_shifts(weekly_list, 2)


def write_schedule(today):
    if today == 'Sunday':
        with open(schedule_file, 'w') as file_object:
            for element in weekly_list:
                file_object.write(element + '\n')
    else:
        print('Not re-writing schedule today.')


def read_schedule():
    with open(schedule_file) as file_object:
        lines = file_object.readlines()
        for line in lines:
            weekly_list.append(line.rstrip())
            # print(line)
    print(weekly_list)


def compare_day_schedule():
    # Compares the schedule that was created by the fill_schedule function against the current day of the week
    # and returns the IT Member whose shift it is for the day
    for day in week_dict:
        if current_day == day:
            shift_member = week_dict[day]
            return shift_member
        else:
            continue


def set_topic():
    # Post to Slack with the below topic, data to the channel above
    r = requests.post(url, data=data)
    print(r.status_code)


# place content of this function into name == main
def saturday_deletion():
    # Clears weekly_list schedule on a Saturday or Sunday, if not weekend then set topic in Slack
    if current_day == 'Saturday' or current_day == 'Sunday':
        # del weekly_list[:]
        print(f'It is {current_day}')
    else:
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

topic = f'The #it-support shift member for the day is {compare_day_schedule().title()}.'
data = {'token': slack_token,
        'channel': slack_channel,
        'topic': topic}

# set_topic()
# saturday_deletion()
'''
NEED TO POTENTIALLY WRITE TO A FILE - SEND DMS BASED ON THIS FILE - CLEAR FILE ON SAT, RERUN SCRIPT/REPOPULATE ON SUN
'''
write_schedule(current_day)