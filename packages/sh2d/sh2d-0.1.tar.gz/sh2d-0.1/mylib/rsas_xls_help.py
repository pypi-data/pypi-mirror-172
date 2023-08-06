#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
from .xlrd_help import excel2list

def parse_rows(rows):
    '''填充合并单元格'''
    for i in range(len(rows)):
        if rows[i][0] == '':
            for j in range(5):
                rows[i][j] = rows[i-1][j]
    return rows

def get_x_list(rows, y, regx, equal=False):
    '''获取指定列中关键字行数'''
    _ = []
    for x in range(len(rows)):
        if equal:
            if regx == rows[x][y]:
                _.append(x)
        else:
            if re.search(regx, rows[x][y]):
                _.append(x)
    return _

def list_subgroup(row, max=-1):
    '''列表连续两个元素分组'''
    _ = []
    for i in range(len(row)):
        if i+1 < len(row):
            _.append([row[i], row[i+1]])
        else:
            _.append([row[i], max])
    return _


def deal_ip_xls(excel_file, task_name, ip):
    '''
    处理单个IP扫描结果
    :param excel_file eg: excel文件名
    :param task_name eg: 任务或系统名称
    :param ip eg: ip
    :return json
    '''
    data = excel2list(excel_file)
    result = {}
    for ws_name in data:
        if ws_name in ['远程漏洞']:
            name = ws_name + '_' + data[ws_name][0][0]
            result.setdefault(name, [])
            title = data[ws_name][1]
            for row in parse_rows(data[ws_name][2:]):
                _ = {'任务名称': task_name, 'ip地址': ip}
                _.update(dict(zip(title, row)))
                if '' in _:
                    del _['']
                result[name].append(_)
        elif ws_name in ['配置合规信息']:
            for i, j in list_subgroup(get_x_list(data[ws_name], 0, '\S+'), len(data[ws_name])):
                if all([o == '' for o in data[ws_name][j:j]]):
                    j -= 1 
                name = ws_name + '_' + data[ws_name][i][0]
                result.setdefault(name, [])
                title = data[ws_name][i+1][1:]
                for row in parse_rows(data[ws_name][i+2:j]):
                    _ = {'任务名称': task_name, 'ip地址': ip}
                    _.update(dict(zip(title, row[1:])))
                    if '' in _:
                        del _['']
                    result[name].append(_)
        else:
            for i, j in list_subgroup(get_x_list(data[ws_name], 0, '\S+'), len(data[ws_name])):
                if all([o == '' for o in data[ws_name][j:j]]):
                    j -= 1
                name = ws_name + '_' + data[ws_name][i][0]
                x_list = get_x_list(data[ws_name][i:j], 1, '', equal=True)
                if len(x_list) == 1:
                    result.setdefault(name, [])
                    title = data[ws_name][i+1][1:]
                    for l in range(i+2, j):
                        _ = {'任务名称': task_name, 'ip地址': ip}
                        _.update(dict(zip(title, data[ws_name][l][1:])))
                        if '' in _:
                            del _['']
                        result[name].append(_)
                else:
                    for m, n in enumerate(list_subgroup(x_list)):
                        new_name = name + '_' + str(m+1)
                        result.setdefault(new_name, [])
                        x, y = n
                        title = data[ws_name][i+1+x][1:]
                        for l in range(i+2+x, j if y == -1 else i+y):
                            _ = {'任务名称': task_name, 'ip地址': ip}
                            _.update(dict(zip(title, data[ws_name][l][1:])))
                            if '' in _:
                                del _['']
                            result[new_name].append(_)
    return result


def deal_index_xls(excel_file, task_name):
    '''
    处理index.xls结果
    :param excel_file eg: excel文件名
    :param task_name eg: 任务或系统名称
    :return json
    '''
    data = excel2list(excel_file)
    result = {}
    for ws_name in data:
        if ws_name in ['配置信息']:
            for i, j in list_subgroup(get_x_list(data[ws_name], 0, '\S+'), len(data[ws_name])):
                if all([o == '' for o in data[ws_name][j:j]]):
                    j -= 1 
                name = ws_name + '_' + data[ws_name][i][0]
                result.setdefault(name, [])
                title = data[ws_name][i+1][1:]
                for row in parse_rows(data[ws_name][i+2:j]):
                    _ = {'任务名称': task_name, 'ip地址': ip}
                    _.update(dict(zip(title, row[1:])))
                    if '' in _:
                        del _['']
                    result[name].append(_)
        else:
            for i, j in list_subgroup(get_x_list(data[ws_name], 0, '\S+'), len(data[ws_name])):
                if all([o == '' for o in data[ws_name][j:j]]):
                    j -= 1
                name = ws_name + '_' + data[ws_name][i][0]
                x_list = get_x_list(data[ws_name][i:j], 1, '', equal=True)
                if len(x_list) == 1:
                    result.setdefault(name, [])
                    title = data[ws_name][i+1][1:]
                    for l in range(i+2, j):
                        _ = {'任务名称': task_name}
                        _.update(dict(zip(title, data[ws_name][l][1:])))
                        if '' in _:
                            del _['']
                        result[name].append(_)
                else:
                    for m, n in enumerate(list_subgroup(x_list)):
                        new_name = name + '_' + str(m+1)
                        result.setdefault(new_name, [])
                        x, y = n
                        title = data[ws_name][i+1+x][1:]
                        for l in range(i+2+x, j if y == -1 else i+y):
                            _ = {'任务名称': task_name}
                            _.update(dict(zip(title, data[ws_name][l][1:])))
                            if '' in _:
                                del _['']
                            result[new_name].append(_)
    return result