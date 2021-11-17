import requests
import time
import re

import config

name = 'jlwz'
username = ''
password = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}


# 登录
def login():
    url = 'https://jlwz.cn/waplogin.aspx'
    data = {
        'logname': username,
        'logpass': password,
        'action': 'login',
        'classid': '0',
        'siteid': '1000',
        'sid': '-2-0-0-0-0-480'
    }
    response = requests.post(url, data, headers=headers)
    return response


# 获取cookies
def get_cookie(response):
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    return cookies


# 签到
def checkin(cookies):
    url = 'https://jlwz.cn/Signin/Signin.aspx?Action=index&Mod=Signin&siteid=1000'
    response = requests.post(url, cookies=cookies, headers=headers)
    return response


# 登出
def logout(cookies):
    url = 'https://jlwz.cn/waplogout.aspx?siteid=1000&isGO=OK'
    response = requests.get(url, cookies=cookies, headers=headers, allow_redirects=True)
    return response


def main():
    print('====== 【机领网】开始签到 ======')
    login_re = login()
    if '成功' in login_re.text:
        print('登录成功')
        ck = get_cookie(login_re)
        # print(ck)

        time.sleep(3)  # 等待3秒
        checkin_re = checkin(ck)
        checkin_m1 = re.findall(r'class="tip">(.*)</div><div class="content">', checkin_re.text)
        checkin_m2 = re.findall(r'class="content">(.*)<form name="f"', checkin_re.text)
        msg = checkin_m1[0] + '\n' + checkin_m2[0].replace('<br/>', '\n')
        if '经过计算' in checkin_re.text:
            print('签到成功：' + msg)
        else:
            print('签到失败：' + msg)

        time.sleep(3)  # 等待3秒
        logout_re = logout(ck)
        if '点击此重新登录你的帐号' in logout_re.text:
            print('账号已登出')
    else:
        print('登录失败')

    print('====== 【机领网】完成签到 ======\n\n')


def start_run():
    global username
    global password
    configs = config.main(name)

    if 'dict' in str(type(configs)):
        # 单账号
        username = configs.get('username')
        password = configs.get('password')
        # print(username,password)
        main()
    else:
        # 多账号
        for config_item in configs:
            username = config_item.get('username')
            password = config_item.get('password')
            # print(username,password)
            main()
            time.sleep(3)  # 等待3秒


if __name__ == '__main__':
    start_run()
