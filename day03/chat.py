import os
from dotenv import load_dotenv
from openai import OpenAI

# 读取同目录下的 .env 文件，把里面的 DEEPSEEK_API_KEY 变成环境变量
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ 没找到 Key！请确认 day03 目录下有 .env 文件，且内容为：")
    print("   DEEPSEEK_API_KEY=sk-你的密钥")
    exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个耐心的中文老师。"},
        {"role": "user", "content": "用成都话说一句'今天天气不错"},
    ],
)

print(response.choices[0].message.content)
