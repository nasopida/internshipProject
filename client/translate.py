import requests

class Translate:
    def __init__(self, text):
        request_url = "https://openapi.naver.com/v1/papago/n2mt"

        # 자신이 받은 API의 ID와 Secret을 입력
        headers = {"X-Naver-Client-Id":"자신의 ID","X-Naver-Client-Secret":"자신의 PW"}
        params = {"source" : "ko","target" : "en","text" : text}
        response = requests.post(request_url,headers = headers,data = params)

        result = response.json()
        print(result['message']['result']['translatedText'])