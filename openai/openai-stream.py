import os
import time
import openai
from dotenv import load_dotenv

# 初始化操作
load_dotenv()  # 读取 .env 文件

# 设置您的 OpenAI API 密钥
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Example of an OpenAI ChatCompletion request with stream=True
# https://platform.openai.com/docs/guides/chat

# record the time before the request is sent
start_time = time.time()

# send a ChatCompletion request to count to 100
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': '请详细介绍一下朱元璋'}
    ],
    temperature=0,
    stream=True  # again, we set stream=True
)

# create variables to collect the stream of chunks
answer = ''
for part in response:
    finish_reason = part["choices"][0]["finish_reason"]
    if "content" in part["choices"][0]["delta"]:
        content = part["choices"][0]["delta"]["content"]
        answer += content
        content = content.replace('\n', '<br>')  # 将换行替换为<br>，用于前端显示。
        print(f"data: {content}\n\n")
    elif finish_reason:
       print(f"event: end\ndata: {answer}\n\n")
