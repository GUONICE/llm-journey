# 把 response 一层层拆开，看清答案到底藏在哪
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "用四个字形容秋天"},
    ],
)

print("=" * 50)
print("第 0 层：response 本身")
print("类型：", type(response).__name__)
print("=" * 50)

# 把 response 转成普通字典，方便看清结构
data = response.model_dump()

print("\n第 1 层：response 里面有哪些字段？")
print(list(data.keys()))
print("→ 关键字段是 choices（还有 id、usage 等，先不管）")

print("\n" + "=" * 50)
print("第 2 层：choices 是什么？")
choices = data["choices"]
print("类型：", type(choices).__name__)
print("长度：", len(choices))
print("→ 是个列表！默认只让模型给 1 个答案，所以长度是 1")
print("→ 列表取第一个要写 [0]，所以是 choices[0]")

print("\n" + "=" * 50)
print("第 3 层：choices[0] 里面有什么？")
print(json.dumps(choices[0], ensure_ascii=False, indent=2))
print("→ 里面有 message、finish_reason、index")

print("\n" + "=" * 50)
print("第 4 层：choices[0]['message'] 是什么？")
print(choices[0]["message"])
print("→ 是个字典，有 role 和 content")
print("→ role=assistant 表示这是模型说的内容")

print("\n" + "=" * 50)
print("第 5 层：最终答案 content")
print(repr(choices[0]["message"]["content"]))
print("→ 这才是我们想要的文字！")

print("\n" + "=" * 50)
print("对比：直接一层层取，效果完全一样")
print("response.choices       ->", type(response.choices).__name__)
print("response.choices[0]    ->", type(response.choices[0]).__name__)
print("response.choices[0].message ->", type(response.choices[0].message).__name__)
print("response.choices[0].message.content ->", response.choices[0].message.content)
