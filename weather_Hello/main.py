import argparse
from dotenv import load_dotenv
from weather import get_weather_data, format_hourly_forecast
from anniversary import calculate_anniversary_days
from llm_utils import generate_weather_report, parse_weather_report
from email_utils import send_weather_emails
import os
from datetime import datetime
from utils import log_execution  # 导入 log_execution 函数

# 加载环境变量
load_dotenv()

def main():
    # 从环境变量中获取城市名称
    city = os.getenv("DEFAULT_CITY", "深圳")
    monitor_email = os.getenv("MONITOR_EMAIL")
    
    log_execution("程序启动")
    
    # 获取天气数据
    print(f"正在为 {city} 获取天气数据...\n")
    log_execution(f"开始获取 {city} 的天气数据")
    weather_data = get_weather_data(city)
    if "error" in weather_data:
        error_message = f"获取天气数据失败: {weather_data['error']}"
        print(error_message)
        log_execution(error_message)
        return
    log_execution(f"成功获取 {city} 的天气数据")
    
    # 计算纪念日天数
    anniversary_days = calculate_anniversary_days()
    log_execution(f"纪念日天数计算结果: {anniversary_days}")
    
    # 格式化天气数据
    hourly_forecast = format_hourly_forecast(weather_data["hourly"])
    log_execution("天气数据格式化完成")
    
    # 生成天气预报
    report = generate_weather_report(city, anniversary_days, hourly_forecast)
    log_execution("天气预报生成成功")
    print(report)
    
    # 解析标题和正文
    body, subject = parse_weather_report(report, city)
    log_execution(f"天气预报标题解析成功: {subject}")
    
    # 发送邮件
    send_weather_emails(city, body, subject)
    log_execution("邮件发送流程完成")

if __name__ == "__main__":
    main()