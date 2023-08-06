#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import re
import json
import requests

requests.packages.urllib3.disable_warnings()

class RSASClient:

    def __init__(self, url, username, password):

        self.url = url
        self.username = username
        self.password = password
        self.headers = {"Referer": url}
        self.session = requests.session()

    def login(self):
        self.connect('GET', '/accounts/login/')
        csrftoken = self.session.cookies.get('csrftoken', 'None')
        data = {"username": self.username, "password": self.password, "csrfmiddlewaretoken": csrftoken}
        rc, _, _ = self.connect('POST', '/accounts/login_view/', data)
        if rc == 302:
            print('[+] 登录成功')
        else:
            print('[-] 登录失败')

    def connect(self, method, resource, data=None):
        if method == 'GET':
            r = self.session.get('{0}{1}'.format(
                self.url, resource), data=data, headers=self.headers, verify=False, allow_redirects=False)
        elif method == 'POST':
            r = self.session.post('{0}{1}'.format(
                self.url, resource), data=data, headers=self.headers, verify=False, allow_redirects=False)
        r.encoding = r.apparent_encoding
        try:
            return r.status_code, r.headers, r.json()
        except:
            if 'text' in r.headers.get('Content-Type', ''):
                return r.status_code, r.headers, r.text
            else:
                return r.status_code, r.headers, r.content

    def create_task(self, name, ip_list):
        '''新建任务'''
        data = {
            'csrfmiddlewaretoken': self.session.cookies.get('csrftoken', 'None'),
            'vul_or_pwd': 'vul',
            'config_task': 'taskname',
            'task_config': '',
            'diff': 'writesomething',
            'target': 'ip',
            'ipList': ",".join(ip_list),
            'domainList': '',
            'name': name,
            'exec': 'immediate',
            'exec_timing_date': '',
            'exec_everyday_time': '00: 00',
            'exec_everyweek_day': '1',
            'exec_everyweek_time': '00: 00',
            'exec_emonthdate_day': '1',
            'exec_emonthdate_time': '00: 00',
            'exec_emonthweek_pre': '1',
            'exec_emonthweek_day': '1',
            'exec_emonthweek_time': '00: 00',
            'tpl': '0',
            'login_check_type': 'login_check_type_vul',
            'isguesspwd': 'yes',
            'exec_range': '',
            'scan_pri': '2',
            'taskdesc': '',
            'comment_1': '任务报表导出配置',
            'report_type_html': 'html',
            'report_type_xls': 'xls',
            'report_type_xml': 'xml',
            'report_content_sum': 'sum',
            'report_content_host': 'host',
            'report_tpl_sum': '1',
            'report_tpl_host': '101',
            'report_ifcreate': 'yes',
            'report_ifsent_type': 'html',
            'report_ifsent_email': '',
            'port_strategy_userports': '1-100,443,445',
            'port_strategy': 'allports',
            'port_speed': '3',
            'port_tcp': 'T',
            'scan_level': '3',
            'timeout_plugins': '40',
            'timeout_read': '15',
            'alert_msg': '远程安全评估系统将对您的主机进行安全评估。',
            'srv_vul_detect': 'yes',
            'scan_oracle': 'yes',
            'encoding': 'GBK',
            'bvs_task': 'no',
            'pwd_smb': 'yes',
            'pwd_type_smb': 'c',
            'pwd_user_smb': 'smb_user.default',
            'pwd_pass_smb': 'smb_pass.default',
            'pwd_userpass_smb': 'smb_userpass.default',
            'pwd_rdp': 'yes',
            'pwd_type_rdp': 'c',
            'pwd_user_rdp': 'rdp_user.default',
            'pwd_pass_rdp': 'rdp_pass.default',
            'pwd_userpass_rdp': 'rdp_userpass.default',
            'pwd_telnet': 'yes',
            'pwd_type_telnet': 'c',
            'pwd_user_telnet': 'telnet_user.default',
            'pwd_pass_telnet': 'telnet_pass.default',
            'pwd_userpass_telnet': 'telnet_userpass.default',
            'pwd_ftp': 'yes',
            'pwd_type_ftp': 'c',
            'pwd_user_ftp': 'ftp_user.default',
            'pwd_pass_ftp': 'ftp_pass.default',
            'pwd_userpass_ftp': 'ftp_userpass.default',
            'pwd_sftp': 'yes', 'pwd_type_sftp': 'c',
            'pwd_user_sftp': 'sftp_user.default',
            'pwd_pass_sftp': 'sftp_pass.default',
            'pwd_userpass_sftp': 'sftp_userpass.default',
            'pwd_ssh': 'yes', 'pwd_type_ssh': 'c',
            'pwd_user_ssh': 'ssh_user.default',
            'pwd_pass_ssh': 'ssh_pass.default',
            'pwd_userpass_ssh': 'ssh_userpass.default',
            'pwd_activemq': 'yes',
            'pwd_type_activemq': 'c',
            'pwd_user_activemq': 'activemq_user.default',
            'pwd_pass_activemq': 'activemq_pass.default',
            'pwd_userpass_activemq': 'activemq_userpass.default',
            'pwd_pop3': 'yes', 'pwd_type_pop3': 'c',
            'pwd_user_pop3': 'pop3_user.default',
            'pwd_pass_pop3': 'pop3_pass.default',
            'pwd_userpass_pop3': 'pop3_userpass.default',
            'pwd_tomcat': 'yes',
            'pwd_type_tomcat': 'c',
            'pwd_user_tomcat': 'tomcat_user.default',
            'pwd_pass_tomcat': 'tomcat_pass.default',
            'pwd_userpass_tomcat': 'tomcat_userpass.default',
            'pwd_mssql': 'yes', 'pwd_type_mssql': 'c',
            'pwd_user_mssql': 'mssql_user.default',
            'pwd_pass_mssql': 'mssql_pass.default',
            'pwd_userpass_mssql': 'mssql_userpass.default',
            'pwd_mysql': 'yes',
            'pwd_type_mysql': 'c',
            'pwd_user_mysql': 'mysql_user.default',
            'pwd_pass_mysql': 'mysql_pass.default',
            'pwd_userpass_mysql': 'mysql_userpass.default',
            'pwd_oracle': 'yes',
            'pwd_type_oracle': 'c',
            'pwd_user_oracle': 'oracle_user.default',
            'pwd_pass_oracle': 'oracle_pass.default',
            'pwd_userpass_oracle': 'oracle_userpass.default',
            'pwd_sybase': 'yes',
            'pwd_type_sybase': 'c',
            'pwd_user_sybase': 'sybase_user.default',
            'pwd_pass_sybase': 'sybase_pass.default',
            'pwd_userpass_sybase': 'sybase_userpass.default',
            'pwd_db2': 'yes', 'pwd_type_db2': 'c',
            'pwd_user_db2': 'db2_user.default',
            'pwd_pass_db2': 'db2_pass.default',
            'pwd_userpass_db2': 'db2_userpass.default',
            'pwd_mongodb': 'yes',
            'pwd_type_mongodb': 'c',
            'pwd_user_mongodb': 'mongodb_user.default',
            'pwd_pass_mongodb': 'mongodb_pass.default',
            'pwd_userpass_mongodb': 'db2_userpass.default',
            'pwd_smtp': 'yes',
            'pwd_type_smtp': 'c',
            'pwd_user_smtp': 'smtp_user.default',
            'pwd_pass_smtp': 'smtp_pass.default',
            'pwd_userpass_smtp': 'smtp_userpass.default',
            'pwd_imap': 'yes',
            'pwd_type_imap': 'c',
            'pwd_user_imap': 'imap_user.default',
            'pwd_pass_imap': 'imap_pass.default',
            'pwd_userpass_imap': 'imap_userpass.default',
            'pwd_onvif': 'yes',
            'pwd_type_onvif': 'c',
            'pwd_user_onvif': 'onvif_user.default',
            'pwd_pass_onvif': 'onvif_pass.default',
            'pwd_userpass_onvif': 'onvif_userpass.default',
            'pwd_rtsp': 'yes', 'pwd_type_rtsp': 'c',
            'pwd_user_rtsp': 'rtsp_user.default',
            'pwd_pass_rtsp': 'rtsp_pass.default',
            'pwd_userpass_rtsp': 'rtsp_userpass.default',
            'pwd_rtsp_url': '',
            'pwd_redis': 'yes',
            'pwd_pass_redis': 'redis_pass.default',
            'pwd_snmp': 'yes',
            'pwd_pass_snmp': 'snmp_pass.default',
            'pwd_timeout': '10',
            'pwd_timeout_time': '120',
            'pwd_interval': '0',
            'pwd_num': '0',
            'pwd_threadnum': '5',
            'loginarray': [
                {
                    'ip_range': '192.168.1.255',
                    'admin_id': '',
                    'protocol': '',
                    'port': '',
                    'os': '',
                    'user_name': '',
                    'user_pwd': '',
                    'ostpls': [],
                    'apptpls': [],
                    'dbtpls': [],
                    'virttpls': [],
                    'devtpls': [],
                    'statustpls': '',
                    'tpl_industry': '',
                    'tpllist': [],
                    'tpllistlen': 0,
                    'jhosts': [],
                    'tpltype': '',
                    'protect': '',
                    'protect_level': '',
                    'jump_ifuse': '',
                    'host_ifsave': '',
                    'oracle_ifuse': '',
                    'ora_username': '',
                    'ora_userpwd': '',
                    'ora_port': '',
                    'ora_usersid': '',
                    'weblogic_ifuse': '',
                    'weblogic_system': '',
                    'weblogic_version': '',
                    'weblogic_user': '',
                    'weblogic_path': ''
                }
            ]
        }
        _,_, rs = self.connect('POST', '/task/vul/tasksubmit', data)
        print('[+] 创建任务成功',rs)
        return rs[8:]

    def task_process(self, task_list):
        '''任务进度'''
        self.headers['X-Csrftoken'] = self.session.cookies.get(
            'csrftoken', 'None')
        data = {'ids': ';{};'.format(';'.join(task_list))}
        _, _, rs = self.connect('POST', '/list/setProcess/', data)
        return rs

    def create_report(self, task_list):
        '''创建报表'''
        data = [
            ('csrfmiddlewaretoken', self.session.cookies.get('csrftoken', 'None')),
            ('export_area', 'sys'),
            ('report_type', 'html'),
            ('report_type', 'xls'),
            ('report_type', 'xml'),
            ('report_content', 'summary'),
            ('summary_template_id', '1'),
            ('summary_report_title', '绿盟科技"远程安全评估系统"安全评估报告'),
            ('report_content', 'host'),
            ('host_template_id', '101'),
            ('single_report_title', '绿盟科技"远程安全评估系统"安全评估报告-主机报表'),
            ('multi_export_type', 'multi_batch'),
            ('multi_report_name', '多任务输出'),
            ('single_task_report_name', ''),
            ('from', 'report_export'),
            ('task_id', ','.join(task_list))]
        _, _, rs = self.connect('POST', '/report/export', data)
        report_id = json.loads(rs.lstrip('(').rstrip(')'))[
            'context']['report_id']
        print('[+] 创建报表成功',report_id)
        return report_id

    def report_process(self, report_id):
        '''报表进度'''
        _, _, rs = self.connect('GET', '/report/export/process_info/id/{}'.format(report_id))
        progress = json.loads(rs.lstrip('(').rstrip(')'))[
            'context']['progress']
        return progress

    def download_report(self, path, report_id, report_type='xls'):
        '''下载报表'''
        _, rh, rs = self.connect('GET', '/report/download/id/{}/type/{}/'.format(report_id, report_type))
        filename = re.findall('attachment; filename="(.*?)"',rh.get('Content-Disposition', ''))[0].encode('ISO-8859-1').decode('gbk')
        if not os.path.exists(path):
            os.makedirs(path)
        print('[+] 下载报表',filename)
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(rs)

    def system_info(self):
        '''系统信息'''
        _, _, rs = self.connect('GET', '/system/getInfo/')
        return rs

    def current_task_num(self):
        '''当前任务数'''
        _, _, rs = self.connect('GET', '/system/get_task_num/')
        return rs

    def total_task_num(self):
        '''当前任务数'''
        _, _, rs = self.connect('GET', '/list/')
        s = re.findall(r'共(\d+)条',rs)
        return s[0] if s else 0

