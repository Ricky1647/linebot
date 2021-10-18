from flask import Flask
#from werkzeug.datastructures import T #架站軟體 做route回應
app = Flask(__name__) # route 設定
from flask import request,abort #request接收訊息
from linebot import LineBotApi,WebhookHandler # LINEBOTAPI接收訊息 # handle 識別碼
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
import numpy as np
from linebot.models import *
import tempfile
import os
## 授權
line_bot_api = LineBotApi("r7Zq64defLm6ZXPBwUUT8AS+/5Rbau+jUnOY+lcDWTx+p/b0pX94AdeSbiPrGuxMDDkDfy6m0GQcJcLNc7Y5Ie49HQh+dl8nmJytkntT52AA3XAgO83kqGrntlNFOoaInPOJD0QAqbd/E6jZFoPFtQdB04t89/1O/w1cDnyilFU=")
## channel secert
handler = WebhookHandler("cfc2857f38799f624e02148130e0706c")
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# @app.route("/",methods=["POST"]) # 接收資料 不傳密碼
# def callback(): #回覆函數 
#     signature = request.headers["X-Line-Signature"] #查詢簽名
#     body = request.get_data(as_text = True) # get 
#     try:
#         handler.handle(body,signature) 
#     except InvalidSignatureError:
#         abort(500)
#     return "OK"

# @handler.add(MessageEvent,message= TextMessage)  # handler become router cope with textmessage
# def handle_message(event):
#     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
# 回覆訊息 event連接 text event所送過來的文字
# event.replt_token識別跟誰對話
# TextSendMessage(text=event.message.text)) event的message
dic = {0 : '三杯雞', 1 : '什錦炒麵',2:"咖哩雞",3:"塔香海茸",4:"大陸妹",5:"客家小炒",6:"小番茄",7:"有機小松菜",8:"有機青松菜",9:"木瓜",
        10:"柳丁",11:"棗子",12:"橘子",13:"沙茶肉片",14:"油菜",15:"洋蔥炒蛋",16:"滷蛋",17:"滷雞腿",18:"玉米炒蛋",19:"瓜仔肉",
        20:"番茄炒蛋",21:"白米飯",22:"白菜滷",23:"福山萵苣",24:"空心菜",25:"糖醋雞丁",26:"紅蘿蔔炒蛋",27:"義大利麵",28:"芥藍菜",29:"菠菜",
        30:"葡萄",31:"蒜泥白肉",32:"蒸蛋",33:"蓮霧",34:"螞蟻上樹",35:"西瓜",36:"豆芽菜",37:"關東煮",38:"青江菜",39:"香蕉",40:"香酥魚排",
        41:"馬鈴薯燉肉",42:"高麗菜",43:"鳳梨'",44:"鵝白菜",45:"鹽酥雞",46:"麥克雞塊",47:"麻婆豆腐",48:"麻油雞",49:"黑胡椒豬柳"}
model = load_model('model.h5')
def predict_label(img_path):
    i = image.load_img(img_path, target_size=(224,224))
    #i = image.img_to_array(i)/255.0
	#i = i.reshape(None,224,224,3)
    #i = np.expand_dims(i,axis=0)
    i  = np.expand_dims( i , axis = 0) 
    p = model.predict(i)[0]
    top = p.argsort()[::-1][:5]
    return dic[top[0]]
@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
@handler.add(MessageEvent,message= TextMessage)  # handler become router cope with textmessage
def handle_message(event):
    message = TextSendMessage(text='哈囉你好，第一道謎題，請問某水果以屏東黑珍珠著稱，請回傳圖片解題！')
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='哈囉你好，第一道謎題，請問某水果以屏東黑珍珠著稱，請回傳圖片解題！'))
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    
    #line_bot_api.reply_message(event.reply_token, message)
    if isinstance(event.message,ImageMessage):
        ext = "jpg"
        #line_bot_api.reply_message(event.reply_token, message)
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        res = predict_label(dist_path)
        if(res=="蓮霧"):
            message =TextSendMessage(text="答對了，是蓮霧")
        else:
            message = TextSendMessage(text="答錯了，你給的是{}".format(res))
        line_bot_api.reply_message(event.reply_token, message)
    #print('-----------------')
    # if event.message.type=="image":
    #     #line_bot_api.reply_message(event.reply_token,message)
    #     res = predict_label(event.message)
    #     line_bot_api.reply_message(event.reply_token,res)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

# @handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
# def handle_content_message(event):
#     if event.message.type=="image":
#         line_bot_api.reply_message(event.reply_token,"ff")


if __name__ == "__main__":
    app.run()