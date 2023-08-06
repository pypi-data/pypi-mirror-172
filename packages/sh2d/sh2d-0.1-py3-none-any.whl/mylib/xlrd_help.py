#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple


def excel2list(excle_name):
    """
    读取表格为列表
    :param excle_name: excel文件路径
    :return 返回json eg: {"sheet1":[[第一行数据],[第二行数据],...}
    """
    _ = {}
    try:
        wb = xlrd.open_workbook(filename=excle_name)
    except:
        print("Faild open {}".format(excle_name))
        return _
    wss = wb.sheets()
    if len(wss) == 0:
        print("{} is null".format(excle_name))
    for i in range(0, len(wss)):
        _.setdefault(wss[i].name, [])
        for n in range(0, wss[i].nrows):
            row = []
            for m in range(0, wss[i].ncols):
                ctype = wss[i].cell(n, m).ctype
                cell = wss[i].cell_value(n, m)
                if ctype == 2 and cell % 1 == 0:
                    cell = int(cell)
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y-%m-%d %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                row.append(cell)
            _[wss[i].name].append(row)
    return _


def excel2json(excle_name):
    """
    读取表格为json
    :param excle_name: excel文件路径
    :return 返回json eg: {"sheet1":[{"表头":第1行}，{"表头":第2行}],"sheet2":[{"表头":第1行}，{"表头":第2行}],...}
    """
    _ = {}
    try:
        wb = xlrd.open_workbook(filename=excle_name)
    except Exception as e:
        print("Faild open {},{}".format(excle_name,e))
        return _
    wss = wb.sheets()
    if len(wss) == 0:
        print("{} is null".format(excle_name))
    for i in range(0, len(wss)):
        _.setdefault(wss[i].name, [])
        try:
            title = wss[i].row_values(0)
        except Exception:
            print("{}/{} is null".format(excle_name, wss[i].name))
            continue
        for n in range(1, wss[i].nrows):
            row = []
            for m in range(0, wss[i].ncols):
                ctype = wss[i].cell(n, m).ctype
                cell = wss[i].cell_value(n, m)
                if ctype == 2 and cell % 1 == 0:
                    cell = int(cell)
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y-%m-%d %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                row.append(cell)
            _[wss[i].name].append(dict(zip(title, row)))
    return _
