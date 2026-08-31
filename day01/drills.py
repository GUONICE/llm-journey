# -*- coding: utf-8 -*-
"""
Day 1 补救练习 —— 12 道自测题全部不会时的补救方案
==================================================
用法：
  1. 用编辑器打开这个文件
  2. 找到每个 【动手题】 里的 "# ← 在这里写你的代码"
  3. 自己先写，写完保存，在终端跑： python day1_drills.py
  4. 对照 "期望输出" 检查对不对
  5. 卡住超过 5 分钟，再看下面给的参考答案（不要一开始就偷看）

  概念题不用写，直接跑，看输出，读懂注释里的解释即可。

运行：  python day1_drills.py
"""

print("=" * 60)
print("Part 1 · 动手题（7 道，自己写）")
print("=" * 60)


# ---------------------------------------------------------------
# 【动手题 1】列表推导式
# 场景：从一堆文件名里筛出图片文件 —— 做数据集清洗天天干这事
# ---------------------------------------------------------------
files = ["cat.jpg", "notes.txt", "dog.png", "readme.md", "car.jpg"]

# 任务：用一行列表推导式，筛出所有 .jpg 结尾的文件
# 提示：for f in files if f.endswith(".jpg")
jpg_files = None  # ← 在这里写你的代码

print("\n[题1] 筛出的 jpg 文件：", jpg_files)
# 期望输出： ['cat.jpg', 'car.jpg']
# 参考答案： jpg_files = [f for f in files if f.endswith(".jpg")]


# ---------------------------------------------------------------
# 【动手题 2】dict.get() vs dict[]  —— 面试必考，也是真实 bug 来源
# 场景：解析大模型 API 返回的 JSON，有些字段可能不存在
# ---------------------------------------------------------------
api_response = {"content": "你好", "model": "deepseek-chat"}
# 注意：这个 dict 里没有 "usage" 字段，就像真实 API 有时不返回一样

# 任务 A：用中括号取值，看看会发生什么（先猜，再跑）
# 把下面这行的注释去掉，跑一次，看报错信息：
# value_a = api_response["usage"]

# 任务 B：用 .get() 取值，key 不存在时返回你给的默认值
value_b = None  # ← 在这里写：取 "usage"，取不到就返回 {"total_tokens": 0}

print("\n[题2] 用 get 取 usage：", value_b)
# 期望输出： {'total_tokens': 0}
# 参考答案： value_b = api_response.get("usage", {"total_tokens": 0})
# 记住：中括号取不存在的 key → 直接 KeyError 崩掉
#      .get() 取不存在的 key → 返回默认值，程序继续跑


# ---------------------------------------------------------------
# 【动手题 3】zip 把两个 list 合成 dict
# 场景：调大模型 API 时构造 messages，或者把列名和数据配对
# ---------------------------------------------------------------
keys = ["name", "city", "target"]
values = ["陈果", "成都", "大模型应用开发"]

# 任务：合并成 {"name": "陈果", "city": "成都", "target": "大模型应用开发"}
profile = None  # ← 在这里写你的代码（一行搞定，用 zip）

print("\n[题3] 合并结果：", profile)
# 期望输出： {'name': '陈果', 'city': '成都', 'target': '大模型应用开发'}
# 参考答案： profile = dict(zip(keys, values))
# 举一反三：zip 也常用来同时遍历两个列表
#           for k, v in zip(keys, values): print(k, v)


# ---------------------------------------------------------------
# 【动手题 4】enumerate 带序号遍历
# 场景：把文档切成 10 段，打印时要带 "第 3 段" 这种序号
# ---------------------------------------------------------------
chunks = ["第一段内容", "第二段内容", "第三段内容"]

# 任务：遍历 chunks，打印成 "第 1 段: 第一段内容" 这种格式
print("\n[题4] 带序号遍历：")
# ↓ 在这里写你的代码
for item in chunks:
    print(item)

# 期望输出：
#   第 1 段: 第一段内容
#   第 2 段: 第二段内容
#   第 3 段: 第三段内容
# 参考答案：
#   for i, item in enumerate(chunks, start=1):
#       print(f"第 {i} 段: {item}")
# 注意：enumerate 默认从 0 开始，加 start=1 才从 1 开始


# ---------------------------------------------------------------
# 【动手题 5】f-string 格式化
# 场景：打印 token 消耗和耗时，需要控制小数位数
# ---------------------------------------------------------------
tokens_used = 1234
cost_per_1k = 0.002
seconds = 3.14159

# 任务：用 f-string 打印成下面这个样子（cost 保留 4 位小数，seconds 保留 2 位）
# "消耗 1234 tokens，花费 0.0025 元，耗时 3.14 秒"
cost = tokens_used / 1000 * cost_per_1k
message = None  # ← 在这里写你的 f-string

print("\n[题5] 格式化输出：", message)
# 期望输出： 消耗 1234 tokens，花费 0.0025 元，耗时 3.14 秒
# 参考答案：
#   message = f"消耗 {tokens_used} tokens，花费 {cost:.4f} 元，耗时 {seconds:.2f} 秒"
# 记住：{变量:.2f} = 保留 2 位小数；{变量:>10} = 右对齐占 10 位


# ---------------------------------------------------------------
# 【动手题 6】*args 和 **kwargs
# 场景：看 LangChain / FastAPI 源码时满地都是，看不懂这个就看不懂源码
# ---------------------------------------------------------------

# 任务 A：写一个函数，能接收任意数量的位置参数，返回它们的和
def add_all(*args):
    total = None  # ← 在这里写（提示：用 sum()）
    return total

print("\n[题6-A] add_all(1, 2, 3, 4) =", add_all(1, 2, 3, 4))
# 期望输出： 10
# 参考答案： total = sum(args)

# 任务 B：写一个函数，能接收任意数量的关键字参数，把它们打印出来
def show_config(**kwargs):
    # ↓ 在这里写：遍历 kwargs，打印成 "key = value"
    pass

print("[题6-B] show_config 结果：")
show_config(model="deepseek-chat", temperature=0.7, max_tokens=2000)
# 期望输出：
#   model = deepseek-chat
#   temperature = 0.7
#   max_tokens = 2000
# 参考答案：
#   for k, v in kwargs.items():
#       print(f"{k} = {v}")
# 记住：*args 收到的是元组 (1, 2, 3)，**kwargs 收到的是字典 {"model": "..."}


# ---------------------------------------------------------------
# 【动手题 9】json 写文件时让中文正常显示
# 场景：存 Prompt 模板、存标注结果，中文变成 \u4e2d\u6587 就没法看了
# ---------------------------------------------------------------
import json
import os
import tempfile

prompt_lib = [{"名称": "简历抽取", "内容": "从简历中提取姓名和学历"}]

# 任务：把 prompt_lib 写成 JSON 文件，要求文件里的中文是正常中文，不是 \uXXXX
tmp_path = os.path.join(tempfile.gettempdir(), "day1_prompt_demo.json")

# ↓ 在这里写（提示：open 加 encoding，json.dump 加 ensure_ascii 参数）
with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(prompt_lib, f)  # ← 改这一行，加参数

print("\n[题9] 写入的文件内容：")
with open(tmp_path, "r", encoding="utf-8") as f:
    print(f.read())
# 期望输出： [{"名称": "简历抽取", "内容": "从简历中提取姓名和学历"}]
# 参考答案： json.dump(prompt_lib, f, ensure_ascii=False, indent=2)
# 记住：ensure_ascii=False → 中文正常显示；indent=2 → 格式化缩进，人能看懂
# 坑：如果看到 \u7b80\u5386 这种，就是忘了加 ensure_ascii=False


print("\n" + "=" * 60)
print("Part 2 · 概念题（5 道，跑一遍看输出，读懂解释就行）")
print("=" * 60)


# ---------------------------------------------------------------
# 【概念题 7】可变默认参数 —— 经典面试题，也是真实 bug 来源
# ---------------------------------------------------------------
print("\n[题7] 可变默认参数的坑")

def add_item_bad(item, bag=[]):        # 错误写法：默认参数是可变的 list
    bag.append(item)
    return bag

def add_item_good(item, bag=None):     # 正确写法
    if bag is None:
        bag = []
    bag.append(item)
    return bag

print("错误写法调用 3 次：")
print("  第1次:", add_item_bad("苹果"))
print("  第2次:", add_item_bad("香蕉"))
print("  第3次:", add_item_bad("橘子"))
print("  ↑ 看到了吗？bag 没有清空，越攒越多。因为默认参数只在函数定义时创建一次，")
print("    之后每次调用都用的是同一个 list 对象。")

print("正确写法调用 3 次：")
print("  第1次:", add_item_good("苹果"))
print("  第2次:", add_item_good("香蕉"))
print("  第3次:", add_item_good("橘子"))
print("  ↑ 每次都是全新的空 list，符合直觉。")
print("记住：函数的默认参数永远不要用 [] 或 {}，用 None 然后在函数里创建。")


# ---------------------------------------------------------------
# 【概念题 8】with open 比 f = open() 好在哪
# ---------------------------------------------------------------
print("\n[题8] with open 的作用")

demo_path = os.path.join(tempfile.gettempdir(), "day1_with_demo.txt")

# 写法 A：手动开关（不好）
f = open(demo_path, "w", encoding="utf-8")
f.write("第一行")
# 如果这里代码报错了，f.close() 就执行不到 → 文件句柄泄漏
f.close()
print("写法 A：手动 close，中途报错就关不掉文件")

# 写法 B：with 上下文管理器（推荐）
with open(demo_path, "w", encoding="utf-8") as f:
    f.write("第一行")
    # 就算这里报错，Python 也会保证文件被正确关闭
print("写法 B：with 会自动关闭，哪怕中间出错")
print("记住：以后所有 open() 都用 with，永远不要手动 close。")
print("      encoding='utf-8' 在 Windows 上必须写，否则中文乱码。")


# ---------------------------------------------------------------
# 【概念题 10】self 到底是什么
# ---------------------------------------------------------------
print("\n[题10] self 是什么")

class LLMClient:
    def __init__(self, api_key):
        # self 就是"这个对象自己"
        # 下面这行的意思是：给"这个对象"绑定一个 api_key 属性
        self.api_key = api_key

    def chat(self, message):
        # 在方法里可以通过 self 拿到 __init__ 里存的属性
        masked = self.api_key[:4] + "****"
        return f"用 {masked} 发送消息：{message}"

client_a = LLMClient("sk-abcdefghijklmn")
client_b = LLMClient("sk-xyzwxyzwxyzw")

print("  client_a:", client_a.chat("你好"))
print("  client_b:", client_b.chat("你好"))
print("  ↑ 两个对象各有各的 api_key，互不干扰。这就是 self 的作用：")
print("    self = 当前这个对象实例，用来区分'哪个对象的哪个属性'。")
print("  记住：定义方法时第一个参数必须写 self（名字可以改但没人改），")
print("        调用时不用传，Python 自动把对象传进去。")


# ---------------------------------------------------------------
# 【概念题 11】__init__ 和普通实例方法的区别
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
print("  ↑ __init__ 在 'Document(...)' 这一行自动执行，你不用手动调用。")
print('    它的作用就是给新对象做初始化，比如存属性、建立连接。')
print("    普通方法要你手动 .summary() 才会执行。")


# ---------------------------------------------------------------
# 【概念题 12】什么时候必须写 super().__init__()
# ---------------------------------------------------------------
print("\n[题12] super().__init__() 的作用")

class BaseClient:
    def __init__(self, api_key):
        self.api_key = api_key
        print("    → BaseClient 的初始化执行了")

class ChatClient(BaseClient):
    def __init__(self, api_key, model):
        super().__init__(api_key)   # 调用父类的 __init__
        self.model = model          # 再初始化自己独有的属性
        print("    → ChatClient 自己的初始化执行了")

print("  创建子类对象：")
c = ChatClient("sk-test1234", "deepseek-chat")
print("  ", c.api_key, "|", c.model)
print("  ↑ 注意：api_key 是父类负责初始化的。如果不写 super().__init__()，")
print("    父类的 __init__ 就不会执行，self.api_key 就不存在，后面用到会报错。")
print("  规则：子类要扩展父类、且父类有初始化逻辑时，子类 __init__ 第一行写 super().__init__()。")


print("\n" + "=" * 60)
print("全部跑完了。回去把 7 道动手题的空白处补上，再跑一次对照期望输出。")
print("=" * 60)
