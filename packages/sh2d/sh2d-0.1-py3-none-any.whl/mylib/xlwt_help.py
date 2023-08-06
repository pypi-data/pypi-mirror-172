#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import xlwt


def list2xls(excle_name, **tables):
    ''''
    写入xls文件
    :param excle_name: excel文件路径
    :param sheet: sheet名称与数据
    '''
    def write_row(sheet, n, row):
        for i in range(0, len(row)):
            sheet.write(n, i, row[i])
    workbook = xlwt.Workbook()
    for name, rows in tables.items():
        sheet = workbook.add_sheet(name)
        for n, row in enumerate(rows):
            write_row(sheet, n, row)
    workbook.save(excle_name)
