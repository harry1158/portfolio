import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def add_note(front, back, deck_name, tag):
    note = {
        "deckName": deck_name,  # デッキ名
        "modelName": "基本",  # 使用するノートモデル (例: "Basic")
        "fields": {
            "表面": front,  # フロントフィールド
            "裏面": back  # バックフィールド
        },
        "tags": [tag],  # タグを追加
        "options": {
            "allowDuplicate": True
        }
    }
    invoke('addNote', note=note)


    
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import requests
import os

section = {
    "front" : {
        "q":"",
        "img":"",
    },
    "choices":{
        "all_img":"",
        "a":"",
        "a img":"",
        "b" :"",
        "b img":"",
        "c" :"",
        "c img":"",
        "d" :"",
        "d img":"",
        },
    "back" : {
        "ans":"",
        "url":""
    }
}

def main(year,season,q_num):

    def img_dl(path):
        Fname = ""
        img_element = page.query_selector(path)
        
        if img_element:
            img_src = page.get_attribute(path, 'src')
            absolute_img_src = urljoin(page.url, img_src)
            response = requests.get(absolute_img_src)
            if response.status_code == 200:
                # ファイル名を生成して保存
                file_name = os.path.join(r"C:\Users\User\AppData\Roaming\Anki2\ユーザー 1\collection.media", f'{year}_{season}_{os.path.basename(absolute_img_src)}')
                Fname = f'{year}_{season}_{os.path.basename(absolute_img_src)}'
                Fname = f'<img src="{Fname}">'
                with open(file_name, 'wb') as f:
                    f.write(response.content)
        return Fname
        
    def mondai(path):
        mondai_ele = page.query_selector(path)
        if mondai_ele :
            return page.text_content(path)
        else:
            return ""
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Chromiumブラウザを起動
        page = browser.new_page()  # 新しいページを作成
        page.goto(f'https://www.fe-siken.com/kakomon/{year}_{season}/q{q_num}.html')  # ページに移動
        page.wait_for_selector('#mondai')#問題文
        section["front"]["q"] = mondai('#mondai')
        section["front"]["img"]=img_dl("#mondai .img_margin img")#問題文 写真
        #選択
        section["choices"]["all_img"] = img_dl("div.ansbg ul.selectList li img")
        section["choices"]["a"] = mondai('#select_a') #ア
        section["choices"]["a img"] = img_dl("#select_a img")
        section["choices"]["b"] = mondai('#select_i') #イ
        section["choices"]["b img"] = img_dl("#select_i img")
        section["choices"]["c"] = mondai('#select_u') #ウ
        section["choices"]["c img"] = img_dl("#select_u img")
        section["choices"]["d"] = mondai('#select_e') #エ
        section["choices"]["d img"] = img_dl("#select_e img")
        if section["choices"]["a img"] == section["choices"]["all_img"]:
            section["choices"]["all_img"] = ""
        #回答
        page.click("#showAnswerBtn")
        section["back"]["ans"] = mondai("#answerChar")
        section["back"]["url"] = page.url


s = "haru" 

for y in range(15,19):   
    print(f'year: {y}')
    invoke('createDeck', deck=f'FE{y}-haru')  
    for i in range(0,80): 
        a = i+1       
        main(y,s,a)
        add_note(f'{section["front"]["q"]}<br>\
                {section["front"]["img"]}<br><br><br>\
                {section["choices"]["all_img"]}<br>\
                ア {section["choices"]["a"]}<br>\
                {section["choices"]["a img"]}<br><br>\
                イ {section["choices"]["b"]}<br>\
                {section["choices"]["b img"]}<br><br>\
                ウ {section["choices"]["c"]}<br>\
                {section["choices"]["c img"]}<br><br>\
                エ {section["choices"]["d"]}<br>\
                {section["choices"]["d img"]}<br><br>\
                ',f'{section["back"]["ans"]}<br>\
                    {section["back"]["url"]}',f'FE{y}-haru',"")
        print(a)
  
s = "aki" 
for y in range(15,19):   
    print(f'year: {y}aki')
    invoke('createDeck', deck=f'FE{y}-aki')  
    for i in range(0,80): 
        a = i+1       
        main(y,s,a)
        add_note(f'{section["front"]["q"]}<br>\
                {section["front"]["img"]}<br><br><br>\
                {section["choices"]["all_img"]}<br>\
                ア {section["choices"]["a"]}<br>\
                {section["choices"]["a img"]}<br><br>\
                イ {section["choices"]["b"]}<br>\
                {section["choices"]["b img"]}<br><br>\
                ウ {section["choices"]["c"]}<br>\
                {section["choices"]["c img"]}<br><br>\
                エ {section["choices"]["d"]}<br>\
                {section["choices"]["d img"]}<br><br>\
                ',f'{section["back"]["ans"]}<br>\
                    {section["back"]["url"]}',f'FE{y}-aki',"")
        print(a)
        
# invoke('createDeck', deck=f'FE01-aki')  
for i in range(0,80): 
    a = i+1       
    main("01","aki",a)
    # add_note(f'{section["front"]["q"]}<br>\
    #         {section["front"]["img"]}<br><br><br>\
    #         {section["choices"]["all_img"]}<br>\
    #         ア {section["choices"]["a"]}<br>\
    #         {section["choices"]["a img"]}<br><br>\
    #         イ {section["choices"]["b"]}<br>\
    #         {section["choices"]["b img"]}<br><br>\
    #         ウ {section["choices"]["c"]}<br>\
    #         {section["choices"]["c img"]}<br><br>\
    #         エ {section["choices"]["d"]}<br>\
    #         {section["choices"]["d img"]}<br><br>\
    #         ',f'{section["back"]["ans"]}<br>\
    #                 {section["back"]["url"]}',f'FE01-aki',"")
    print(a)
                  
#10:30 start
#10:35 end

#22:58