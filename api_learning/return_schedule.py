# import boto3

# s3_client = boto3.resource('s3')
# bucket = s3_client.Bucket('weekly-schedule')
# file_name = "weekly_schedule.txt"
# object_name = file_name
# lambda_path = ("/tmp/" + file_name)

file_name = 'weekly_schedule.txt'

weekly_list = []


def schedule_formatter():
    with open(file_name) as file_object:
        lines = file_object.readlines()
        for line in lines:
            weekly_list.append(line.rstrip())


schedule_formatter()
# print(weekly_list)

week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         "response_type": "in_channel",
#         "text": week_dict
#     }

other_dict = {
    "hello": "there"
}

print(week_dict)
# print(other_dict)

"""
    with open(schedule_file) as file_object:
        lines = file_object.readlines()
        if weekly_list:
            del weekly_list[:]
        for line in lines:
            weekly_list.append(line.rstrip())
"""