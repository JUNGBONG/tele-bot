import os
import requests
import json
token = os.getenv('TELE_TOKEN')
method = 'getUpdates'
# c9에서 텔레그램 api 막음 ㅠㅠㅠ
# url = "https://api.telegram.org/bot{}/{}".format(token,method)
url = "https://api.hphk.io/telegram/bot{}/{}".format(token,method)

res = requests.get(url).json()

user_id = res["result"][0]["message"]["from"]["id"]
msg = "호" 

method = 'sendMessage'
msg_url = "https://api.hphk.io/telegram/bot{}/{}?chat_id={}&text={}".format(token, method,user_id,msg)

requests.get(msg_url)