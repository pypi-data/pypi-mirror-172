#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from dns import resolver


def domain2ip(domain):
    """
    解析域名到IP
    :param domian: 域名
    :return 返回IP列表
    """
    try:
        answers = resolver.query(domain, 'A')
        return [_.address for _ in answers]
    except:
        return []

def domain2cname(domain):
    """
    解析域名到IP
    :param domian: 域名
    :return 返回cname列表
    """
    try:
        answers = resolver.query(domain, 'CNAME')
        return [str(_.target).strip(".").lower() for _ in answers]
    except:
        return []

if __name__ == '__main__':
    pass
    # domain = 'www.baidu.com'
    # print(domain,domain2ip(domain),domain2cname(domain))
