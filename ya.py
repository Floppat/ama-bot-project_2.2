import aiohttp

import config


class Ai():
    def __init__(self, messages: list):
        self.messages = messages

    async def new_prompt(self, text):
        self.messages.append({"role": "user", "text": text})

    async def asis_ans(self, text):
        self.messages.append({"role": "assistant", "text": text})

    async def get_history(self):
        return self.messages
    
    async def gpt(self):
        self.prompt = {
            "modelUri": f"gpt://{config.id_ya}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.4,
                "maxTokens": "2000"
            },
            "messages": self.messages
        }
        
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {config.key_ya}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=self.prompt) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get('result', {})
                    return result.get('alternatives', [{}])[0].get('message', {}).get('text', '')
                else:
                    # Обработка ошибок
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")