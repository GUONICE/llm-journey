"""
Day 9：多轮对话上网页 —— 后端

和 Day8 比，只多了一件事：请求里除了"本轮新问题"，还带着"之前所有轮次的对话历史"。
后端把历史拼到 messages 前面，再追加本轮问题，发给模型。

为什么非要前端把历史一起发？因为 HTTP 是无状态的（Day9 第一层讲过）：
    后端每收到一个请求，函数跑完内存就回收了，它什么都不记得。
    所以"记住你"这件事，必须由前端负责 —— 前端攒着全部历史，每次重发一遍。

启动（在自己电脑的 PowerShell 里，项目根目录执行）：

    C:\\Users\\chenguo\\.workbuddy\\binaries\\python\\envs\\llmjourney\\Scripts\\python.exe -m uvicorn --app-dir day09 stream_backend:app --port 8021

然后浏览器打开：http://127.0.0.1:8021/
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

SYSTEM_PROMPT = "你是耐心的技术老师，用简短的话回答。"


# ----------------------------------------------------------------
# 模子：规定前端发来什么
#
#   ★ 和 Day8 唯一的不同：多了一个 history 字段 ★
#
#   question: 本轮新问题，至少 2 个字（照旧校验）
#   history:  之前所有轮次的对话，默认空列表 []，【不校验长度】
#
#   💡 坑点（Day9 第二层重点）：
#      如果写成 history: list[dict] = Field(min_length=1)，
#      那第一轮对话时前端发来的 history 是 []（空的），
#      FastAPI 会因为"长度不够 1"直接回 422，第一个字都问不出去。
#      所以历史字段必须允许为空 —— 用裸的默认值 [] 就行。
# ----------------------------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(min_length=2, description="本轮新问题，至少 2 个字")
    history: list[dict] = []   # 默认空列表，故意不校验，第一轮就是空的


# ----------------------------------------------------------------
# 流式接口：POST /api/chat
# ----------------------------------------------------------------
@app.post("/api/chat")
def chat(req: ChatRequest):
    def gen():
        # ① 先放系统提示
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # ② 把前端发来的历史，一条条原样拼上去
        #    history 里的每一项是 {"role": "user"/"assistant", "content": "..."}
        for turn in req.history:
            messages.append({"role": turn["role"], "content": turn["content"]})

        # ③ 再追加本轮的新问题
        messages.append({"role": "user", "content": req.question})

        # 到此，messages 跟 Day4 终端版里那个被反复 append 的列表，完全一样
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True,
        )
        for chunk in response:
            text = chunk.choices[0].delta.content or ""
            yield text

    return StreamingResponse(gen(), media_type="text/plain; charset=utf-8")


# ----------------------------------------------------------------
# 首页：把前端页面发给浏览器
# ----------------------------------------------------------------
@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "stream_frontend.html")
