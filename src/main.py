# 导入必要的模块
import logging
import sys

# 从其他模块导入类和函数
from cos import Cos


# 定义函数
def main():
    # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    cos = Cos()
    cos.upload()


# 当文件作为脚本运行时执行
if __name__ == "__main__":
    main()
