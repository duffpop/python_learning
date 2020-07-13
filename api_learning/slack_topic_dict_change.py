import requests
import os
from dotenv import load_dotenv
from random import choice
import datetime
from collections import Counter
from slack import WebClient
from slack.errors import SlackApiError

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
# Slack module API token
client = WebClient(token=os.environ.get('SLACK_TOKEN'))


# #it-support-bantz channel
# slack_channel = 'G0125J6V866'

# #it-support-alerts channel
# slack_channel = 'C013XK82R24'

# #shift-bot-spam channel
slack_channel = 'C015SGU1LBV'


# list of IT Support members with the following value types
# {name: DM channel name, user ID} -- NOTE THAT THE DM CHANNEL NAME NEEDS TO BE THE USER ID WHEN USING AN APP TOKEN
# it_dict = {
#     'hayden': ['UEPH6G519', 'UEPH6G519'],
#     'adeel': ['UHNT8DGGY', 'UHNT8DGGY'],
#     'alex': ['U011VK4K44S', 'U011VK4K44S']
# }

# list of IT Support members with the following value types
# {name: DM channel name, user ID} -- NOTE THAT THE DM CHANNEL NAME NEEDS TO BE THE USER ID WHEN USING AN APP TOKEN
# it_dict = {
#     'hayden': ['DEPF8CW2G', 'UEPH6G519'],
#     'adeel': ['DHNT8FJ8G', 'UHNT8DGGY'],
#     'alex': ['D0123FPLCE9', 'U011VK4K44S']
# }

# All DMs go to Hayden but tags Alex, Adeel, Hayden - test Dict
it_dict = {
    'hayden': ['UEPH6G519', 'UEPH6G519'],
    'adeel': ['UEPH6G519', 'UHNT8DGGY'],
    'alex': ['UEPH6G519', 'U011VK4K44S']
}

# txt file which stores the schedule for the week
schedule_file = 'weekly_schedule.txt'

# list to store the weekly schedule
weekly_list = []

# day to wipe the schedule and repopulate it
rota_day = 'Saturday'

# grabs the current day
current_time = datetime.datetime.now()
# returns the current day in Monday, Tuesday etc format
current_day = current_time.strftime("%A")
# testing the current_day variable by hardcoding the day
current_day = 'Tuesday'


def max_shifts(remove_from, how_many):
    # Ensures that no IT Member is placed on more than 2 shifts a week
    # https://stackoverflow.com/questions/38599066/removing-some-of-the-duplicates-from-a-list-in-python
    counts = Counter()
    for item in remove_from:
        counts[item] += 1
        if counts[item] > how_many:
            weekly_list.remove(item)


def write_schedule(day):
    # If the day is Sunday, the schedule gets wiped
    if day == rota_day:
        with open(schedule_file, 'w') as file_object:
            for element in weekly_list:
                file_object.write(element + '\n')
        # del weekly_list[:]
    else:
        print('Not re-writing schedule today.')


def read_schedule():
    with open(schedule_file) as file_object:
        lines = file_object.readlines()
        if weekly_list:
            del weekly_list[:]
        for line in lines:
            weekly_list.append(line.rstrip())
            # print(line)
    # print(weekly_list)


def fill_schedule(day):
    # Fills the weekly_list schedule and calls the max_shifts function to ensure
    # that no IT Member is placed on more than 2 shifts a week
    if day == rota_day:
        while len(weekly_list) != 5:
            weekly_list.append(choice(list(it_dict.keys())))
            max_shifts(weekly_list, 2)
        write_schedule(current_day)
    else:
        read_schedule()


def today_shift_member():
    # Compares the schedule that was created by the fill_schedule function against the current day of the week
    # and returns the IT Member whose shift it is for the day
    for day in week_dict:
        if current_day == day:
            shift_member = week_dict[day]
            return shift_member
        else:
            continue


def get_shift_member_user_id():
    name = f'{today_shift_member()}'
    # print(name)
    # return it_dict[name]
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
    print(f'Topic POST response: {topic_post.content}')

    message_post = requests.post(post_message_url, data=message_data)
    print(f'Message POST response: {message_post.content}')


# place content of this function into name == main
def saturday_deletion(day):
    # Clears weekly_list schedule on a Saturday or Sunday, if not weekend then set topic in Slack
    if day == rota_day:
        # del weekly_list[:]
        write_schedule(current_day)
        print(f'It is {current_day}')
    else:
        write_schedule(current_day)
        read_schedule()
        set_topic()


# get_date()
fill_schedule(current_day)

# Assigns a day to an IT Member
week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

topic = f'The #it-support shift member for the day is <@{get_shift_member_user_id()}> whose name is {today_shift_member().title()}.'
topic_data = {
    'token': slack_token,
    'channel': slack_channel,
    'topic': topic
}

message_data = {
    'token': slack_token,
    'channel': get_shift_member_user_id(),
    'text': f'<@{get_shift_member_user_id()}> :snake:'
}

# saturday_deletion(current_day)

if __name__ == "__main__":
    # fill_schedule(current_day)
    saturday_deletion(current_day)