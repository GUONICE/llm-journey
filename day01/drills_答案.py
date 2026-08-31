# -*- coding: utf-8 -*-
"""
Day 1 练习题 · 答案版
==================================================
每题都填好了，并且附上「为什么这么写」。
用法：先读懂，然后打开 drills.py（题目版）手抄一遍，不要复制粘贴。
"""

print("=" * 60)
print("Part 1 · 动手题答案（7 道）")
print("=" * 60)


# ---------------------------------------------------------------
# 【题 1】列表推导式
# ---------------------------------------------------------------
files = ["cat.jpg", "notes.txt", "dog.png", "readme.md", "car.jpg"]

jpg_files = [f for f in files if f.endswith(".jpg")]

print("\n[题1] 筛出的 jpg 文件：", jpg_files)
# 输出： ['cat.jpg', 'car.jpg']
#
# 拆解这个语法：
#   [  f          for f in files        if f.endswith(".jpg")  ]
#     ↑ 要收集什么   ↑ 从哪儿遍历          ↑ 留下满足条件
#
# 等价于下面这 4 行，但一行搞定：
#   jpg_files = []
#   for f in files:
#       if f.endswith(".jpg"):
#           jpg_files.append(f)
#
# 什么时候用：数据清洗、过滤、格式转换。做 RAG 时筛文档、过滤空切片全靠它。


# ---------------------------------------------------------------
# 【题 2】dict.get() vs 中括号
# ---------------------------------------------------------------
api_response = {"content": "你好", "model": "deepseek-chat"}

# 错误写法（去掉注释跑一次会直接崩）：
# usage = api_response["usage"]        # KeyError: 'usage'

# 正确写法：
value_b = api_response.get("usage", {"total_tokens": 0})

print("\n[题2] 用 get 取 usage：", value_b)
# 输出： {'total_tokens': 0}
#
# 区别：
#   d["usage"]              → key 不存在，程序直接崩（KeyError）
#   d.get("usage", 默认值)   → key 不存在，返回你给的默认值，程序继续跑
#
# 为什么重要：大模型 API 返回的 JSON 字段不稳定。
#   有的模型返回 usage，有的不返回；有的带 reasoning_content，有的不带。
#   你敢用中括号，线上就会在半夜崩给你看。


# ---------------------------------------------------------------
# 【题 3】zip 合并两个 list
# ---------------------------------------------------------------
keys = ["name", "city", "target"]
values = ["陈果", "成都", "大模型应用开发"]

profile = dict(zip(keys, values))

print("\n[题3] 合并结果：", profile)
# 输出： {'name': '陈果', 'city': '成都', 'target': '大模型应用开发'}
#
# 拆解：
#   zip(keys, values)  →  产生一对一对的：('name','陈果'), ('city','成都'), ...
#   dict(...)          →  把每一对变成 dict 的一个键值对
#
# zip 的字面意思就是「拉链」，把两排齿咬合在一起。
#
# 另一个高频用法 —— 同时遍历两个列表：
#   for k, v in zip(keys, values):
#       print(k, v)
#
# 什么时候用：构造 messages、把表头和数据配对、批量构造请求参数。


# ---------------------------------------------------------------
# 【题 4】enumerate 带序号遍历
# ---------------------------------------------------------------
chunks = ["第一段内容", "第二段内容", "第三段内容"]

print("\n[题4] 带序号遍历：")
for i, item in enumerate(chunks, start=1):
    print(f"第 {i} 段: {item}")

# 输出：
#   第 1 段: 第一段内容
#   第 2 段: 第二段内容
#   第 3 段: 第三段内容
#
# 拆解：
#   enumerate(chunks)        →  产生 (0, '第一段'), (1, '第二段'), ...
#   for i, item in ...       →  同时接住序号和内容（这叫「解包」）
#   start=1                  →  从 1 开始数（不加的话默认从 0 开始）
#
# 为什么写 start=1：给用户看的序号从 1 开始才符合直觉。
#   但注意：列表索引永远从 0 开始，enumerate 只是改了 i 的值，没改列表本身。
#
# 什么时候用：RAG 里给文档切片编号、打印检索结果的排名。


# ---------------------------------------------------------------
# 【题 5】f-string 格式化
# ---------------------------------------------------------------
tokens_used = 1234
cost_per_1k = 0.002
seconds = 3.14159

cost = tokens_used / 1000 * cost_per_1k
message = f"消耗 {tokens_used} tokens，花费 {cost:.4f} 元，耗时 {seconds:.2f} 秒"

print("\n[题5] 格式化输出：", message)
# 输出： 消耗 1234 tokens，花费 0.0025 元，耗时 3.14 秒
#
# 格式说明：
#   {变量}        → 直接插入变量
#   {变量:.2f}    → 浮点数保留 2 位小数
#   {变量:.4f}    → 保留 4 位小数
#   {变量:>10}    → 右对齐，占 10 个字符宽（打印表格时用）
#   {变量:<10}    → 左对齐
#
# 注意 cost 是 0.002468，用 :.4f 变成 0.0025 —— 自动四舍五入。
#
# 什么时候用：打印 token 消耗、耗时统计、日志。这几项做大模型应用天天要看。


# ---------------------------------------------------------------
# 【题 6】*args 和 **kwargs
# ---------------------------------------------------------------
def add_all(*args):
    total = sum(args)
    return total

print("\n[题6-A] add_all(1, 2, 3, 4) =", add_all(1, 2, 3, 4))
# 输出： 10
#
# *args 收到的是一个「元组」：调用 add_all(1,2,3,4) 时，args = (1, 2, 3, 4)
# 所以 sum(args) 就是 sum((1,2,3,4)) = 10


def show_config(**kwargs):
    for k, v in kwargs.items():
        print(f"{k} = {v}")

print("[题6-B] show_config 结果：")
show_config(model="deepseek-chat", temperature=0.7, max_tokens=2000)
# 输出：
#   model = deepseek-chat
#   temperature = 0.7
#   max_tokens = 2000
#
# **kwargs 收到的是一个「字典」：
#   kwargs = {"model": "deepseek-chat", "temperature": 0.7, "max_tokens": 2000}
# 所以用 .items() 遍历，跟遍历普通 dict 一模一样。
#
# 记忆口诀：
#   一个星号 *   → 元组 (1, 2, 3)              收位置参数
#   两个星号 **  → 字典 {"a": 1, "b": 2}        收关键字参数
#
# 为什么重要：这是你看懂别人源码的钥匙。
#   FastAPI 的路由、LangChain 的 Chain、Pydantic 的验证器，签名里全是这俩。
#   看不懂 *args/**kwargs，等于看源代码时一半的字不认识。


# ---------------------------------------------------------------
# 【题 9】json 写文件保留中文
# ---------------------------------------------------------------
import json
import os
import tempfile

prompt_lib = [{"名称": "简历抽取", "内容": "从简历中提取姓名和学历"}]

tmp_path = os.path.join(tempfile.gettempdir(), "day1_prompt_demo.json")

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(prompt_lib, f, ensure_ascii=False, indent=2)

print("\n[题9] 写入的文件内容：")
with open(tmp_path, "r", encoding="utf-8") as f:
    print(f.read())

# 输出（中文正常显示）：
#   [
#     {
#       "名称": "简历抽取",
#       "内容": "从简历中提取姓名和学历"
#     }
#   ]
#
# 两个参数缺一不可：
#   ensure_ascii=False  → 不加的话中文变成 \u540d\u79f0 这种转义，人没法看
#   indent=2            → 缩进 2 格，多层嵌套时能看清结构
#
# 再看 open 那行：
#   encoding="utf-8"    → Windows 上必须显式写，否则用系统默认编码，中文直接乱码
#
# 什么时候用：存 Prompt 模板、存标注结果、存配置文件、存 RAG 的切片数据。


print("\n" + "=" * 60)
print("Part 2 · 概念题（跑一遍看输出，读懂解释就行）")
print("=" * 60)


# ---------------------------------------------------------------
# 【概念题 7】可变默认参数 —— 经典面试题，也是真实 bug 来源
# ---------------------------------------------------------------
print("\n[题7] 可变默认参数的坑")

def add_item_bad(item, bag=[]):
    bag.append(item)
    return bag

def add_item_good(item, bag=None):
    if bag is None:
        bag = []
    bag.append(item)
    return bag

print("错误写法调用 3 次：")
print("  第1次:", add_item_bad("苹果"))
print("  第2次:", add_item_bad("香蕉"))
print("  第3次:", add_item_bad("橘子"))
print("  ↑ bag 越攒越多，因为默认参数只在函数定义时创建一次，")
print("    之后每次调用用的都是同一个 list 对象。")

print("正确写法调用 3 次：")
print("  第1次:", add_item_good("苹果"))
print("  第2次:", add_item_good("香蕉"))
print("  第3次:", add_item_good("橘子"))
print("  ↑ 每次都是全新的空 list，符合直觉。")
print("记住：默认参数永远不要用 [] 或 {}，用 None 然后在函数里创建。")


# ---------------------------------------------------------------
# 【概念题 8】with open 比手动 close 好在哪
# ---------------------------------------------------------------
print("\n[题8] with open 的作用")

demo_path = os.path.join(tempfile.gettempdir(), "day1_with_demo.txt")

f = open(demo_path, "w", encoding="utf-8")
f.write("第一行")
f.close()
print("写法 A：手动 close，中途报错就关不掉文件")

with open(demo_path, "w", encoding="utf-8") as f:
    f.write("第一行")
print("写法 B：with 会自动关闭，哪怕中间出错")
print("记住：以后所有 open() 都用 with，永远不要手动 close。")
print("      encoding='utf-8' 在 Windows 上必须写，否则中文乱码。")


# ---------------------------------------------------------------
# 【概念题 10】self 到底是什么
# ---------------------------------------------------------------
print("\n[题10] self 是什么")

class LLMClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, message):
        masked = self.api_key[:4] + "****"
        return f"用 {masked} 发送消息：{message}"

client_a = LLMClient("sk-abcdefghijklmn")
client_b = LLMClient("sk-xyzwxyzwxyzw")

print("  client_a:", client_a.chat("你好"))
print("  client_b:", client_b.chat("你好"))
print("  ↑ 两个对象各有各的 api_key，互不干扰。")
print("    self = 当前这个对象实例，用来区分哪个对象的哪个属性。")
print("  记住：定义方法时第一个参数必须写 self，调用时不用传，Python 自动传。")


# ---------------------------------------------------------------
# 【概念题 11】__init__ 是什么时候调用的
# ---------------------------------------------------------------
print("\n[题11] __init__ 是什么时候调用的")

class Document:
    def __init__(self, text):
        print("    → __init__ 被调用了，正在初始化对象")
        self.text = text
        self.length = len(text)

    def summary(self):
        return f"这段文档共 {self.length} 字"

print("  创建对象的瞬间：")
doc = Document("这是一段测试文本")
print("  调用普通方法：")
print("   ", doc.summary())
print("  ↑ __init__ 在 Document(...) 这一行自动执行，你不用手动调用。")
print("    普通方法要你手动 .summary() 才会执行。")


# ---------------------------------------------------------------
# 【概念题 12】super().__init__() 的作用
# ---------------------------------------------------------------
print("\n[题12] super().__init__() 的作用")

class BaseClient:
    def __init__(self, api_key):
        self.api_key = api_key
        print("    → BaseClient 的初始化执行了")

class ChatClient(BaseClient):
    def __init__(self, api_key, model):
        super().__init__(api_key)
        self.model = model
        print("    → ChatClient 自己的初始化执行了")

print("  创建子类对象：")
c = ChatClient("sk-test1234", "deepseek-chat")
print("  ", c.api_key, "|", c.model)
print("  ↑ api_key 是父类负责初始化的。不写 super().__init__()，")
print("    父类的 __init__ 不执行，self.api_key 就不存在，后面用到会报错。")
print("  规则：子类扩展父类、且父类有初始化逻辑时，子类 __init__ 第一行写 super().__init__()。")


print("\n" + "=" * 60)
print("答案版跑完了。现在打开 drills.py，照着手抄一遍，不要复制粘贴。")
print("=" * 60)
