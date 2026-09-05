"""
最简单的前后端 Demo —— 后端（Python / FastAPI）

这个文件只干三件事：
  1. 提供两个接口（网址），等前端来调
  2. 把前端页面本身发给浏览器（GET /）
  3. 校验前端送来的数据

怎么启动（在自己电脑的 PowerShell 里，不是这里）：
    cd C:\\Users\\chenguo\\Desktop\\llm-journey
    uv run uvicorn --app-dir day07 simple_demo.backend:app --port 8010

    如果 uv 报 os error 4551（被系统策略拦了），换这条：
    .venv\\Scripts\\python.exe -m uvicorn --app-dir day07 simple_demo.backend:app --port 8010

然后浏览器打开：http://127.0.0.1:8010/

【重点】请把这个文件和同目录的 frontend.html 并排打开看，
        注意注释里标着【对齐点】的那几处 —— 那就是两边唯一的联系方式。
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()


# =================================================================
# 接口 1：GET /api/hello
#
#   【对齐点 A】路径："/api/hello"
#       这个字符串必须和 frontend.html 里 fetch("/api/hello") 一模一样
#
#   【对齐点 B】方法：GET
#       由 @app.get 决定。前端不写 method 时默认就是 GET，正好对上
#
#   两个都对齐了，请求才会落进这个函数
# =================================================================
@app.get("/api/hello")
def hello():
    return {"msg": "后端收到了你的 GET，这是 /api/hello 的回答"}


# =================================================================
# 数据形状声明：前端送来的 JSON 长什么样
#
#   【对齐点 C】字段名：name / words
#       前端 JSON.stringify({ name: ..., words: ... }) 里的 key
#       必须和下面这两个名字一字不差。
#       写成 username，后端就会回 422（收到了，但内容不合约定）
# =================================================================
class Talk(BaseModel):
    name: str
    words: str


# =================================================================
# 接口 2：POST /api/echo
#   收到 Talk 形状的数据，加工一下再送回去
# =================================================================
@app.post("/api/echo")
def echo(t: Talk):
    return {
        "我收到了谁的话": t.name,
        "话有多少个字": len(t.words),
        "后端回你一句": f"{t.name} 说：{t.words}",
    }


# =================================================================
# 接口 3：GET /  ——  把前端页面本身发给浏览器
#
#   这一步很关键：你看到的网页，是后端送过去的。
#   所以浏览器天然知道"这个页面来自 127.0.0.1:8010"，
#   页面里写相对路径 fetch("/api/hello") 时，浏览器会自动补全成
#   http://127.0.0.1:8010/api/hello
#
#   注意：必须用 Path(__file__).parent 定位文件，
#   不能写 "frontend.html" 这种相对路径 —— 相对路径是以
#   "启动命令时所在目录"为准的，很容易找不到文件
# =================================================================
@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "frontend.html")
