# 演示：对象为什么能"点点点"
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 第 1 部分：你自己也能造一个"有内容"的对象 =====
class 包裹:
    def __init__(self):
        # self.内容 / self.重量 就是对象里面预先装好的"字段"
        self.内容 = "一封信"
        self.重量 = "500克"

p = 包裹()          # p 是接住的"对象"
print("p.内容 =", p.内容)     # 用 . 取里面的字段
print("p.重量 =", p.重量)
print("→ 你看，自己造的对象也能【点点点】取东西")
print("  这些字段是 __init__ 里 self.xxx = ... 装进去的")
print()

# ===== 第 2 部分：对比简单变量 vs 复杂对象 =====
姓名 = "陈果"          # 简单变量，没有 .xxx
print("姓名 =", 姓名)
# print(姓名.内容)     # 会报错：字符串没有"内容"这个字段

print()
print("===== 回到 response =====")

# ===== 第 3 部分：response 是【库造的对象】，不是你捏的 =====
load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "hi"}],
)

print("response 的类型：", type(response).__name__)
print("→ 它是 OpenAI 库的 ChatCompletion 对象")
print("→ 里面装了哪些字段，是库作者写好的，你用 . 一层层取")
print("→ choices 是其中一个字段，它的值是个列表，所以能 [0]")
print("→ choices[0] 又是个对象，里面有 message 字段")
print("→ message 里的 content 字段，才是最终文字")
