import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def format_hourly_forecast(hourly_data):
    """格式化24小时天气数据"""
    return "\n".join([
        f"{hour['fxTime']}: 温度 {hour['temp']}°C, {hour['text']}, 风向 {hour['windDir']}, 风力 {hour['windScale']}级"
        for hour in hourly_data
    ])

def get_weather_data(city="深圳"):
    """获取指定城市的24小时天气信息"""
    weather_api_key = os.getenv("WEATHER_API_KEY")
    try:
        # 获取城市ID
        location_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={weather_api_key}"
        location_response = requests.get(location_url)
        location_data = location_response.json()
        
        if location_data.get("code") != "200" or not location_data.get("location"):
            return {"error": f"无法找到城市: {city}", "hourly": []}
        
        city_id = location_data["location"][0]["id"]
        
        # 获取24小时天气
        weather_url = f"https://devapi.qweather.com/v7/weather/24h?location={city_id}&key={weather_api_key}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_data.get("code") != "200":
            return {"error": "获取天气数据失败", "hourly": []}
        
        # 格式化天气数据
        formatted_forecast = format_hourly_forecast(weather_data["hourly"])
        return {"city": city, "forecast": formatted_forecast, "hourly": weather_data["hourly"]}
    except Exception as e:
        return {"error": f"获取天气数据时出错: {str(e)}", "hourly": []}
