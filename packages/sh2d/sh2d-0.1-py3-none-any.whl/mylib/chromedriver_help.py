#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import requests
import winreg
import zipfile


def get_chrome_version():
    '''获取本地chrome版本'''
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    return version


def get_server_chrome_versions():
    '''获取chrome版本列表'''
    versionList = []
    url = "https://registry.npmmirror.com/-/binary/chromedriver/"
    rep = requests.get(url).json()
    for item in rep:
        versionList.append(item["name"])
    return versionList


def download_driver(download_url):
    '''下载chromedriver.zip文件'''
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print("[+] chromedriver下载成功")


def get_version(file_path):
    '''查询当前Chromedriver版本'''
    outstd2 = os.popen(os.path.join(
        file_path, "chromedriver.exe") + '  --version').read()
    return outstd2.split(' ')[1]


def unzip_driver(path):
    '''解压Chromedriver压缩包到指定目录'''
    f = zipfile.ZipFile("chromedriver.zip", 'r')
    for file in f.namelist():
        f.extract(file, path)


def update_chromedriver(file_path):
    '''检查并更新chromedriver版本'''
    url = 'http://npm.taobao.org/mirrors/chromedriver/'
    chromeVersion = get_chrome_version()
    chrome_main_version = int(chromeVersion.split(".")[0])  # chrome主版本号
    driver_main_version = ''
    if os.path.exists(os.path.join(file_path, "chromedriver.exe")):
        driverVersion = get_version(file_path)
        driver_main_version = int(driverVersion.split(".")[
                                  0])  # chromedriver主版本号
    download_url = ""
    if driver_main_version != chrome_main_version:
        print("[+] chromedriver版本与chrome浏览器不兼容，更新中>>>")
        versionList = get_server_chrome_versions()
        if chromeVersion in versionList:
            download_url = "{}{}/chromedriver_win32.zip".format(url,chromeVersion)
        else:
            for version in versionList:
                if version.startswith(str(chrome_main_version)):
                    download_url = "{}{}/chromedriver_win32.zip".format(url,version)
                    break
            if download_url == "":
                print(
                    "[-] 未找到兼容的chromedriver版本，请在http://npm.taobao.org/mirrors/chromedriver/ 核实。")

        download_driver(download_url=download_url)
        path = file_path
        unzip_driver(path)
        os.remove("chromedriver.zip")
        print('[+] 更新后的Chromedriver版本为：', get_version(file_path))
    else:
        print("[+] chromedriver版本兼容，无需更新！")
    return os.path.join(file_path, "chromedriver.exe")


if __name__ == "__main__":
    file_path = "D:\\Temp"
    print(update_chromedriver(file_path))
