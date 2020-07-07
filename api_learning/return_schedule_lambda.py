import boto3
import datetime

s3_client = boto3.resource('s3')
bucket = s3_client.Bucket('weekly-schedule')
file_name = "weekly_schedule.txt"
object_name = file_name
lambda_path = ("/tmp/" + file_name)

today = datetime.date.today()
week_beginning = today - datetime.timedelta(days=today.weekday())
week_beginning = week_beginning.strftime("%d/%m/%Y")

weekly_list = []

def schedule_formatter():
    bucket.download_file(file_name, lambda_path)
    with open(lambda_path, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            weekly_list.append(line.rstrip())


schedule_formatter()

week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

def lambda_handler(event, context):
    return {
        "response_type": "in_channel",
        "text": (f'The schedule for the week beginning *{week_beginning}* is as follows:'
                 f'\n\t• Monday: {week_dict["Monday"].title()}'
                 f'\n\t• Tuesday: {week_dict["Tuesday"].title()}'
                 f'\n\t• Wednesday: {week_dict["Wednesday"].title()}'
                 f'\n\t• Thursday: {week_dict["Thursday"].title()}'
                 f'\n\t• Friday: {week_dict["Friday"].title()}')
    }
