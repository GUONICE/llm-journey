# Day 5：流式输出（打字机效果）
# 对比：普通调用（一次性返回） vs 流式调用（逐字蹦）
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# ===== 普通调用：等模型全部生成完，一次性 return =====
print("=== 普通调用（一次性返回）===")
resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "用三句话介绍成都"}],
)
print(resp.choices[0].message.content)

# ===== 流式调用：stream=True，边生成边返回 =====
print("\n=== 流式调用（逐字蹦）===")
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "用三句话介绍成都"}],
    stream=True,
)
for chunk in stream:
    # 每个 chunk 是一小段"增量"，不是完整消息
    delta = chunk.choices[0].delta
    if delta.content:                 # 开头/结尾可能为 None，要跳过
        print(delta.content, end="", flush=True)
print()  # 结束后补个换行
