# 用flask 架設伺服器
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, VideoSendMessage
)

app = Flask(__name__)

# Channel access token
line_bot_api = LineBotApi('R6WS+FrE4vSkN0HSfDdj4jNB4cngBifDVw7yRBARu2tpCdqyCZDFuMcVRuD06Cgo/WUIm4yk5Hj6I9exPP0hRQdoInkPBNnliRuRgywmmDp6V5Ruz81VL1COEggCiL+D4I85gocP39MPOXdgq3NNtQdB04t89/1O/w1cDnyilFU=')
# Channel secret
handler = WebhookHandler('9cc85ca5db0abd79a24e485dcf9ae869')


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
    msg = event.message.text
    req = TextSendMessage(text="女神那麼正還不看來影片?")
    sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002747')
    video_message = VideoSendMessage(
        original_content_url='https://www.youtube.com/watch?v=aV4S2YYCYe0')

    r = [req, video_message, sticker_message]

    line_bot_api.reply_message(
        event.reply_token,
        r)

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     StickerSendMessage(package_id='11537', sticker_id='52002747'))


if __name__ == "__main__":
    app.run()