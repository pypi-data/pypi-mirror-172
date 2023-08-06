#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import requests
import time
requests.packages.urllib3.disable_warnings()


class NessusClient:

    def __init__(self, url, accessKey, secretKey):

        self.url = url
        self.headers = {'X-ApiKeys': 'accessKey={}; secretKey={};'.format(
            accessKey, secretKey), 'Content-Type': 'application/json', }

    def connect(self, method, resource, data=None):
        if data:
            data = json.dumps(data)
        r = getattr(requests, method.lower())('{0}{1}'.format(
            self.url, resource), data=data, headers=self.headers, verify=False)
        if r.status_code != 200:
            print(resource, data, r.text)
        else:
            try:
                return r.json()
            except:
                return r.text

    def get_policies(self):
        '''获取所有策略模板'''
        data = self.connect('GET', '/editor/policy/templates')
        return dict((p['title'], p['uuid']) for p in data['templates'])

    def add_scan(self, name, targets, pid):
        '''创建任务'''
        scan_data = {"uuid": pid, "settings": {
            "discovery_mode": "Port scan (all ports)", 'name': name, "text_targets": targets, }}
        data = self.connect('POST', '/scans', scan_data)
        return data["scan"]

    def launch(self, sid):
        '''启动扫描'''
        data = self.connect('POST', '/scans/{}/launch'.format(sid))
        return data["scan_uuid"]

    def get_scans(self):
        '''当前任务'''
        data = self.connect('GET', '/scans?folder_id=3')
        return [[i['name'],i['status'],time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i['last_modification_date']))] for i in data['scans']]

if __name__ == '__main__':
    url = 'https://127.0.0.1:8834'
    accessKey = '71cf45723e00ddad07c226ce31047d6e18d9db9d9b3d3ebe5d81db02bfc19bd7'
    secretKey = '42035d11f2aea714b255d14a95dfe6f3cf76e79762abbe81921c67555d7815a7'

    nessus = NessusClient(url, accessKey, secretKey)
    # policies = nessus.get_policies()
    # scan_data = nessus.add_scan("test", "192.168.1.1",
    #                             policies['Basic Network Scan'])

    # print(nessus.launch(scan_data['id']))
    data = nessus.get_scans()
    print(data)
