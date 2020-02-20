import requests

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
        headers = {"X-Naver-Client-Id":" A ","X-Naver-Client-Secret":" B "}
        params = {"source" : source,"target" : target,"text" : text}
        response = requests.post(request_url,headers = headers,data = params)

        result = response.json()
        #print(result['message']['result']['translatedText'])
        return result['message']['result']['translatedText']
    except:
        return "번역 실패"