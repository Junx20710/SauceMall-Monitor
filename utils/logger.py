from loguru import logger
import os
import sys

# 创建 logs 目录
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 移除默认的 handler（避免重复打印）
logger.remove()

# 1. 这是一个控制台 Handler (Console)
# 作用：在终端显示包含颜色的日志，方便开发调试
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 2. 这是一个文件 Handler (File)
# 作用：把日志存到文件里，跑飞书自动化或者出问题时可以回溯
# rotation="500 MB": 单个文件超过 500MB 自动切割
# retention="10 days": 只保留最近 10 天的日志
logger.add(
    os.path.join(log_dir, "runtime_{time}.log"),
    rotation="500 MB",
    retention="10 days",
    encoding="utf-8",
    level="DEBUG"
)

# 导出 logger 供其他模块使用
__all__ = ["logger"]
