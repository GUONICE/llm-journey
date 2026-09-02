# 演示：messages 列表是怎么一轮一轮"长胖"的
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 一开始只有人设
messages = [
    {"role": "system", "content": "你是一个耐心的中文老师。"},
]
print("【第 0 轮】messages 里有", len(messages), "条")
for m in messages:
    print("   ", m["role"], ":", m["content"])

# 用户问第一句
messages.append({"role": "user", "content": "我叫陈果"})
print("\n【第 1 轮：你说了话】messages 里有", len(messages), "条")
for m in messages:
    print("   ", m["role"], ":", m["content"])

# 模型回答
resp = client.chat.completions.create(model="deepseek-chat", messages=messages)
answer = resp.choices[0].message.content
print("\n>>> 模型回答:", answer)

# 关键一步：把模型的回答也塞回 messages！
messages.append({"role": "assistant", "content": answer})
print("\n【第 1 轮结束：模型的话也加进去了】messages 里有", len(messages), "条")
for m in messages:
    print("   ", m["role"], ":", m["content"])

# 用户问第二句 —— 这句能"记住"上面所有内容
messages.append({"role": "user", "content": "我叫什么名字？"})
print("\n【第 2 轮：又问了一句】messages 里有", len(messages), "条")
for m in messages:
    print("   ", m["role"], ":", m["content"])

resp = client.chat.completions.create(model="deepseek-chat", messages=messages)
answer2 = resp.choices[0].message.content
print("\n>>> 模型回答:", answer2)

print("\n===== 结论 =====")
print("模型之所以记得你叫陈果，不是它有记忆，")
print("而是我们把整段聊天记录又发了一遍。")
