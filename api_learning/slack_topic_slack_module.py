import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

from dotenv import load_dotenv

# get path to current directory
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# prepend the .env file with current directory
load_dotenv(os.path.join(BASEDIR, '.env'))

client = WebClient(token=os.environ.get('SLACK_TOKEN'))

try:
  response = client.chat_postMessage(
    channel="UEPH6G519",
    text="Hello from your app! :tada:"
  )
  print("Succeeded!")
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
  # print("Failed!")