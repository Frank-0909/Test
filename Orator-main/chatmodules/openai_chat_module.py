# pip install openai
import openai
from openai import OpenAI
openai_api_key = 'sk-NYsoG3VBKDiTuvdtC969F95aFc4f45379aD3854a93602327'#'sess-oevAVEQ1wAvyXzzdYMiQBD7pxIvs8OUuxqn8WppF'


class OpenaiChatModule:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.origin_model_conversation = [
                                {"role": "system", "content": "你是用户user的好朋友，能够和user进行愉快的交谈，你的名字叫Yuki."}
                            ]

    def chat_with_origin_model(self, text):
        # openai.api_key = self.openai_api_key
        text = text.replace('\n', ' ').replace('\r', '').strip()
        if len(text) == 0:
            return
        print(f'chatGPT Q:{text}')
        self.origin_model_conversation.append({"role": "user", "content": text})
        client = OpenAI(api_key=self.openai_api_key)

        response = client.chat.completions.create(
        # response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model="gpt-4",
            messages=self.origin_model_conversation,
            max_tokens=2048,
            temperature=0.3,
        )
        reply = response.choices[0].message.content
        self.origin_model_conversation.append({"role": "assistant", "content": reply})
        return reply



if __name__ == '__main__':
    openaichatmodule = OpenaiChatModule(openai_api_key)
    print(openaichatmodule.chat_with_origin_model('你好，你叫什么?'))
    print(openaichatmodule.chat_with_origin_model('天空为什么是蓝色的?'))