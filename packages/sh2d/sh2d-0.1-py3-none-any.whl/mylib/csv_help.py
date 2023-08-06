#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv


def list2csv(path, rows,encoding='utf8'):
    ''''
    写入csv文件
    :param path: csv文件路径
    :param rows: 多行数据[[1,2],[...]]
    '''
    with open(path, 'a', newline='',encoding=encoding) as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerows(rows)


def csv2list(path,encoding='utf8'):
    ''''
    读取csv文件
    :param path: csv文件路径
    :return [[1,2,3],[4,5,6]]
    '''
    with open(path, 'r',encoding=encoding) as f:
        reader = csv.reader(f)
        return [row for row in reader]

def csv2json(path,encoding='utf8'):
    ''''
    读取csv文件
    :param path: csv文件路径
    :return 返回json eg: [{"表头":第1行}，{"表头":第2行}],"sheet2":[{"表头":第1行}，{"表头":第2行}]
    '''
    rows = []
    with open(path, 'r',encoding=encoding) as f:
        reader = csv.reader(f)
        rows += [row for row in reader]
    return [dict(zip(rows[0],row)) for row in rows[1:]]

def jsonlist2csv(path,items,encoding='utf8'):
    ''''
    写入csv文件
    :param path: csv文件路径
    :param items[{"表头":第1行}，{"表头":第2行}],"sheet2":[{"表头":第1行}，{"表头":第2行}]
    '''
    rows = [[],]
    for item in items:
        for t in item.keys():
            if t not in rows[0]:
                rows[0].append(t)
    for item in items:
        row = []
        for t in rows[0]:
            row.append(str(item.get(t,'')))
        rows.append(row)
    list2csv(path, rows,encoding)