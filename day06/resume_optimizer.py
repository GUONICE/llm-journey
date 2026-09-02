# Day 6-②：简历优化器雏形（基于 ① 的结构化输出）
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

# 1) 用 Pydantic 定义"我想要的建议结构"
class ResumeAdvice(BaseModel):
    match_score: int                 # 与目标岗位匹配度 0-100
    strengths: list[str]             # 优势点
    gaps: list[str]                  # 差距/硬伤
    suggestions: list[str]           # 具体优化建议

# 2) 你的简历 + 目标岗位 JD（以后可以换成你真实的内容）
resume = """
陈果，24岁，AI专业本科毕业。做过 YOLOv5 图像标注项目（bounding box、类别标注、标注流程实操）。
实习经历：深信服渠道售后、教学助理。沟通表达能力强。
求职意向：成都 AI产品助理。
"""
jd = "招聘 AI产品助理：熟悉大模型应用、能写 Python、有数据标注经验优先、具备良好沟通能力。"

# 3) 调模型，要求按 JSON 返回
resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是资深简历顾问。只输出 JSON，键必须严格是英文："
         "match_score(整数0-100)、strengths(优势字符串数组)、gaps(差距字符串数组)、suggestions(建议字符串数组)。"},
        {"role": "user", "content": f"简历：{resume}\n岗位JD：{jd}\n请给出匹配分析和优化建议。"},
    ],
    response_format={"type": "json_object"},
)
data = json.loads(resp.choices[0].message.content)
advice = ResumeAdvice.model_validate(data)

# 4) 输出（这就是一个能用的小工具）
print("匹配度：", advice.match_score, "/ 100")
print("\n优势：")
for s in advice.strengths:
    print("  +", s)
print("\n差距：")
for g in advice.gaps:
    print("  -", g)
print("\n建议：")
for s in advice.suggestions:
    print("  *", s)
