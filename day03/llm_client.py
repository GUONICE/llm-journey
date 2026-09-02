from openai import OpenAI
import config

# 只造一个"客户端"，全程序共用（避免每次调用都新建）
client = OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url=config.DEEPSEEK_BASE_URL,
)


def chat(messages):
    """把「聊天记录列表」发出去，返回 AI 的文字回答。"""
    response = client.chat.completions.create(
        model=config.DEEPSEEK_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content
