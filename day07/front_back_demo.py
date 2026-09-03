"""Day 7 补课：前端 / 后端 / FastAPI 最小演示

一个文件同时演示三件事：
  1. GET  请求：向服务器"要"东西，参数写在网址里
  2. POST 请求：给服务器"送"东西，数据放在请求体（JSON）里
  3. 返回网页：后端直接把 HTML 发给浏览器，这就是"前端"

启动：
  uv run uvicorn day07.front_back_demo:app --port 8003
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()


# ---------------------------------------------------------------
# 1) GET：向服务器"要"东西
#    访问 http://127.0.0.1:8003/hi?name=陈果 就会执行这个函数
#    name 后面的 "陈果" 是默认值，网址里不写就用它
# ---------------------------------------------------------------
@app.get("/hi")
def hi(name: str = "陈果"):
    return {"msg": f"你好 {name}！这是 GET，参数写在网址里"}


# ---------------------------------------------------------------
# 2) POST：给服务器"送"东西
#    这次数据不是写在网址里，而是放在"请求体"里（一包 JSON）
#    用 Pydantic 声明"我会收到什么"，FastAPI 自动帮你解析+校验
# ---------------------------------------------------------------
class Msg(BaseModel):
    name: str   # 前端会发来 name
    text: str   # 前端会发来 text


@app.post("/echo")
def echo(m: Msg):
    return {
        "我收到了谁的名字": m.name,
        "这段文字有多少字": len(m.text),
        "回复": f"收到 {m.name} 发来的 {len(m.text)} 个字",
    }


# ---------------------------------------------------------------
# 2-b) 严格版：空字符串也要拒
#      Field(min_length=1) = 这个字符串最少 1 个字
#      不加这行时，"" 也是合法 str（长度 0），Pydantic 不拦
# ---------------------------------------------------------------
class StrictMsg(BaseModel):
    name: str = Field(min_length=1)
    text: str = Field(min_length=1)


@app.post("/echo_strict")
def echo_strict(m: StrictMsg):
    return {"回复": f"收到 {m.name} 发来的 {len(m.text)} 个字"}


# ---------------------------------------------------------------
# 3) 返回一个网页：这就是"前端"
#    浏览器打开 http://127.0.0.1:8003/ 看到的就是这个 HTML
#    页面里的 JS 用 fetch 去调上面那个 /echo 接口
# ---------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>前后端演示</title></head>
<body style="font-family:sans-serif;max-width:640px;margin:40px auto;">
  <h2>前端页面（你看到的这个网页）</h2>

  <p>名字：<input id="name" value="陈果" style="width:120px"></p>
  <p>内容：<input id="text" value="我在学 FastAPI" style="width:300px"></p>
  <button onclick="send('/echo')" style="padding:6px 16px;">发给宽松版 /echo</button>
  <button onclick="send('/echo_strict')" style="padding:6px 16px;">发给严格版 /echo_strict</button>

  <h3>后端返回的结果：</h3>
  <pre id="out" style="background:#f4f4f4;padding:12px;">（还没发过请求）</pre>

  <script>
  async function send(url) {
    const name = document.getElementById("name").value;
    const text = document.getElementById("text").value;

    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name, text: text })
    });

    const data = await resp.json();
    const out = document.getElementById("out");

    // resp.ok 为 false 说明被后端拒绝（比如 422 校验不通过）
    if (resp.ok) {
      out.textContent = "通过！后端说：\n" + JSON.stringify(data, null, 2);
    } else {
      out.textContent = "被拒绝了！HTTP " + resp.status + "\n" + JSON.stringify(data, null, 2);
    }
  }
  </script>
</body>
</html>
"""
