#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import requests


def api_search(email, key, query_str, fields, size, page=1):
    url = 'https://fofa.info/api/v1/search/all'
    params = {
        'email': email,
        'key': key,
        'qbase64': base64.b64encode(query_str.encode('utf-8')).decode('utf-8'),
        'size': size,
        'fields': ",".join(fields),
        'page': page
    }
    rj = requests.get(url, params=params).json()
    status = rj.get('errmsg')
    if status:
        if '401 Unauthorized' in status:
            print('api或邮箱不正确!')
        return
    print("查询参数：{}，当前第{}页，结果数：{}".format(
        query_str, page, len(rj.get('results'))))
    return rj.get('results')


def fofa(email, key, query_list, fields, size=100, max_page=100, check_url=True):
    ''' 
    fofa 批量api查询
    :param email eg: xxxx@qq.com
    :param key eg: asssssssssssssssss
    :param query_list eg: ['app="tomcat"']
    :param fields eg: ['host','title','ip','domain','port','protocol','city']
    '''
    results = []
    for query_str in query_list:
        for page in range(1, max_page+1):
            try:
                res = api_search(email, key, query_str,
                                 fields, size=size, page=page)
            except:
                continue
            if res:
                for item in res:
                    if len(fields) == 1:
                        _ = {fields[0]: item}
                    else:
                        _ = dict(zip(fields, item))
                    _.update({'query_str': query_str})
                    if check_url:
                        _.update({'url': _['host'] if 'http' in _[
                                 'host'] else "http://"+_['host']})
                    results.append(_)
            else:
                break
    return results
