import requests
from tkinter import *
import tkinter
import ctypes
import tkinter.font

def failButton(window, event=None):
    print("hi")
    window.destroy()

def translate(text, source_lang, target_lang):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"

    if source_lang == "영어":
        source = "en"
    elif source_lang == "한국어":
        source = "ko"
    else:
        source = "ja"

    if target_lang == "영어":
        target = "en"
    elif target_lang == "한국어":
        target = "ko"
    else:
        target = "ja"

    try:
        # 자신이 받은 API의 ID와 Secret을 입력
        headers = {"X-Naver-Client-Id":"TRgF7onHPgDW8CVQNkIg","X-Naver-Client-Secret":"C4VZJo9hvS"}
        params = {"source" : source,"target" : target,"text" : text}
        response = requests.post(request_url,headers = headers,data = params)

        result = response.json()
        #print(result['message']['result']['translatedText'])
        return result['message']['result']['translatedText']

    except:
        window = Toplevel()
        window.title("번역 실패")
        #centerWindow(window)
        window.geometry('200x80+%d+%d'%((ctypes.windll.user32).GetSystemMetrics(0)/2-100,(ctypes.windll.user32).GetSystemMetrics(1)/2-40))
        window.resizable(0,0)
        window.focus_set()
        failLabel = tkinter.Label(window,text="번역 실패",font=tkinter.font.Font(family="맑은 고딕",size=20))
        failLabel.pack()
        failbtn = tkinter.Button(window,text="확인",command=lambda:failButton(window))
        window.bind('<Return>',lambda x :failButton(window))
        failbtn.pack()
        
        #return "번역 실패"
