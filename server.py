from flask import Flask, request, json

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'your verify token' #openssl rand -base64 32
PAGE_ACCESS_TOKEN = 'your FB Page access token'

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is Hello bot response to '{}'".format(message)

def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        print("verified")
        return req.args.get("hub.challenge")
    else :
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)

def is_user_message(message):
    """Check if the message is a message from the user"""
    return(message.get('message') and message['message'].get('text'))

@app.route("/webhook", methods=['GET','POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    print("get response")
    if request.method == 'GET':
        print("get response")
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        print(payload)

        event = payload['entry'][0]['messaging']
        """ [{'message': 'TEST_MESSAGE'}] """
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id= x['sender']['id']
                respond(sender_id, text)
                print("respond " + '{}{}'.format(text, sender_id))

        return "200"
        

import requests

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message' : {
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
    
    """send data"""
    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    print("result {}".format(response.ok))
    
    return response.json()