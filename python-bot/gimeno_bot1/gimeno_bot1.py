from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# Get credentials from file
credentials = {}
with open("credentials.txt", 'r') as f:
    for line in f:
        lspl = line.split('=', 1)
        credentials[lspl[0]] = lspl[1]


line_bot_api = LineBotApi(credentials['CHANNEL_ACCESS'])
handler = WebhookHandler(credentials['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from_user = event.message.text

    if msg_from_user == 'hello':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='hi')
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


# Runs the app
if __name__ == "__main__":
    app.run()
