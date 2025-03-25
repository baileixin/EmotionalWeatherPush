import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime
from utils import log_execution  # 导入 log_execution 函数

def send_email(subject, body, recipients=None, html_body=None, sender_name="超级猪猪侠"):
    """通过SMTP发送邮件"""
    sender_name = os.getenv("SENDER_NAME", sender_name)  # 新增：从.env中设置sender_name
    try:
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        recipients = recipients or [os.getenv("EMAIL_RECIPIENT")]
        
        if not all([smtp_server, smtp_port, smtp_user, smtp_password, recipients]):
            log_execution("SMTP配置或收件人邮箱缺失，无法发送邮件")
            print("请在.env文件中配置SMTP相关信息和收件人邮箱")
            return
        
        custom_from_address = formataddr((sender_name, smtp_user))
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = custom_from_address
        message["To"] = ", ".join(recipients)
        
        text_part = MIMEText(body, "plain", "utf-8")
        message.attach(text_part)
        
        if html_body:
            html_part = MIMEText(html_body, "html", "utf-8")
            message.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(custom_from_address, recipients, message.as_string())
        log_execution(f"邮件已成功发送到: {', '.join(recipients)}")
        print(f"邮件已成功发送到 {', '.join(recipients)}")
    except Exception as e:
        error_message = f"发送邮件失败: {str(e)}"
        print(error_message)
        log_execution(error_message)

def send_email_to(email, city, report, subject, is_html=False):
    """通用邮件发送逻辑"""
    if not email:
        log_execution(f"邮箱地址未配置，无法发送邮件: {email}")
        print(f"请在.env文件中配置邮箱地址: {email}")
        return
    
    if is_html:
        html_body = report  # 直接使用 HTML 格式的正文
        plain_body = "请查看HTML格式的天气预报内容。"
    else:
        html_body = None
        plain_body = report
    
    log_execution(f"准备发送邮件到: {email}")
    send_email(subject=subject, body=plain_body, html_body=html_body, recipients=[email])

def send_weather_emails(city, body, subject):
    """发送天气预报邮件到主收件人和监控邮箱"""
    recipient = os.getenv("EMAIL_RECIPIENT")
    monitor_email = os.getenv("MONITOR_EMAIL")
    
    send_email_to(recipient, city, body, subject, is_html=True)
    send_email_to(monitor_email, city, body, subject, is_html=True)
    
    log_execution("邮件发送流程完成")
