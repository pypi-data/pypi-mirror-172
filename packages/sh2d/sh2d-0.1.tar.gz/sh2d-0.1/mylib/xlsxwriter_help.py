#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import xlsxwriter


def list2xlsx(excle_name, **tables):
    ''''
    写入xlsx文件
    :param excle_name: excel文件路径
    :param sheet: sheet名称与数据 {'sheet1':["",""]}
    '''
    workbook = xlsxwriter.Workbook(excle_name)
    for name, rows in tables.items():
        if not rows:
            continue
        worksheet = workbook.add_worksheet(name)
        for index, row in enumerate(rows):
            worksheet.write_row(index, 0, row)
    workbook.close()


def jsonlist2xlsx(excle_name, **tables):
    ''''
    写入xlsx文件
    :param excle_name: excel文件路径
    :param sheet: sheet名称与数据 {'sheet1':[{"a":"b"}]}}
    '''
    _title = {}
    for name in tables:
        _title.setdefault(name, [])
        for item in tables[name]:
            for t in item.keys():
                if t not in _title[name]:
                    _title[name].append(t)
    _dict = {}
    for name in tables:
        _dict.setdefault(name, [_title[name]])
        for item in tables[name]:
            row = []
            for t in _title[name]:
                row.append(str(item.get(t, '')))
            _dict[name].append(row)
    list2xlsx(excle_name, **_dict)
