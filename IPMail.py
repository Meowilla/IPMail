# Introduction: get ipconfig and send email to self, check interval default value is 30s
# 简介： 获取IP配置并发送到自己的邮箱，检测间隔默认30秒
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import os
import time

def _formatAddr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendMail(IP):
    sender = '' # input your email address 输入你的邮件地址
    receiver = sender
    grantCode = ''  # input your grant-code or password 输入你的授权码或密码
    SMTPServer = ['smtp.qq.com', 587]   # input SMTP server and port of your email provider 输入你邮件提供商的 SMTP 服务器以及端口号

    msg = MIMEText(f'{IP}', 'plain', 'utf-8')   # 邮件的内容
    msg['From'] = _formatAddr(f'self <{sender}>')
    msg['To'] = _formatAddr(f'self <{receiver}>')
    msg['Subject'] = Header('IP Return', 'utf-8').encode() # Subject of mail 邮件的主题

    session = smtplib.SMTP(SMTPServer[0], SMTPServer[1])
    session.starttls()
    #session.set_debuglevel(1)
    session.login(sender, grantCode)
    session.sendmail(sender, [receiver], msg.as_string())
    session.quit()


def getIP():
    content = os.popen("ipconfig")
    return content.read()


def monitor(interval):
    old = ''
    while True:
        new = getIP()
        if old != new:
            sendMail(new)
            old = new
        time.sleep(interval)

monitor(30)
