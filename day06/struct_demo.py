# Day 6-①：结构化输出（模型返回 JSON + Pydantic 校验）
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 1) 用 Pydantic 定义"我想要的结构"
class ResumeInfo(BaseModel):
    name: str
    city: str
    target_role: str
    skills: list[str]

# 2) 让模型按 JSON 格式返回（response_format 是关键）
text = "我叫陈果，在成都，想做AI产品助理，会YOLOv5标注和Python"
resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是信息提取助手，只输出 JSON，不要多余文字。JSON 的键必须严格是英文：name(姓名)、city(城市)、target_role(求职意向)、skills(技能数组)。"},
        {"role": "user", "content": "从下面这句话提取信息：" + text},
    ],
    response_format={"type": "json_object"},   # ← 强制模型输出合法 JSON
)
raw = resp.choices[0].message.content
print("模型原始返回：", raw)

# 3) 解析 + 用 Pydantic 校验
data = json.loads(raw)
info = ResumeInfo.model_validate(data)
print("\n用 Pydantic 校验后：")
print("  姓名：", info.name)
print("  城市：", info.city)
print("  目标：", info.target_role)
print("  技能：", info.skills)
