import requests
import time

import config

name = "youdao"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.75 Safari/537.36'
}


# 签到
def sign(cookies):
    ad_space = 0
    refresh_cookies_res = requests.get("http://note.youdao.com/login/acc/pe/getsess?product=YNOTE", cookies=cookies,
                                       headers=headers)
    cookies = dict(refresh_cookies_res.cookies)
    url = "https://note.youdao.com/yws/api/daupromotion?method=sync"
    res = requests.post(url=url, cookies=cookies, headers=headers)
    if "error" not in res.text:
        checkin_response = requests.post(
            url="https://note.youdao.com/yws/mapi/user?method=checkin", cookies=cookies, headers=headers
        )
        for i in range(3):
            ad_response = requests.post(
                url="https://note.youdao.com/yws/mapi/user?method=adRandomPrompt", cookies=cookies, headers=headers
            )
            ad_space += ad_response.json().get("space", 0) // 1048576
        if "reward" in res.text:
            sync_space = res.json().get("rewardSpace", 0) // 1048576
            checkin_space = checkin_response.json().get("space", 0) // 1048576
            space = sync_space + checkin_space + ad_space
            youdao_message = "+{0}M".format(space)
        else:
            youdao_message = "获取失败"
    else:
        youdao_message = "Cookie 可能过期"
    return youdao_message


def main(cookie):
    print('======【有道云笔记】开始签到======')
    youdao_cookie = {item.split("=")[0]: item.split("=")[1] for item in cookie.split("; ")}
    # print(youdao_cookie)

    try:
        ynote_pers = youdao_cookie.get("P_INFO", "")
        uid = ynote_pers.split("|")[0]
    except Exception as e:
        print(f"获取账号信息失败: {e}")
        uid = "未获取到账号信息"

    msg = sign(cookies=youdao_cookie)
    msg = [
        {"name": "帐号信息", "value": uid},
        {"name": "获取空间", "value": msg},
    ]
    msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
    print(msg)
    print('======【有道云笔记】完成签到======\n\n')


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
