#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

def bj_mail(subject,cont):
    # @subject:邮件主题
    # @msg :邮件内容
    # @toaddrs:收信人的邮箱地址
    # @fromaddr:发信人的邮箱地址
    # @smtpaddr :smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    # @password :发信人的邮箱密码
    fromaddr = 'yst_super@163.com'
    toaddrs = ['963668943@qq.com','748180585@qq.com','1304172984@qq.com']
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(cont, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = fromaddr
    message['To'] = ','.join(toaddrs)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        username = 'yst_super@163.com'
        password = 'yst123456' #授权码
        smtp.login(username, password)
        smtp.sendmail(fromaddr, toaddrs, message.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# 主函数
def send_mail(today_time,today_i):
    print()
    today_t = str(datetime.date.today())
    subject = "%s教育决策信息平台爬取情况" % today_t
    cont = """
    <h1>爬取详情</h1>
    <table border="1">
      <tr>
        <th>爬取时间</th>
        <th>爬取数量</th>
        <th>爬取用时</th>
      </tr>
      <tr>
        <td>"""+str(today_t)+"""</td>
        <td>"""+str(today_i)+"""篇</td>
        <td>"""+str(today_time)+"""秒</td>
      </tr>
    </table>
    <p>
    <h3>快速审核通道</h3>
    <p><a href="http://edu-backend.tmsb2b.com/index">点击进入管理员页面</a></p>
    <p><a href="http://edu-web.tmsb2b.com/index/main/edu">点击进入用户页面</a></p>
    """
    bj_mail(subject,cont)

#
# today_time = '1'
# today_i = '2'
# today_t = '3'
# send_mail(today_time,today_i)

