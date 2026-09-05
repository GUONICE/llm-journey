"""
Day 8：流式输出 —— 后端

和 Day7 那个"憋着说完"的版本比，只有两处不一样：
    1. 调模型时多了一个 stream=True
    2. 不 return 结果，改成 return StreamingResponse(gen())

其余（路径、方法、Pydantic 校验）一个字都没变。

启动（在自己电脑的 PowerShell 里，项目根目录执行）：

    C:\\Users\\chenguo\\.workbuddy\\binaries\\python\\envs\\llmjourney\\Scripts\\python.exe -m uvicorn --app-dir day08 stream_backend:app --port 8020

    ⚠ 2026-09-05 起 uv 那套 Python 被 Windows 策略拦了（os error 4551），
      所以 uv run 和 .venv 里的 python 都不能用 —— 那个 .venv 是 uv 建的，
      Python 本体在 AppData\\Roaming\\uv\\ 下，同一个东西被拦。
      上面这条用的是另一套 Python（跟 uv 无关），能正常跑。

然后浏览器打开：http://127.0.0.1:8020/
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

app = FastAPI()


# ----------------------------------------------------------------
# 模子：规定前端发来什么
#   对照 Day7 的 OptimizeRequest，结构一模一样，只是字段换成了 question
#   注意这里是 class 的括号 —— BaseModel 是父类，校验能力就是继承来的
# ----------------------------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(min_length=2, description="想问模型的话，至少 2 个字")


# ----------------------------------------------------------------
# 流式接口：POST /api/chat
#
#   对照左边（Day7 普通版）看，差别就在最后两行：
#
#     普通：result = 调模型(不流式)
#           return result                    ← 一次性交出
#
#     流式：def gen():  ... yield 一块
#           return StreamingResponse(gen())  ← 交出一条传送带
# ----------------------------------------------------------------
@app.post("/api/chat")
def chat(req: ChatRequest):
    def gen():
        # stream=True 是关键：让模型一个字一个字回，而不是憋完再给
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是耐心的技术老师，用简短的话回答。"},
                {"role": "user", "content": req.question},
            ],
            stream=True,
        )
        # 模型吐一块，我立刻 yield 一块，StreamingResponse 就立刻发出去
        for chunk in response:
            text = chunk.choices[0].delta.content or ""
            yield text

    # media_type 里必须带 charset=utf-8，否则浏览器会把中文显示成乱码
    return StreamingResponse(gen(), media_type="text/plain; charset=utf-8")


# ----------------------------------------------------------------
# 首页：把前端页面发给浏览器
# ----------------------------------------------------------------
@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "stream_frontend.html")
