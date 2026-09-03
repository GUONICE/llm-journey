# Day 7：简历优化器 Web 版（FastAPI 后端）
# 把 Day6 的 resume_optimizer.py 改造成一个网页服务：
#   前端填简历 + 岗位JD → 点按钮 → 后端调 DeepSeek → 返回结构化建议
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.responses import FileResponse

load_dotenv()  # 读 .env 里的 DEEPSEEK_API_KEY
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 1) 定义"建议长什么样"（和 Day6 一样）
class ResumeAdvice(BaseModel):
    match_score: int                 # 匹配度 0-100
    strengths: list[str]             # 优势
    gaps: list[str]                  # 差距
    suggestions: list[str]           # 建议

# 2) 定义"前端会发来什么"（请求体的结构）
#    Field(min_length=10)：只传字段还不够，内容至少 10 个字
#    注意：前端 JS 也有校验，但那是"省一次请求"的体验优化；
#    这一层才是真正的安全边界 —— 别人用 curl 直接打接口也绕不过去
class OptimizeRequest(BaseModel):
    resume: str = Field(min_length=10, description="简历文本，至少 10 个字")
    jd: str = Field(min_length=10, description="岗位 JD 文本，至少 10 个字")

app = FastAPI()

# 3) 核心接口：POST /api/optimize
#    前端把简历和 JD 发过来，这里调模型，返回校验过的结构化建议
@app.post("/api/optimize", response_model=ResumeAdvice)
def optimize(req: OptimizeRequest):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是资深简历顾问。只输出 JSON，键必须严格是英文："
             "match_score(整数0-100)、strengths(优势字符串数组)、gaps(差距字符串数组)、suggestions(建议字符串数组)。"},
            {"role": "user", "content": f"简历：{req.resume}\n岗位JD：{req.jd}\n请给出匹配分析和优化建议。"},
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(resp.choices[0].message.content)
    return ResumeAdvice.model_validate(data)   # 结构不对会直接报错，前端拿到 500

# 4) 首页：返回网页
INDEX_HTML = Path(__file__).parent / "static" / "index.html"   # 基于本文件定位，不依赖运行目录

@app.get("/")
def index():
    return FileResponse(INDEX_HTML)
