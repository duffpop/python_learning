import logging
import os
from random import choice
import datetime
from collections import Counter
from botocore.vendored import requests
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

slack_token = os.environ.get('SLACK_TOKEN')

s3_client = boto3.resource('s3')
bucket = s3_client.Bucket('weekly-schedule')
file_name = "weekly_schedule.txt"
object_name = file_name
lambda_path = ("/tmp/" + file_name)

# Slack set topic URL
topic_url = 'https://slack.com/api/conversations.setTopic'
# Slack post message URL
post_message_url = 'https://slack.com/api/chat.postMessage'

'''
Required API scopes:
    - channels:manage - Manage public channels - to set channel topic for #it-support - NOT YET IMPLEMENTED
    - groups:write - Manage private channels - to set channel topic for #it-support-team-bantz
    - im:write - DM people - to send the IT Support shift member a DM notifying them that they're on shift

EventBridge/CloudWatch Cron expression example:
    - 37 11 ? * MON-SAT *
    - Runs at 11:37 UTC, Monday-Saturday 
'''

# #it-support-bantz channel
slack_channel = 'G0125J6V866'

# #it-support-alerts channel
# slack_channel = 'C013XK82R24'

# #shift-bot-spam channel
# slack_channel = 'C015SGU1LBV'

# list of IT Support members with the following value types
# {name: DM channel name, user ID} -- NOTE THAT THE DM CHANNEL NAME NEEDS TO BE THE USER ID WHEN USING AN APP TOKEN
it_dict = {
    'hayden': ['UEPH6G519', 'UEPH6G519'],
    'adeel': ['UHNT8DGGY', 'UHNT8DGGY'],
    'alex': ['U011VK4K44S', 'U011VK4K44S'],
    'owain': ['U01A8GHKS0Y', 'U01A8GHKS0Y']
}

# All DMs go to Hayden but tags Alex, Adeel, Hayden - test Dict
# it_dict = {
#     'hayden': ['UEPH6G519', 'UEPH6G519'],
#     'adeel': ['UEPH6G519', 'UHNT8DGGY'],
#     'alex': ['UEPH6G519', 'U011VK4K44S'],
#     'owain': ['UEPH6G519', 'U01A8GHKS0Y']
# }

# txt file which stores the schedule for the week
schedule_file = 'weekly_schedule.txt'

# list to store the weekly schedule
# weekly_list = ['alex', 'alex', 'hayden', 'hayden', 'alex']
weekly_list = []

# day to wipe the schedule and repopulate it
rota_day = 'Friday'

# grabs the current day
current_time = datetime.datetime.now()
# returns the current day in Monday, Tuesday etc format
current_day = current_time.strftime("%A")
## testing the current_day variable by hardcoding the day
# current_day = 'Saturday'

# A dict showing exceptions for the week
# TODO pull holiday data from bob and feed into this dict
schedule_exceptions = {
    'Monday': None,
    'Tuesday': 'owain',
    'Wednesday': None,
    'Thursday': None,
    'Friday': None
}


def max_shifts(remove_from, how_many):
    # Ensures that no IT Member is placed on more than 2 shifts a week
    # https://stackoverflow.com/questions/38599066/removing-some-of-the-duplicates-from-a-list-in-python
    counts = Counter()
    for item in remove_from:
        counts[item] += 1
        if counts[item] > how_many:
            weekly_list.remove(item)


def min_shifts(schedule_list, how_many):
    counts = Counter(schedule_list)
    it_names = [name for name, slack_info in it_dict.items()]
    most_common_name = [most_common_member for most_common_member, number in counts.most_common(1)]

    for member in it_names:
        if len(schedule_list) == 5 and member not in schedule_list:
            schedule_list.remove(most_common_name[0])

    if len(schedule_list) == 5:
        for most_common_member, number in counts.most_common():
            if number < how_many:
                schedule_list.remove(most_common_name[0])


def member_day_exclusion(member_to_exclude, day, schedule):
    member_to_exclude = member_to_exclude.lower()
    day = day.title()

    while len(schedule) == 5:
        if day == 'Monday':
            assigned_member = schedule[0]
        elif day == 'Tuesday':
            assigned_member = schedule[1]
        elif day == 'Wednesday':
            assigned_member = schedule[2]
        elif day == 'Thursday':
            assigned_member = schedule[3]
        elif day == 'Friday':
            assigned_member = schedule[4]
        else:
            print('Day entered is incorrect. Please enter a day from the week_dict keys.')

        if len(schedule) == 5 and assigned_member == member_to_exclude:
            schedule.remove(assigned_member)
            # The below line may need removing, it means that Owain will have two shifts on weeks
            # where he was chosen to work on Tuesdays
            schedule.append(assigned_member)
            break
        else:
            break


def write_schedule(day):
    # If the day is Sunday, the schedule gets wiped
    if day == rota_day:
        with open(lambda_path, 'w+') as file_object:
            for element in weekly_list:
                file_object.write(element + '\n')
        bucket.upload_file(lambda_path, file_name)
    else:
        print('Not re-writing schedule today.')


def read_schedule():
    # s3_client.meta.client.download_file(bucket, object_name, file_name)
    bucket.download_file(file_name, lambda_path)
    with open(lambda_path, 'r') as file_object:
        lines = file_object.readlines()
        if weekly_list:
            del weekly_list[:]
        for line in lines:
            weekly_list.append(line.rstrip())


def fill_schedule(day):
    # Fills the weekly_list schedule and calls the max_shifts function to ensure
    # that no IT Member is placed on more than 2 shifts a week
    if day == rota_day:
        while len(weekly_list) != 5:
            weekly_list.append(choice(list(it_dict.keys())))
            max_shifts(weekly_list, 2)
            min_shifts(weekly_list, 1)
            member_day_exclusion('owain', 'Tuesday', weekly_list)
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


def get_shift_member_channel_id():
    name = f'{today_shift_member()}'
    # print(name)
    for key, value in it_dict.items():
        if name == key:
            # print(f'{key} + {value}')
            shift_member_id = value[0]
            return shift_member_id
        else:
            continue


def get_shift_member_user_id():
    name = f'{today_shift_member()}'
    # print(name)
    for key, value in it_dict.items():
        if name == key:
            # print(f'{key} + {value}')
            shift_member_id = value[1]
            return shift_member_id
        else:
            continue


def set_topic():
    topic_post = requests.post(topic_url, data=topic_data)
    try:
        topic_post.status_code
        print(f'Status code: {topic_post.status_code}')
        print(f'Content: {topic_post.content}')
    except Exception as e_set_topic:
        # You will get a SlackApiError if "ok" is False
        LOGGER.error(
            f'Error setting Slack topic with return code {topic_post.status_code}: {e_set_topic}'
        )
        raise


def post_message():
    message_post = requests.post(post_message_url, data=message_data)
    try:
        message_post.status_code
        print(f'Status code: {message_post.status_code}')
        print(f' C{message_post.content}')
    except Exception as e_message_post:
        # You will get a SlackApiError if "ok" is False
        LOGGER.error(
            f'Error messaging user {get_shift_member_user_id()}, return code {message_post.status_code}: {e_message_post}'
        )


# place content of this function into name == main
def saturday_deletion(day):
    # Clears weekly_list schedule on a Saturday or Sunday, if not weekend then set topic in Slack
    if day == rota_day:
        write_schedule(current_day)
        print(f'It is {current_day}.')
    else:
        print(f'It is {current_day}.')
        write_schedule(current_day)
        read_schedule()
        set_topic()
        post_message()


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

topic = f'The <#CHGUTD9PV> shift member for the day is <@{get_shift_member_user_id()}>.'

topic_data = {
    'token': slack_token,
    'channel': slack_channel,
    'topic': topic
}

message_data = {
    'token': slack_token,
    'channel': get_shift_member_channel_id(),
    'text': f'<@{get_shift_member_user_id()}> you are keeping an eye on <#CHGUTD9PV> today, try to respond within an hour at all times :party_parrot:'
}


def lambda_handler(event, context):
    saturday_deletion(current_day)
    response = {'statusCode': 200, 'body': ''}
    return response
