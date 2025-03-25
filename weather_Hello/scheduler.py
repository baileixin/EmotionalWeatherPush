import schedule
import time
import os
from datetime import datetime
import pytz  # 引入 pytz 库

def run_main():
    """运行 main.py 文件"""
    os.system("python main.py")

def is_beijing_time_7am():
    """检查当前时间是否为北京时间早上7点"""
    beijing_tz = pytz.timezone("Asia/Shanghai")
    now = datetime.now(beijing_tz)
    return now.hour == 7 and now.minute == 0

# 定时检查是否为北京时间早上7点
print("定时任务已启动，每天北京时间早上7点运行 main.py")

while True:
    if is_beijing_time_7am():
        run_main()
    time.sleep(60)  # 每分钟检查一次
