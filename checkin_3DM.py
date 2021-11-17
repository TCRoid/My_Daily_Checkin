import requests
import time

import config

name = '3DM'
username = ''
password = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}


# 登录
def login():
    url = 'https://my.3dmgame.com/api/login'
    data = {
        'username': username,
        'passwd': password,
        'autologin': 0
    }
    response = requests.post(url, data, headers=headers)
    return response


# 获取cookies
def get_cookie(response):
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    return cookies


# 签到
def checkin(cookies):
    url = 'https://my.3dmgame.com/api/subsign'
    response = requests.post(url, cookies=cookies, headers=headers)
    return response


# 登出
def logout(cookies):
    url = 'https://my.3dmgame.com/api/logout'
    response = requests.post(url, cookies=cookies, headers=headers)
    return response


def main():
    print('====== 【3DMGAME】开始签到 ======')
    login_re = login()
    if login_re.json()['code'] == 1:
        ck = get_cookie(login_re)
        # print(ck)
        print('登录成功：' + login_re.json()['user']['nickname'])

        time.sleep(3)  # 等待3秒
        checkin_re = checkin(ck)
        if checkin_re.json()['code'] == 1:
            print('签到成功：' + checkin_re.json()['data']['integralmsg'])
        else:
            print('签到失败：' + checkin_re.json()['msg'])

        time.sleep(3)  # 等待3秒
        logout_re = logout(ck)
        if logout_re.json()['code'] == 1:
            print('账号已登出')
    else:
        print('登录失败：' + login_re.json()['msg'])
    print('====== 【3DMGAME】完成签到 ======\n\n')


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
