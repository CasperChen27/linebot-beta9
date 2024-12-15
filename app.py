from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexMessage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
import os
import json

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_Template_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # Buttons Template
        if text == '地址':
            url = request.url_root + 'static/Guns&Roses.jpg'
            url = url.replace("https", "http")
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='槍與玫瑰',
                text='營業時間21:30-02:00，歡迎捧場!',
                actions=[
                   # URIAction(label='fb連結', uri='https://www.facebook.com/GunsNRosesBar/?ref=bookmarks&_rdr'),
                   # URIAction(label='instagram連結', uri='https://www.instagram.com/guns__roses_bar/'),
                    URIAction(label='店家地址(Google Map)', uri='https://www.google.com/maps?q=621%E5%98%89%E7%BE%A9%E7%B8%A3%E6%B0%91%E9%9B%84%E9%84%89%E8%A3%95%E8%BE%B2%E4%B8%80%E8%A1%9723%E8%99%9F%E6%A7%8D%E8%88%87%E7%8E%AB%E7%91%B0&ftid=0x346ebe50129cbe03:0xe69959cc7d9c99c0&entry=gps&lucs=,94246480,94242505,94224825,94227247,94227248,47071704,47069508,94218641,94228354,94233079,94203019,47084304,94208458,94208447&g_ep=CAISEjI0LjQ3LjMuNjk4NTMxOTU1MBgAIJ6dCip-LDk0MjQ2NDgwLDk0MjQyNTA1LDk0MjI0ODI1LDk0MjI3MjQ3LDk0MjI3MjQ4LDQ3MDcxNzA0LDQ3MDY5NTA4LDk0MjE4NjQxLDk0MjI4MzU0LDk0MjMzMDc5LDk0MjAzMDE5LDQ3MDg0MzA0LDk0MjA4NDU4LDk0MjA4NDQ3QgJUVw%3D%3D&g_st=com.google.maps.preview.copy'),
                    # PostbackAction(label='回傳值', data='ping', displayText='傳了'),
                    # MessageAction(label='傳"哈囉"', text='哈囉'),
                    # DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
                    # CameraAction(label='拍照'),
                    # CameraRollAction(label='選擇相片'),
                    # LocationAction(label='選擇位置')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        #店內特調
        elif text == '店內特調':
            url = request.url_root + 'static/saton.png'
            url = url.replace("https", "http")
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        # ImageCarousel Template
        elif text == 'ig':
            url = request.url_root + 'static/'
            url = url.replace("https", "http")
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=url+'guns&rosesig.png',
                        action=URIAction(
                            label='造訪我們的IG',
                            uri='https://www.instagram.com/guns__roses_bar/'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=url+'guns&rosesfb.png',
                        action=URIAction(
                            label='造訪我們的FB',
                            uri='https://www.facebook.com/GunsNRosesBar/'
                        )
                    ),
                    #ImageCarouselColumn(
                     #   image_url=url+'youtube.png',
                      #  action=URIAction(
                       #     label='造訪YT',
                        #    uri='https://www.youtube.com/@bigdatantue'
                       # )
                    #),
                ]
            )

            image_carousel_message = TemplateMessage(
                alt_text='傳送一則訊息',
                template=image_carousel_template
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_carousel_message]
                )
            )
            
   #推薦
        elif text == '推薦':
            line_flex_json = {
                "type": "carousel",
                "contents": [
                    {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://i.ibb.co/mHTXTXD/seven.png",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1"
                    }
                    },
                    {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://i.ibb.co/mywYkHz/gap.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1"
                    }
                    },
                    {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://i.ibb.co/3MSGzpF/plato.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1"
                    }
                    }
                ]
            }
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='推薦飲品', contents=FlexContainer.from_json(line_flex_str))]
                )
            )  



if __name__ == "__main__":
    app.run()