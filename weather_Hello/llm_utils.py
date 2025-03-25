import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化LangChain的ChatOpenAI模型
llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("SILICONFLOW_API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model_name="deepseek-ai/DeepSeek-V3"
)

def generate_weather_report(city, anniversary_days, hourly_forecast):
    """生成趣味天气预报"""
    template = """
    请你依据以下内容框架，把每日气象数据{hourly_forecast}转化为对一位异性好友的问候，自然地融入关怀，
    ，然后用html源码的方式，给它加一些样式，4个模块每个模块都单独一段。
    最后根据内容设计一个邮件标题。要求：
    1、保持创意且富有吸引力
    2、语气适当俏皮但不轻浮
    3、严格控制在 15 字以内
    4、可酌情添加一个相关表情符号
    5、不要与邮件正文表达重复

    ###  1: 情感化开场模块
    早安句式巧妙嵌入天气、季节特色信息。

    ### 2: 天气播报模块
    需要包含城市名称{city}、天气、气温、湿度、风力，如果遇到雨天或者极端天气则增加警告标志

    ### 3：分时段生活指南
    通勤时段：穿衣建议+出行提醒
    午间时段：紫外线防护+饮食建议
    晚间时段：放松建议

    ### 4: 动态关怀模块
    根据不同的天气状况，给出一句幽默风趣且贴心的特别关怀内容。根据日期当天日期查询判断今天是否属于节日，如果是就增加一个节日彩蛋，如果不是则省略，不要作出“今天不是什么特殊的日子”之类的解释。

    ### 5：内容风格要求
    1. 采用自然聊天式排版，适当加入表情符号，避免机械播报。
    2. 禁用所有亲密称谓（亲爱的 / 宝贝等），符合{relationship}的状态。
    3. 用自然的语言融入我们已经相识的天数{anniversary_days}

    ### 6： 禁止的内容
    禁止出现虚构的具体事件、共同回忆（如“我给你点了外卖”“你昨晚...”“路边新开了家...”“我们之前...”）。

    ### 7 HTML样式要求
    1. **屏幕适配**：
    - 严格适配手机QQ邮箱客户端竖屏显示
    -使用响应式留白，body的padding:至少20px，实现移动端友好间距，制造呼吸感
    2. 卡片容器设计圆角
    3. 所有使用的Unicode字符必须是Web安全的，并且能够在所有主流邮件客户端（如QQ, 163，139等）中正常显示。

    ### 8 输出格式
    请严格按以下格式生成内容：正文|||标题
    正文部分直接输出html源码，以<!DOCTYPE html>开始，以</html>结束，不要以【```html】开头，不要有多余的文字、符号、解释。
    标题部分直接输出文本格式的标题
    """
    # 定义生成报告所需变量
    variables = {
        "city": city,
        "anniversary_days": anniversary_days,
        "hourly_forecast": hourly_forecast,
        "relationship": os.getenv("RELATIONSHIP", "朋友")  # 新增：从.env文件中获取关系设置
    }
    
    prompt = PromptTemplate(
        input_variables=["city", "anniversary_days", "hourly_forecast", "relationship"],  # 修改：添加 relationship
        template=template
    )
    # 修改部分：使用管道操作符组合 prompt 和 llm，并用 invoke 调用
    chain = prompt | llm
    result = chain.invoke(variables)
    from utils import log_execution  # 导入日志记录函数
    if hasattr(result, "usage_metadata"):
        log_execution(f"Token使用量: {result.usage_metadata}")
    return result

def parse_weather_report(report, city):
    """解析天气预报的标题和正文"""
    # 如果 report 不是字符串，则尝试转换为字符串（例如获取 .content 属性）
    if not isinstance(report, str) and hasattr(report, "content"):
        report = report.content
    if "|||" in report:
        body, subject = report.split("|||", 1)
    else:
        body, subject = report, f"{city}的趣味天气预报"
    return body.strip(), subject.strip()
