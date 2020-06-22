import os
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.errors import SlackApiError

# This `app` represents your existing Flask app
app = Flask(__name__)

# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    token = payload.get('token', {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    try:
        # reply for a text which says start
        if text.lower() == "start":
            return slack_web_client.chat_postMessage(channel=channel_id, text='hello world')
        if text.lower() == "s":
            return slack_web_client.files_upload( channels=channel_id,file='./cv.pdf')

    except SlackApiError as e:
        print(e)


# Start the server on port 3000
if __name__ == "__main__":
    app.run(port=3000)
