import os
from datetime import datetime

def calculate_anniversary_days():
    """计算纪念日与当前日期的天数"""
    try:
        start_date = os.getenv("ANNIVERSARY_DATE", "2022-01-01")
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        current_date_obj = datetime.now()
        delta = current_date_obj - start_date_obj
        return delta.days
    except Exception as e:
        print(f"计算纪念日天数时出错: {str(e)}")
        return 0
