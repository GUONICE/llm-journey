import llm_client

# 这就是程序入口：只负责「准备聊天内容」和「打印结果」
messages = [
    {"role": "system", "content": "你是一个耐心的中文老师。"},
    {"role": "user", "content": "用一句话解释什么是大模型"},
]

answer = llm_client.chat(messages)
print(answer)
