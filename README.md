# 情感化天气推送系统

## 项目简介
本项目基于和风天气 API 和 LangChain，提供高度个性化和情感化的天气预报服务。系统不仅实时获取天气数据，还结合纪念日信息生成温馨幽默的预报，通过邮件自动推送，为用户带来每日惊喜体验。

## 功能详解

### 1. 实时天气获取
- 通过和风天气 API 获取指定城市24小时内的天气数据（温度、湿度、风力、天气状况等）。
- 利用 HTTP 请求实现数据抓取，并进行错误处理，确保数据稳定准确。

### 2. 纪念日计算
- 从环境变量中读取纪念日日期，自动计算自纪念日起至今的天数。
- 为预报生成提供时间参考，使内容更具个性化。

### 3. 个性化天气预报生成
- 使用 LangChain 与 LLM 模型结合天气数据和纪念日天数生成幽默且贴心的天气预报。
- 预报内容包括四个模块：情感化开场、详细天气播报、分时段生活指南以及动态关怀提示。
- 生成的邮件正文以 HTML 格式输出，并附带一个简洁时尚的邮件标题。

### 4. 邮件推送
- 采用 SMTP 协议，通过配置的发件服务器发送邮件。
- 同时推送至主收件人和监控邮箱，确保预报信息的覆盖与备份。
- 邮件发送过程集成日志记录，方便追踪发送状态及问题诊断。

### 5. 定时任务调度
- 利用 scheduler 模块每天定时在北京时间早上7点触发主程序，确保每日准时获取最新天气数据及生成预报。
- 使用 schedule 库结合时区校验保证任务运行的稳定性。

### 6. 日志记录与错误监控
- 系统运行中的关键流程（如数据获取、预报生成、邮件发送）均有日志记录，存入 execution_log.txt 文件。
- 便于快速定位异常及后续问题处理。

## 环境依赖与安装

- Python 3.8 或更高版本
- 依赖库：requests, schedule, pytz, python-dotenv, langchain, smtplib 等（详见 requirements.txt）。

### 安装步骤
1. 克隆项目：
   ```bash
   git clone <项目地址>
   cd LangChain
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   - 将根目录下的 `example.env` 文件复制到 weather_Hello 文件夹并重命名为 `.env`，然后按实际情况填写各项参数。

## 使用方法

### 运行主程序
直接运行主程序以获取天气、生成预报并发送邮件：
```bash
python weather_Hello/main.py
```

### 启动定时任务
运行 scheduler 模块，每天自动执行主程序：
```bash
python weather_Hello/scheduler.py
```

## 文件结构说明
```
LangChain/
├── weather_Hello/
│   ├── main.py               # 主程序入口，协调各功能模块
│   ├── weather.py            # 天气数据获取和格式化
│   ├── email_utils.py        # 邮件发送工具
│   ├── anniversary.py        # 纪念日天数计算模块
│   ├── llm_utils.py          # LLM预报生成工具
│   ├── scheduler.py          # 定时任务调度模块
│   ├── utils.py              # 日志记录及其他辅助工具
│   ├── .env                  # 环境变量配置文件
├── requirements.txt          # Python依赖项清单
└── README.md                 # 项目说明文档
```

## 注意事项
- 请确保 `.env` 文件中的 API 密钥、SMTP配置、收件地址等信息配置正确。
- 网络不稳定时数据获取可能失败，检查日志文件 execution_log.txt 可帮助诊断问题。
- 定时任务依赖服务器时间，需保证与北京时间同步。

## 贡献与许可
欢迎提交 Issue 或 Pull Request 改进项目。  
本项目遵循 [MIT License](LICENSE) 协议。