# 演示：model_dump() 到底从哪来
from pydantic import BaseModel

# ===== 第 1 部分：自己写的普通类，没有 model_dump =====
class 普通包裹:
    def __init__(self):
        self.内容 = "一封信"
        self.重量 = "500克"

p1 = 普通包裹()
print("普通类 有 model_dump 吗？", hasattr(p1, "model_dump"))
# print(p1.model_dump())   # 取消注释会报错：普通类没有这个方法

# ===== 第 2 部分：继承 pydantic 的 BaseModel，自动获得 model_dump =====
class 高级包裹(BaseModel):
    内容: str = "一封信"
    重量: str = "500克"

p2 = 高级包裹()
print("pydantic 模型 有 model_dump 吗？", hasattr(p2, "model_dump"))
print("调用后变成：", p2.model_dump())

print()
print("===== 回到 response =====")
print("OpenAI 的 ChatCompletion 也是 pydantic 模型")
print("所以它天生就有 model_dump()，能把对象扒成字典看")
