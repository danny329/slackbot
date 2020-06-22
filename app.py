import os
from flask import Flask, json, request, Response, make_response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.errors import SlackApiError

# This `app` represents your existing Flask app
app = Flask(__name__)

blocks = '''[
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Daniel want to send a interactive message\nselect one option",
				"emoji": true
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "option 1",
						"emoji": true
					},
					"value": "click_me_1"
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "option 2",
						"emoji": true
					},
					"action_id": "button2",
					"value": "click_me_2"
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "option 3",
						"emoji": true
					},
					"value": "click_me_3"
				}
			]
		}
	]'''

message_attachments = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "games_list",
                "text": "Pick a game...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]
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
        if text:
            # reply for a text which says start with text
            if text.lower() == "start":
                return slack_web_client.chat_postMessage(channel=channel_id, text='hello world')
            # reply for with a file
            if text.lower() == "s":
                return slack_web_client.files_upload(channels=channel_id, file='./cv.pdf')
            # reply with interactive message select from drop down external
            if text.lower() == "ide":
                return slack_web_client.chat_postMessage(channel=channel_id, attachments=message_attachments)
            # reply with interactive message select from drop down external
            if text.lower() == "ibi":
                return slack_web_client.chat_postMessage(channel=channel_id, blocks=blocks)

    except SlackApiError as e:
        print(e)


@app.route("/slack/options-load-endpoint", methods=["POST"])
def options_load_endpoint():
    # Parse the request payload
    payload = json.loads(request.form["payload"])
    print(payload)
    menu_options = {
        "options": [
            {
                "text": "Chess",
                "value": "chess"
            },
            {
                "text": "Global Thermonuclear War",
                "value": "war"
            }
        ]
    }

    return Response(json.dumps(menu_options), mimetype='application/json')


@app.route("/slack/interactive-endpoint", methods=["POST"])
def interactive_endpoint():
    # Parse the request payload
    payload = json.loads(request.form["payload"])
    print(payload)
    if payload['type'] == 'block_actions':
        if payload['actions'][0]['type'] == 'button':
            value = payload['actions'][0]['value']
            print(value)
            response = slack_web_client.chat_update(channel=payload["channel"]["id"], ts=payload['container']["message_ts"],
                                                    text=value, attachments=[])
    else:
        # Check to see what the user's selection was and update the message
        selection = payload["actions"][0]["selected_options"][0]["value"]

        if selection == "war":
            message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
        else:
            message_text = ":horse:"

        response = slack_web_client.chat_update(channel=payload["channel"]["id"], ts=payload["message_ts"],
                                                text=message_text, attachments=[])

    return make_response("", 200)


# Start the server on port 3000
if __name__ == "__main__":
    app.run(port=3000)
ACTIONS = [
    {
     'action_id': 'HM/pX',
     'block_id': '7hNh',
     'text': {
         'type': 'plain_text',
         'text': 'option 1',
         'emoji': True
            },
     'value': 'click_me_1',
     'type': 'button',
     'action_ts': '1592832241.363170'
     }
]