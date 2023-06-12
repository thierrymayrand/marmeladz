from flask import Flask, request
import requests

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v10.0/me/messages'
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'  # replace 'YOUR_VERIFY_TOKEN' with your Facebook page's verify token
PAGE_ACCESS_TOKEN = 'YOUR_PAGE_ACCESS_TOKEN'  # replace 'YOUR_PAGE_ACCESS_TOKEN' with your Facebook page's access token

@app.route("/", methods=['GET'])
def listen():
    """This endpoint is for Facebook verification."""
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

@app.route("/", methods=['POST'])
def receive_message():
    """This endpoint is for processing incoming messaging events."""
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    event = messaging_event['message']
                    sender_id = messaging_event['sender']['id']
                    handle_message(sender_id, event)
    return "Message Processed"

def handle_message(sender_id, message):
    """Handle messages from users."""
    # TODO: Customize your bot's behavior here
    # This is where you'll define how your bot responds to messages sent by users
    text = message.get('text')
    send_message(sender_id, "You said: {}".format(text))

def send_message(recipient_id, text):
    """Send a response to Facebook."""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

if __name__ == "__main__":
    app.run(port=8000, debug=True)
