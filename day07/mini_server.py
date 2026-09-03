# Day7 最小服务器：让你看见"访问一个网址 = 执行一个函数"
# 你是网络工程师，把下面这个当成"监听 8001 端口的小服务器"就行
from fastapi import FastAPI

app = FastAPI()   # 造一个服务器对象

# 装饰器 @app.get("/hi") = 告诉服务器："有人用 GET 方式访问 /hi 这个路径时，执行下面这个函数"
@app.get("/hi")
def hi():
    return {"msg": "你好陈果！这个函数的返回，就是网址给你的内容"}
