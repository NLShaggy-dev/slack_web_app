import slack_sdk #slack SDK for python (originally called slackclient)
import os #used for environ method to get environment variable
from pathlib import Path #used for specifing path to .env file
from dotenv import load_dotenv #loads .env file for SLACK_TOKEN variable
from flask import Flask
from slackeventsapi import SlackEventAdapter

#defining path and loading SLACK_TOKEN variable
env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events',app)

#define client for connection to slack app
client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])
# get BOT ID
BOT_ID = client.api_call("auth.test")['user_id']

#Slack events API: grabs text sent to a channel and repeats message
@slack_events_adapter.on('message')
def message(payload):
    print(payload) # veiw payload info recieved
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

if __name__ == "__main__":
    app.run(debug=True)