#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import requests
from requests.adapters import HTTPAdapter
requests.packages.urllib3.disable_warnings()
# 添加自动重试
requests = requests.Session()
requests.mount('http://', HTTPAdapter(max_retries=3))
requests.mount('https://', HTTPAdapter(max_retries=3))

class AWVSClient:

    def __init__(self, url, api_key):

        self.url = url
        self.headers = {'X-Auth': api_key, 'Content-Type': 'application/json'}

    def connect(self, method, resource, data=None):
        print('[{}] {}'.format(method,resource))
        if data:
            data = json.dumps(data)
        r = getattr(requests, method.lower())('{0}{1}'.format(
            self.url, resource), data=data, headers=self.headers, timeout=20, verify=False)
        r.encoding = r.apparent_encoding
        try:
            return r.status_code, r.headers, r.json()
        except:
            if 'text' in r.headers.get('Content-Type', ''):
                return r.status_code, r.headers, r.text
            else:
                return r.status_code, r.headers, r.content

    def get_targets(self):
        '''获取所有目标'''
        c = 0
        while True:
            _, _, rs = self.connect(
                'GET', '/api/v1/targets?c={}&l=100'.format(c*100))
            c += 1
            if not len(rs["targets"]):
                break
            for s in rs["targets"]:
                yield s['target_id'], s['address']

    def add_target(self, url):
        '''添加目标'''
        data = {"address": url, "description": url, "criticality": "10"}
        _, _, rs = self.connect('POST', '/api/v1/targets', data)
        return rs['target_id']

    def del_target(self, target_id):
        '''删除目标'''
        rc, _, _ = self.connect(
            'DELETE', '/api/v1/targets/{}'.format(target_id))
        return True if rc == 204 else False

    def add_scan(self, target_id, rule='full'):
        '''添加扫描'''
        rules = {
            "full": "11111111-1111-1111-1111-111111111111",
            "highrisk": "11111111-1111-1111-1111-111111111112",
            "XSS": "11111111-1111-1111-1111-111111111116",
            "SQL": "11111111-1111-1111-1111-111111111113",
            "Weakpass": "11111111-1111-1111-1111-111111111115",
            "crawlonly": "11111111-1111-1111-1111-111111111117"
        }
        data = {'target_id': target_id, 'profile_id': rules[rule], 'schedule': {
            'disable': False, 'start_date': None, 'time_sensitive': False}}
        rc, _, _ = self.connect('POST', '/api/v1/scans', data)
        return True if rc == 201 else False

    def get_scans(self):
        '''获取所有扫描'''
        c = 0
        while True:
            _, _, rs = self.connect(
                'GET', '/api/v1/scans?c={}&l=100&q=threat:1,2,3;&s=target_address:desc'.format(c*100))
            c += 1
            if not len(rs["scans"]):
                break
            for s in rs["scans"]:
                yield s['scan_id'], s['current_session']['scan_session_id'],s['current_session']['severity_counts'] 

    def get_vulns(self, scan_id, scan_session_id):
        '''获取漏洞id'''
        c = 0
        while True:
            _, _, rs = self.connect(
                'GET', '/api/v1/scans/{}/results/{}/vulnerabilities?c={}'.format(scan_id, scan_session_id, c*100))
            c += 1
            if not len(rs["vulnerabilities"]):
                break
            for s in rs["vulnerabilities"]:
                yield s['vuln_id']

    def get_vuln_details(self, scan_id, scan_session_id, vuln_id):
        '''获取漏洞详情'''
        vuln = {}
        _, _, rs = self.connect(
            'GET', '/api/v1/scans/{}/results/{}/vulnerabilities/{}'.format(scan_id, scan_session_id, vuln_id)) 
        vuln['affects_url'] =rs.get('affects_url','')
        vuln['target_description'] =rs.get('target_description','')
        vuln['vt_name'] = rs.get('vt_name','') 
        vuln['severity'] = rs.get('severity','') 
        vuln['description'] = rs.get('description','') 
        vuln['impact'] = rs.get('impact','') 
        vuln['recommendation'] = rs.get('recommendation','') 
        vuln['details'] = rs.get('details','') 
        vuln['recommendation'] = rs.get('recommendation','') 
        vuln['request'] = rs.get('request','') 
        return vuln

    def get_vuln_http_response(self, scan_id, scan_session_id, vuln_id):
        '''获取漏洞详情'''
        _, _, rs = self.connect(
            'GET', '/api/v1/scans/{}/results/{}/vulnerabilities/{}/http_response'.format(scan_id, scan_session_id, vuln_id))
        return rs

if __name__ == '__main__':
    url = 'https://127.0.0.1:3443'
    api_key = '1986ad8c0a5b3df4d7028d5f3c06e936c09b72504c2714a7c934c1247cd7be59c'

    awvs = AWVSClient(url, api_key)

    # 导出漏洞清单
    # vulns = []
    # from mylib import jsonlist2xlsx
    # for scan_id,scan_session_id,severity_counts in awvs.get_scans():
    #     if sum([severity_counts[i] for i in ['high','medium','low','info']]) == 0:continue
    #     for vuln_id in awvs.get_vulns(scan_id, scan_session_id):
    #         vuln = awvs.get_vuln_details(scan_id, scan_session_id, vuln_id)
    #         vuln['http_response'] = awvs.get_vuln_http_response(scan_id, scan_session_id, vuln_id)
    #         vulns.append(vuln)
    # jsonlist2xlsx('vuln.xlsx',vuln=vulns)

    

