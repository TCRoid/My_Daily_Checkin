import requests
import time

import config

name = 'CSDN'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.75 Safari/537.36'
}


# 签到
def sign(cookies):
    url = 'https://me.csdn.net/api/LuckyDraw_v2/signIn'
    response = requests.get(url, headers=headers, cookies=cookies).json()
    if response.get("code") == 200:
        msg = response.get("data").get("msg")
    else:
        msg = "签到失败"
        print(response)
    return msg


# 抽奖
def draw(cookies):
    url = 'https://me.csdn.net/api/LuckyDraw_v2/goodluck'
    response = requests.get(url, headers=headers, cookies=cookies).json()
    if response.get("code") == 200:
        msg = response.get("data").get("msg")
    else:
        msg = "抽奖失败"
        print(response)
    return msg


def main(cookie):
    print('====== 【CSDN】开始签到 ======')
    cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie.split("; ")}
    user_name = cookies.get("UserName", "未获取到账号信息")

    sign_msg = sign(cookies)
    draw_msg = draw(cookies)
    msg = [
        {"name": "帐号信息", "value": user_name},
        {"name": "签到信息", "value": sign_msg},
        {"name": "抽奖结果", "value": draw_msg},
    ]
    msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
    print(msg)
    print('====== 【CSDN】完成签到 ======\n\n')


def start_run():
    configs = config.main(name)

    if 'dict' in str(type(configs)):
        # 单账号
        cookie = configs.get('cookie')
        main(cookie)
    else:
        # 多账号
        for config_item in configs:
            cookie = config_item.get('cookie')
            main(cookie)
            time.sleep(3)  # 等待3秒


if __name__ == '__main__':
    start_run()
