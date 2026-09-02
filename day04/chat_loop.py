# 真正的多轮聊天：一直聊到你说 quit
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 聊天记录，一开始只有人设
messages = [
    {"role": "system", "content": "你是一个耐心的中文老师，回答要简短。"},
]

print("开始聊天（输入 quit 退出）")
print("-" * 40)

while True:
    # 1. 等用户输入
    user_input = input("你说：")

    # 2. 输入 quit 就退出循环
    if user_input.strip() == "quit":
        print("拜拜！")
        break

    # 3. 把用户的话加进聊天记录
    messages.append({"role": "user", "content": user_input})

    # 4. 把整段记录发给模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )
    answer = response.choices[0].message.content

    # 5. 关键！把模型的回答也加进聊天记录
    messages.append({"role": "assistant", "content": answer})

    # 6. 打印回答 + 当前记录条数
    print("AI：", answer)
    print("（当前聊天记录共", len(messages), "条）")
    print("-" * 40)
