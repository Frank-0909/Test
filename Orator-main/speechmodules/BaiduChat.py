import numpy
import requests
import json

# 设置API相关参数
API_URL = 'https://keyue.cloud.baidu.com/online/core/v5/stream/query'  # 替换为实际的API URL
API_KEY = '64670d1a-32dc-480b-938b-9b433ba7b491'  # 替换为你的API密钥


class BaiduLLM:
    def chat_with_baidu_llm(self, input_text: str='你叫什么名字？'):
        # 准备请求头部
        headers = {
            'Content-Type': 'application/json',
            'token': API_KEY,  # 使用Token进行身份验证
        }

        # 准备请求体
        data = {
            'queryText': input_text,  # 用户输入的文本
            "sessionId": API_KEY
            # 其他可能的参数，如模型选择、温度等，根据API文档添加
        }

        # 发送POST请求到API
        response = requests.post(API_URL, headers=headers, json=data)
        # response.encoding = 'utf-8'
        # print(requests)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            # result = response.json()
            # return result['response']  # 假设响应中包含'response'字段作为模型输出

            data = response.content.decode('utf-8')
            print(data)
            print('------')
            index = data.rindex('last_response')
            data = data[index:]
            print(data)
            print('------')
            data = data.split(',',1)
            print(data)
            print('------')
            data = data[0].split(':',1)

            # index = data.index('last_response')
            # data = data[index:]
            print(data)

            return data[1]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        # 示例对话

if __name__ == '__main__':
    user_input = "你好，你叫什么？"
    llmmodel = BaiduLLM()
    model_response = llmmodel.chat_with_baidu_llm(user_input)
    print(model_response)

# data: {
#     "sessionId": "64670d1a-32dc-480b-938b-9b433ba7b491",
#     "queryId": "7fb2e160-cf68-4f79-aa7f-a0e23546dd77",
#     "replyStatus": 200,
#     "answer": [
#         {
#             "chunkId": 0,
#             "status": "running",
#             "topicId": "",
#             "blockId": "",
#             "nodeId": "",
#             "reply": {
#                 "type": 1,
#                 "text": "你好，",
#                 "textList": null,
#                 "clarifyGuide": null,
#                 "replySource": "CHITCHAT",
#                 "showDocumentSource": null,
#                 "documents": null,
#                 "docDebug": null,
#                 "faqSearch": null,
#                 "slotCollectInfo": null
#             }
#         }
#     ],
#     "variables": {
#         "LLM_rewrite_query": "你好，你叫什么？",
#         "last_response": "你好，",
#         "last_user_response": "你好，你叫什么？"
#     },
#     "endTime": null,
#     "recommendList": [
#
#     ],
#     "rewriteQuery": "你好，你叫什么？",
#     "intent": null
# }
# data: {
#     "sessionId": "64670d1a-32dc-480b-938b-9b433ba7b491",
#     "queryId": "7fb2e160-cf68-4f79-aa7f-a0e23546dd77",
#     "replyStatus": 200,
#     "answer": [
#         {
#             "chunkId": 0,
#             "status": "running",
#             "topicId": "",
#             "blockId": "",
#             "nodeId": "",
#             "reply": {
#                 "type": 1,
#                 "text": "我是百度研发的客服机器人，你可以叫我小度。",
#                 "textList": null,
#                 "clarifyGuide": null,
#                 "replySource": "CHITCHAT",
#                 "showDocumentSource": null,
#                 "documents": null,
#                 "docDebug": null,
#                 "faqSearch": null,
#                 "slotCollectInfo": null
#             }
#         }
#     ],
#     "variables": {
#         "LLM_rewrite_query": "你好，你叫什么？",
#         "last_response": "我是百度研发的客服机器人，你可以叫我小度。",
#         "last_user_response": "你好，你叫什么？"
#     },
#     "endTime": null,
#     "recommendList": [
#
#     ],
#     "rewriteQuery": "你好，你叫什么？",
#     "intent": null
# }
# data: {
#     "sessionId": "64670d1a-32dc-480b-938b-9b433ba7b491",
#     "queryId": "7fb2e160-cf68-4f79-aa7f-a0e23546dd77",
#     "replyStatus": 200,
#     "answer": [
#         {
#             "chunkId": 0,
#             "status": "done",
#             "topicId": "",
#             "blockId": "",
#             "nodeId": "",
#             "reply": {
#                 "type": 1,
#                 "text": "",
#                 "textList": null,
#                 "clarifyGuide": null,
#                 "replySource": "CHITCHAT",
#                 "showDocumentSource": null,
#                 "documents": null,
#                 "docDebug": null,
#                 "faqSearch": null,
#                 "slotCollectInfo": null
#             }
#         }
#     ],
#     "variables": {
#         "LLM_rewrite_query": "你好，你叫什么？",
#         "last_response": "你好，我是百度研发的客服机器人，你可以叫我小度。",
#         "last_user_response": "你好，你叫什么？"
#     },
#     "endTime": null,
#     "recommendList": [
#
#     ],
#     "rewriteQuery": "你好，你叫什么？",
#     "intent": null
# }


























# data: {
#     "sessionId": "64670d1a-32dc-480b-938b-9b433ba7b491",
#     "queryId": "f7e5bb28-ba4c-4b3a-9e12-642a1c8d7b27",
#     "replyStatus": 200,
#     "answer": [
#         {
#             "chunkId": 0,
#             "status": "running",
#             "topicId": "",
#             "blockId": "",
#             "nodeId": "",
#             "reply": {
#                 "type": 1,
#                 "text": "你好，",
#                 "textList": null,
#                 "clarifyGuide": null,
#                 "replySource": "CHITCHAT",
#                 "showDocumentSource": null,
#                 "documents": null,
#                 "docDebug": null,
#                 "faqSearch": null,
#                 "slotCollectInfo": null
#             }
#         }
#     ],
#     "variables": {
#         "LLM_rewrite_query": "你好，今天天气怎么样？",
#         "last_response": "你好，",
#         "last_user_response": "你好，今天天气怎么样？"
#     },
#     "endTime": null,
#     "recommendList": [
#
#     ],
#     "rewriteQuery": "你好，今天天气怎么样？",
#     "intent": null
# }
# data: {
#     "sessionId": "64670d1a-32dc-480b-938b-9b433ba7b491",
#     "queryId": "f7e5bb28-ba4c-4b3a-9e12-642a1c8d7b27",
#     "replyStatus": 200,
#     "answer": [
#         {
#             "chunkId": 0,
#             "status": "running",
#             "topicId": "",
#             "blockId": "",
#             "nodeId": "",
#             "reply": {
#                 "type": 1,
#                 "text": "今天天气挺好的，阳光明媚，温度适宜，很适合外出走走，享受一下大自然的美好。",
#                 "textList": null,
#                 "clarifyGuide": null,
#                 "replySource": "CHITCHAT",
#                 "showDocumentSource": null,
#                 "documents": null,
#                 "docDebug": null,
#                 "faqSearch": null,
#                 "slotCollectInfo": null
#             }
#         }
#     ],
#     "variables": {
#         "LLM_rewrite_query": "你好，今天天气怎么样？",
#         "last_response": "今天天气挺好的，阳光明媚，温度适宜，很适合外出走走，享受一下大自然的美好。",
#         "last_user_response": "你好，今天天气怎么样？"
#     },
#     "endTime": null,
#     "recommendList": [
#
#     ],
#     "rewriteQuery": "你好，今天天气怎么样？",
#     "intent": null
# }
# data: {
#     "sessionId": "64670d1a-32dc-480b-938b-9b433ba7b491",
#     "queryId": "f7e5bb28-ba4c-4b3a-9e12-642a1c8d7b27",
#     "replyStatus": 200,
#     "answer": [
#         {
#             "chunkId": 0,
#             "status": "done",
#             "topicId": "",
#             "blockId": "",
#             "nodeId": "",
#             "reply": {
#                 "type": 1,
#                 "text": "",
#                 "textList": null,
#                 "clarifyGuide": null,
#                 "replySource": "CHITCHAT",
#                 "showDocumentSource": null,
#                 "documents": null,
#                 "docDebug": null,
#                 "faqSearch": null,
#                 "slotCollectInfo": null
#             }
#         }
#     ],
#     "variables": {
#         "LLM_rewrite_query": "你好，今天天气怎么样？",
#         "last_response": "你好，今天天气挺好的，阳光明媚，温度适宜，很适合外出走走，享受一下大自然的美好。",
#         "last_user_response": "你好，今天天气怎么样？"
#     },
#     "endTime": null,
#     "recommendList": [
#
#     ],
#     "rewriteQuery": "你好，今天天气怎么样？",
#     "intent": null
# }