from flask import Flask, request, abort
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    TextMessage, ReplyMessageRequest
)
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# 您的 Channel Access Token 和 Channel Secret
CHANNEL_ACCESS_TOKEN = '+fZiXSR1sw0MzCRsSK3Jq5ucmQJG2mN+B5bnuKk7P6hdCBBEUs5uN3/7mHFvS7K5kUq2Up0iPF0Mk20UTRXDoBBvFUIxTX+XSqjYsPL/ioVN9JgdkRWe3tlFL9lyRUpmmA3MnPjnsrsCpt7h8VPPBgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '556cca6ba6eb2072715fcfbc2e176bcc'

app = Flask(__name__)

# 初始化 LINE Bot API 與 Webhook Handler
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(ApiClient(configuration))
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    print("📩 Received body:\n", body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Invalid signature.")
        # 重要：即使簽名無效，仍返回200
        return 'OK', 200
    except Exception as e:
        print("⚠️ 其他錯誤:", e)
        # 重要：任何情況下都返回200
        return 'OK', 200
    
    # 確保最後一定返回200
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_msg = event.message.text  # 使用者輸入的訊息

        if "早安" in user_msg:
            reply_text = "🌅 早安！今天也要加油喔！"
        elif "吃了什麼" in user_msg:
            reply_text = "🍱 記得傳送你的餐點照片給我！"
        elif "訓練" in user_msg:
            reply_text = "💪 今天訓練什麼呢？記得做好暖身喔！"
        elif "晚餐" in user_msg:
            reply_text = "🍽️ 晚餐吃什麼好呢？營養要均衡喔！"
        else:
            reply_text = "✅ 我收到你的訊息了！👍"

        print(f"📝 回應用戶：{event.reply_token}，內容：{event.message.text}")
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )
    except Exception as e:
        print("⚠️ 回覆訊息失敗：", e)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

