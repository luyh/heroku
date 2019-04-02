#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from china_time import ChinaTime

def send_wechat(title,content):
    now = ChinaTime().getChinaTime()
    text = {'text': title, 'desp': content +'\n\n'+ now}
    try:
        response = requests.post('https://sc.ftqq.com/SCU23707T1a6b7b5527ba64588859a61ecfca18775ab65ce918f4f.send',\
                      data= text )
        print(response.content)
        print(text)
    except:
        print('发送微信报错')


if __name__ == '__main__':
    send_wechat('wechat title','微信测试内容')