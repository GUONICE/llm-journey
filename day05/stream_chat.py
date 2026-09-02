# Day 5 进阶：流式 + 多轮 = 打字机聊天机器人
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

messages = [
    {"role": "system", "content": "你是一个耐心的中文老师，回答要简短。"},
]

print("开始聊天（输入 quit 退出）")
print("-" * 40)

while True:
    user_input = input("你说：")
    if user_input.strip().lower() == "quit":
        print("拜拜！")
        break

    messages.append({"role": "user", "content": user_input})

    print("AI：", end="", flush=True)
    answer = ""                              # 边打印边累积完整回答
    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            answer += delta.content          # 拼回完整文本，留着塞记忆
    print()                                  # 本轮 AI 说完，换行

    messages.append({"role": "assistant", "content": answer})  # 记忆不能少！
    print("-" * 40)
