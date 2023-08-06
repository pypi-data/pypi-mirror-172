#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import ipaddress

from .common_help import gen_ip, ip2num, num2ip, num2numnum


def net2ipip(net_str, strict=False):
    """
    转化单个其他网段格式成单个ip-ip格式
    :param net_str: 传入合法网段，eg: 192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :return 返回 192.168.1.5-192.168.1.8
    """

    if re.search(r"^\d+\.\d+\.\d+\.\d+-\d+$", net_str):
        _net, a, b = re.findall(r"(\d+\.\d+\.\d+\.)(\d+)-(\d+)", net_str)[0]
        net = "{}{}-{}{}".format(_net,a,_net,b)
    elif re.match(r"^\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+$", net_str):
        net = net_str
    else:
        try:
            net = '{}-{}'.format(ipaddress.ip_network(net_str, strict=strict).network_address.compressed,ipaddress.ip_network(net_str, strict=strict).broadcast_address.compressed)
        except Exception as e:
            print('{} ,error:{}'.format(net_str,e))
            net = '0-0'
    return net


def net2ip(net_str, strict=False):
    """
    拆分单个网段为IP列表
    :param net_str: 传入合法网段，eg: 192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :param strict: 是否校验网络地址 eg: False
    :return 返回list eg [ip1,ip2,...]
    """
    ip_ip = net2ipip(net_str, strict=strict)
    if ip_ip == '0-0':
        return []
    else:
        return gen_ip(ip_ip)


def net2cidr(net_str, strict=False):
    """
    合并单个网段为cdir格式列表
    :param net_str: 传入合法网段，eg:  192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :return 返回 ["192.168.1.0/24"]
    """
    ip_ip = net2ipip(net_str, strict=strict)
    start_ip, end_ip = ip_ip.split('-')
    try:
        return [ipaddr.compressed for ipaddr in ipaddress.summarize_address_range(
            ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip))]
    except:
        return []


def ip2ipip(iplist):
    """
    合并ip列表为ip-ip格式列表
    :param net_str: 传入合法网段，eg:  [ip1,ip2,...]
    :return 返回 ["ip1-ip2","ip3-ip4"]
    """
    num_iplist = [ip2num(_) for _ in iplist]
    numnumlist = num2numnum(num_iplist)
    return ["{}-{}".format(num2ip(a),num2ip(b)) for a, b in numnumlist]


def ip2cidr(iplist):
    """
    合并ip列表为cidr格式列表
    :param net_str: 传入合法网段，eg:  [ip1,ip2,...]
    :return 返回 ["ip1/24","ip3/32"]
    """

    num_iplist = [ip2num(_) for _ in iplist]
    numnumlist = num2numnum(num_iplist)
    cidr_list = []
    for a, b in numnumlist:
        try:
            cidr_list += [ipaddr.compressed for ipaddr in ipaddress.summarize_address_range(
                ipaddress.IPv4Address(num2ip(a)), ipaddress.IPv4Address(num2ip(b)))]
        except:
            pass
    return cidr_list


if __name__ == '__main__':
    pass
    # for net_str in ["8.8.8.8", "192.168.1.0/28", "192.168.4.3/27", "192.168.1.1-33", "192.168.1.5-192.168.1.8"]:
    #     print(
    #         f"func: net2ipip\tinput: {net_str}\toutput: {net2ipip(net_str,True)}")
    #     print(f"func: net2ipip\tinput: {net_str}\toutput: {net2ipip(net_str)}")
    #     print(
    #         f"func: net2cidr\tinput: {net_str}\toutput: {net2cidr(net_str,True)}")
    #     print(f"func: net2cidr\tinput: {net_str}\toutput: {net2cidr(net_str)}")
    #     print(
    #         f"func: net2ip\tinput: {net_str}\toutput: {net2ip(net_str,True)}")
    #     print(f"func: net2ip\tinput: {net_str}\toutput: {net2ip(net_str)}")
    # ip_list = ["192.168.0.11", "192.168.0.8", "192.168.0.10"]
    # print(f"func: ip2ipip\tinput: {ip_list}\toutput: {ip2ipip(ip_list)}")
    # print(f"func: ip2cidr\tinput: {ip_list}\toutput: {ip2cidr(ip_list)}")
