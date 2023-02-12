from flask import Flask, request
import requests
import json
import re
import os
app = Flask(__name__)

# Replace ACCESS_TOKEN or fill in env with your own Line Messaging API access token
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

# This function is used to send the message to Line Platform
def reply(reply_token, message):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=data)
    return response.json()

# This function is used to send the message to API
def send_message_to_gpt2(text):
    headers = {
        "Content-Type": "application/json",
    }
    # data = {"prompt": text, "max_tokens": 100}
    try:
        response =  requests.post(url='https://hf.space/embed/xibaozi/gpt2-chitchat/+/api/predict/', headers=headers, json={"data":[text]})
        response = json.loads(response.text)
        response = response["data"]
        response = re.sub(r"【.+】|\s+", "", str(response))
        response = re.sub(r"[^\w\s]", "", str(response))
    except Exception as e:
        # if error output error infomation
        response = e
    return response

# This is the main function to handle incoming messages
def handle_message(event):
    try:
        message = event["message"]["text"]
        user_id = event["source"]["userId"]
        response = send_message_to_gpt2(message)
        gpt2_response = response
        reply(event["replyToken"], gpt2_response)
    except Exception as e:
        # if error pass
        pass

@app.route("/bot", methods=["POST"])
def handle_request():
    event = request.get_json()
    # show event in console
    print(event)
    for e in event["events"]:
        handle_message(e)
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=False)
