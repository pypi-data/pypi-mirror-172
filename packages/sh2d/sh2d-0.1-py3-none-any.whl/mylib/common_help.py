#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from itertools import groupby

def mask2num(mask):
    """
    掩码转数字
    :param mask: 255.255.255.255
    :return 32
    """
    def count_bit(bin_str): return len([i for i in bin_str if i == '1'])
    mask_splited = mask.split('.')
    mask_count = [count_bit(bin(int(i))) for i in mask_splited]
    return sum(mask_count)


def num2mask(mask_int):
    """
    数字转掩码
    :param mask_int: 32
    :return 255.255.255.255
    """
    bin_arr = ['0' for i in range(32)]
    for i in range(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


def ip2num(ip):
    """
    IP转数字
    :param ip: 1.1.1.1
    :return 12345567
    """
    ips = [int(x) for x in ip.split('.')]
    return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]


def num2ip(num):
    """
    数字转IP
    :param num: 12345567
    :return 1.1.1.1
    """
    return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))


def gen_ip(ip):
    """
    根据IP范围生成IP
    :param ip: 1.1.1.1-1.1.1.3
    :return ['1.1.1.1','1.1.1.2']
    """
    start, end = [ip2num(x) for x in ip.split('-')]
    return [num2ip(num) for num in range(start, end+1) if num & 0xff]

def num2numnum(numlist):
    """
    根据数字列表生成数字范围列表
    :param numlist: [1,2,18,3,5,6,7,8,13,12,11,10]
    :return [[1,3],[5,8],[10,13]]
    """
    numlist.sort()
    numnumlist = []
    fun = lambda x: x[1] - x[0]
    for k, g in groupby(enumerate(numlist), fun):
        _ = [v for i, v in g]
        if len(_) == 1:
            numnumlist.append([_[0],_[0]])
        else:
            numnumlist.append([_[0],_[-1]])
    return numnumlist

if __name__ == '__main__':
    pass
    # mask = "255.255.255.224"
    # num = 23
    # ip = "8.8.8.8"
    # num1 = 134744073
    # ipip = "1.1.1.1-1.1.1.4"
    # numlist = [1,2,18,3,5,6,7,8,13,12,11,10]
    # print(f"func: mask2num\tinput: {mask}\toutput: {mask2num(mask)}")
    # print(f"func: num2mask\tinput: {num}\toutput: {num2mask(num)}")
    # print(f"func: ip2num\tinput: {ip}\toutput: {ip2num(ip)}")
    # print(f"func: num2ip\tinput: {num1}\toutput: {num2ip(num1)}")
    # print(f"func: gen_ip\tinput: {ipip}\toutput: {gen_ip(ipip)}")
    # print(f"func: num2numnum\tinput: {numlist}\toutput: {num2numnum(numlist)}")


