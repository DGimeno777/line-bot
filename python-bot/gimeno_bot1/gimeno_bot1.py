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

credentials = {}
with open("credentials.txt", 'r') as f:
    for line in f:
        lspl = line.split('=', 1)
        credentials[lspl[0]] = lspl[1]


line_bot_api = LineBotApi(credentials['CHANNEL_ACCESS'])
handler = WebhookHandler(credentials['CHANNEL_SECRET'])

