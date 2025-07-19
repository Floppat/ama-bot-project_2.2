import requests
import config

class Ai():
    def __init__(self, messages: list):
        print('init')
        self.messages = messages # type: ignore

    def new_prompt(self, text):
        print('new prompt')
        self.messages.append({"role": "user", "text": text}) # type: ignore

    def asis_ans(self, text):
        print('asis ans')
        self.messages.append({"role": "assistant", "text": text}) # type: ignore

    def get_history(self):
        return self.messages # type: ignore
    
    def gpt(self):
        print('gpt')
        self.prompt = {
            "modelUri": f"gpt://{config.id_ya}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.4,
                "maxTokens": "2000"
            },
            "messages": self.messages # type: ignore
        }
        
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {config.key_ya}"
        }
        
        response = requests.post(url, headers=headers, json=self.prompt)
        result = (response.json()).get('result')
        return result['alternatives'][0]['message']['text']