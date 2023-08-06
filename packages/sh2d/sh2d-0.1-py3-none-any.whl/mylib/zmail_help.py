#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import zmail


def send_mail(title, content, attachments=[], username="", password="", to_user=[], cc=[], is_html=False):
    ''''
    发送邮件
    :param title: 标题
    :param content: 邮件内容 文本或html
    :param attachments: 附件完整路径列表
    :param username: 邮箱账号
    :param password: 邮箱密码或授权码
    :param to_user: 收件人列表
    :param cc: 抄送人列表
    :param is_html: 是否html 默认False
    '''
    server = zmail.server(username, password)
    mail = {'subject': title, 'attachments': attachments, }
    if is_html:
        mail['content_html'] = content
    else:
        mail['content_text'] = content
    server.send_mail(to_user, mail, cc=cc)
