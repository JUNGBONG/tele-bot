#값을 숨기기 위해 os를 import한다.
#flask의 Flask와 request를 import한다.
#문장을 더 보기 편하게 하기 위해 pprint를 import한다.
#get과 post하기위해 requests를 import한다.
#로또번호 뽑기위해 randm을 import한다.

import os
from flask import Flask, request
from pprint import pprint as pp
import requests
import random


#구글에flask 검색후 다섯줄 복사
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    

#c9에서 텔레그램이 막혀있으므로 우회주소 사용
api_url = 'https://api.hphk.io/telegram'
token = os.getenv('TELE_TOKEN')
    

#bashrc안에 등록후 토큰,아이디,비밀번호 사용
@app.route(f'/{token}',methods=['POST'])
def telegram():
    #naver api 를 사용하기 위한 변수
    naver_client_id =os.getenv("NAVER_ID")
    naver_client_secret =os.getenv("NAVER_SECRET")
    
    
    
    #tele_dict = 데이터 덩어리
    tele_dict = request.get_json()
    pp(request.get_json())
    #유저 정보
    chat_id = tele_dict["message"]["from"]["id"]
    # print(chat_id)
    #유저가 입력한 데이터
    text = tele_dict.get("message").get("text")
    #안녕하세요
    #로또
    #번역 안녕하세요 =>번역
    
    
    
    #번역 번역하고싶은말 => 번역하고싶은말로 출력
    tran = False
    img = False
    # 사용자가 이미지를 넣었는지 체크
    
    # if tele_dict['message']['photo'] is not None:
    if tele_dict.get('message').get('photo') is not None:
        img = True
    #text(유저가입력한데이터) 제일 앞 두글자가 번역?
    else:
        if text[:2]=="번역":
            # 번역안녕하세요
            tran = True
            text = text.replace("번역","")
            #  안녕하세요
    # print(text)
    # naver api 사용
    if tran:
        papago = requests.post("https://openapi.naver.com/v1/papago/n2mt",
                    headers ={
                        "X-Naver-Client-Id":naver_client_id,
                        "X-Naver-Client-Secret":naver_client_secret
                    },
                    data ={
                        'source':'ko',
                        'target':'en',
                        'text':text
                    }
                    
        )
        #강사님 코드
        pp(papago.json())
        text = papago.json()['message']['result']['translatedText']
        
        # papago_dict =papago.json()
        # text = papago_dict["message"]["result"]["translatedText"]
    
    elif img:
        text = "사용자가 이미지를 넣었어요"
        # 텔레그램에게 사진 정보 가져오기 
        file_id = tele_dict['message']['photo'][-1]['file_id']
        file_path = requests.get(f"{api_url}/bot{token}/getFile?file_id={file_id}").json()['result']['file_path']
        file_url = f"{api_url}/file/bot{token}/{file_path}"
        print(file_url)
        #사진을 네이버 유명인인식api로 넘겨주기
        
        file = requests.get(file_url, stream=True)
        clova = requests.post("https://openapi.naver.com/v1/vision/celebrity",
                    headers ={
                        "X-Naver-Client-Id":naver_client_id,
                        "X-Naver-Client-Secret":naver_client_secret
                    },
                    files ={
                        'image':file.raw.read()
                    }
                    
        )
        
        
        #가져온 데이터 중에서 필요한 정보 빼오기
        pp(clova.json())
        #인식이 되었을때
        if clova.json().get('info').get('faceCount'):
            text = clova.json()['faces'][0]['celebrity']['value']
        else:
            text = "얼굴이 없어요 ㅠㅠㅠ"
        # if clova.json().get('info')
        #인식이 되지 않았을때
        
        
        
    
    elif text =="메뉴":
        menu_list =["한식","동식","선택식","중식","일식","양식"]
        text = random.choice(menu_list)
    elif text =="로또":
        text = random.sample(range(1,46),6)
        
    
    
    #유저에게 그대로 돌려주기
    #중괄호 안은 변수화 시켜 놓은것
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    
    
    
    return '',200
    
app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))


