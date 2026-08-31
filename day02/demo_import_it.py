# 这个文件叫 demo_import_it.py

print("【主程序启动】我自己的 __name__ =", repr(__name__))
print("【主程序】现在我要 import demo_name 了")
print()

import demo_name

print()
print("【主程序】import 完毕，我的 __name__ 还是", repr(__name__))
