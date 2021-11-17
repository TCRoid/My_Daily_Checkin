import requests
import time
import re

import config

name = 'mt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PCT-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.75 Mobile Safari/537.36',
    "Referer": "https://bbs.binmt.cc/member.php?mod=logging&action=login&mobile=2"
}


# 获取cookies
def get_cookie(cookie):
    cookieDict = {}
    cookies = cookie.split("; ")
    for co in cookies:
        co = co.strip()
        p = co.split('=')
        value = co.replace(p[0] + '=', '').replace('"', '')
        cookieDict[p[0]] = value
    return cookieDict


def get_formhash(cookies):
    url = 'https://bbs.binmt.cc/k_misign-sign.html'
    response = requests.get(url, cookies=cookies, headers=headers)
    # print(response.text)
    return response


# 签到
def checkin(formhash, cookies):
    url = 'https://bbs.binmt.cc/k_misign-sign.html?operation=qiandao&format=button&formhash=' + formhash + '&inajax=1&ajaxtarget=midaben_sign'
    response = requests.post(url, cookies=cookies, headers=headers)
    return response


def main(cookies):
    print('======【MT论坛】开始签到======')
    formhash_re = get_formhash(cookies)
    formhash = re.findall(r'formhash=(.+?)&', formhash_re.text)
    # print(formhash)

    if len(formhash) > 0 and '登录' not in formhash_re.text:
        checkin_re = checkin(formhash[0], cookies)
        # print(checkin_re.text)

        if '今日已签' in checkin_re.text:
            print('今天已经签到了')
        elif '签到成功' in checkin_re.text:
            coin_get = re.findall(r'获得.*。', checkin_re.text)
            days_all = re.findall(r'已累计.*天', checkin_re.text)
            days_ing = re.findall(r'连续.*天', checkin_re.text)
            print('签到成功：' + coin_get[0] + '\n' + days_ing[0] + '\n' + days_all[0])
        else:
            print('签到失败')
            print(checkin_re.text)

    else:
        print('cookie失效')
    print('======【MT论坛】完成签到======\n\n')


def start_run():
    configs = config.main(name)

    if 'dict' in str(type(configs)):
        # 单账号
        cookie = configs.get('cookie')
        # print(get_cookie(cookie))
        main(get_cookie(cookie))
    else:
        # 多账号
        for config_item in configs:
            cookie = config_item.get('cookie')
            main(get_cookie(cookie))
            time.sleep(3)  # 等待3秒


if __name__ == '__main__':
    start_run()
