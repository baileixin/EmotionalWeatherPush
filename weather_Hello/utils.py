from datetime import datetime

def log_execution(message):
    """记录执行日志到 execution_log.txt 文件"""
    with open("execution_log.txt", "a", encoding="utf-8") as log_file:
        # 如果是程序启动消息，添加分割线
        if message == "程序启动":
            log_file.write("\n" + "=" * 50 + "\n")
        log_file.write(f"{datetime.now()}: {message}\n")
