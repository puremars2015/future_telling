from flask import Flask, request, jsonify, render_template, abort
from openai import OpenAI

import requests
import json


app = Flask(__name__)

# 設置您的 OpenAI API 密鑰
api_key = "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"

GPT = OpenAI(api_key=api_key)


# 你的 Line Bot 的 Channel Access Token 和 Channel Secret
CHANNEL_ACCESS_TOKEN  = '+qIW8NAe7IiO3ounSajStjlKuAvvKSJfSz7qVvkVRSUHBAahZMM+ex1jnvA1S74DVwfkp2s0VTeR5yh7e+dWZEr8K9BFfEtsy9Rj2EWJrOjsJGaL/VyvZLwBAGg2qgD+cE1mpr5CojUfSGyb0mzN4gdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET  = '7573464c1e3506a13bc8bce074e4a873'



@app.route('/', methods=['GET','POST'])
def default():
    return jsonify(message="200 OK"), 200


def reply_message(reply_token, message):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    body = {
        'replyToken': reply_token,
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_json()
    events = body.get('events', [])
    
    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            reply_token = event['replyToken']
            user_message = event['message']['text']
            
            explain_response = GPT.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個聊天的好夥伴"},
                    {"role": "user", "content": f"{user_message}"}
                ]
            )
            explain = explain_response.choices[0].message.content

            reply_message(reply_token, f'{explain}')
    
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True)