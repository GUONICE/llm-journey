# 这个文件叫 demo_name.py

print("本文件里的 __name__ =", repr(__name__))

if __name__ == "__main__":
    print("  → 所以走了 if 里面：我是被直接运行的")
else:
    print("  → 所以走了 else 里面：我是被别人 import 的")
