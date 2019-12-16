# -*- coding: utf-8 -*-
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}


def open_url(target_url, retries=3, cookies=''):
    """
    读取URL
    :param target_url: 目标URL
    :param retries: 最大重试次数
    :param cookies: Cookies信息
    :return:
    """
    header['Cookie'] = cookies
    for i in range(retries):
        proxy = get_proxy()
        response = requests.get(target_url, headers=header, proxies=proxy)
        if response.status_code == 200:
            doc = response.content.decode('utf-8')
            return doc
        print("Error when request the Url:{0},retries {1}".format(target_url, i))


def get_proxy():
    return ""
