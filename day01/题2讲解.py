# -*- coding: utf-8 -*-
"""
题 2 专项讲解：dict.get() 到底在解决什么问题
双击「运行练习.bat」，输入 3 即可运行本文件
"""

print("=" * 60)
print("第 0 步：先确认 dict 是什么")
print("=" * 60)

# dict（字典）就是一个「名字 → 内容」的对照表
person = {"name": "陈果", "city": "成都", "age": 24}

print("整个字典：", person)
print("取 name：", person["name"])   # 中括号里写名字，拿到内容
print("取 city：", person["city"])
print()
print("规律：字典[名字] → 内容")
print()

print("=" * 60)
print("第 1 步：中括号取值的致命问题")
print("=" * 60)

# 这个 dict 是「大模型 API 返回的结果」
# 注意：它只有 content 和 model，没有 usage
api_response = {"content": "你好，有什么可以帮你？", "model": "deepseek-chat"}

print("API 返回的内容：")
print(api_response)
print()
print("现在我要统计花了多少 token，去取 usage 字段：")
print("  代码：api_response['usage']")
print()

# 用 try/except 接住崩溃，这样脚本不会中断，能继续往下演示
try:
    usage = api_response["usage"]
    print("取到了：", usage)
except KeyError as e:
    print(">>> 程序崩溃了！")
    print(">>> 报错信息：KeyError:", e)
    print(">>> 翻译成人话：这个字典里根本没有 usage 这个 key，程序当场死掉")
    print(">>> 后面所有的代码都不会执行了")

print()
print("=" * 60)
print("第 2 步：换成 .get() 会怎样")
print("=" * 60)

print("  代码：api_response.get('usage', {'total_tokens': 0})")
print()

usage_safe = api_response.get("usage", {"total_tokens": 0})
print("取到了：", usage_safe)
print(">>> 没有崩溃！返回的是我提前准备的备胎值")
print(">>> 程序继续往下跑，后面的代码全部正常执行")

print()
print("=" * 60)
print("第 3 步：.get() 的语法拆解")
print("=" * 60)

print("""
    api_response.get( "usage" , {"total_tokens": 0} )
                       ↑              ↑
                       |              └── 第二个参数：备胎。找不到就返回它
                       └───────────────── 第一个参数：你要找的 key

    一句话记：get(要找什么, 找不到的话用什么代替)
""")

# 对比一下：key 存在的时候，get 和中括号没区别
print("验证：key 存在时，两种写法结果一样")
print("  中括号取 content：", api_response["content"])
print("  get 取 content   ：", api_response.get("content", "没找到"))
print()
print(">>> 结论：key 存在时两者完全一样；区别只在 key 不存在的时候")

print()
print("=" * 60)
print("第 4 步：为什么这个知识点对大模型开发是刚需")
print("=" * 60)

print("""
真实情况：不同厂商、不同模式下，API 返回的字段是不一样的。

场景 A：DeepSeek 非流式调用，返回带 usage
    {"content": "你好", "usage": {"total_tokens": 37}}

场景 B：DeepSeek 流式调用（打字机效果），返回不带 usage
    {"content": "你好"}

场景 C：某些模型返回 reasoning_content（思考过程），某些没有
    {"content": "答案", "reasoning_content": "让我想想..."}
    {"content": "答案"}

如果你的代码写死成 resp["usage"]["total_tokens"]，
那么一开流式，程序立刻崩。而流式（打字机效果）几乎是必做的。
""")

# 模拟三种真实返回
responses = [
    ("场景A 非流式", {"content": "你好", "usage": {"total_tokens": 37}}),
    ("场景B 流式", {"content": "你好"}),
    ("场景C 思考模型", {"content": "答案", "reasoning_content": "让我想想"}),
]

print("对比测试：同一行代码，面对三种返回")
print("-" * 60)

for name, resp in responses:
    # 危险写法
    try:
        dangerous = resp["usage"]["total_tokens"]
        dangerous_result = str(dangerous)
    except KeyError:
        dangerous_result = "崩溃！KeyError"

    # 安全写法
    safe = resp.get("usage", {}).get("total_tokens", 0)
    safe_result = str(safe)

    print(f"{name}")
    print(f"    中括号写法 → {dangerous_result}")
    print(f"    get 写法   → {safe_result}")

print("-" * 60)
print(">>> 中括号：3 个场景崩 2 个")
print(">>> get：3 个场景全部正常")

print()
print("=" * 60)
print("第 5 步：连续取两层怎么写（实战最常用）")
print("=" * 60)

print("""
想取 resp["usage"]["total_tokens"]，但两层都可能不存在。

写法：resp.get("usage", {}).get("total_tokens", 0)
                        ↑↑
                        第一层找不到，先给个空字典 {} 顶上
                        这样第二层的 .get 才能继续调用，不会报错

这是链式保险：每一层都准备一个备胎。
""")

resp1 = {"content": "你好", "usage": {"total_tokens": 37}}
resp2 = {"content": "你好"}

print("对 resp1（有 usage）取 token：",
      resp1.get("usage", {}).get("total_tokens", 0))
print("对 resp2（无 usage）取 token：",
      resp2.get("usage", {}).get("total_tokens", 0))
print()
print(">>> 两个都正常返回，没有崩溃")

print()
print("=" * 60)
print("记忆口诀")
print("=" * 60)
print("""
    自己的数据，确定有 → 用中括号，写起来短
    别人的数据，不确定 → 用 get，给个备胎

    API 返回、配置文件、用户输入，全部属于「别人的数据」。
    在大模型开发里，你打交道的数据 90% 是别人给的。
    所以默认就用 get，养成习惯。
""")
