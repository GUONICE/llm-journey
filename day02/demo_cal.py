# 这个文件叫 demo_cal.py（被别人导入的工具模块）


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


print("[demo_cal] 文件被加载了 —— 这行在被 import 时也会执行")


if __name__ == "__main__":
    print("[demo_cal] 我直接运行时，才会执行这里")
    print("1 + 2 =", add(1, 2))
