import requests
import time
import re

import config

# 什么值得买 网页端签到
name = 'smzdm'
headers = {
    'Referer': 'https://www.smzdm.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
}


# 签到
def checkin(cookies):
    url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
    response = requests.get(url, cookies=cookies, headers=headers)
    # print(response.json())
    return response.json()


def main(cookie):
    print('====== 【什么值得买】开始签到 ======')
    cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie.split("; ")}

    checkin_re = checkin(cookies)
    if checkin_re['error_code'] == 0:
        slogan = re.findall(r'class=\"red\">(\d+)</span>', checkin_re['data']['slogan'])
        print('签到成功！今日已领 {0} 积分，再签到 {1} 天可领 {2} 积分'.format(slogan[0], slogan[1], slogan[2]))
        print('签到天数：' + str(checkin_re['data']['checkin_num']) + '，连续签到天数：' + str(checkin_re['data']['continue_checkin_days']))
        print('等级：' + str(checkin_re['data']['rank']) + '，经验：' + str(checkin_re['data']['exp']))
    else:
        print('签到失败：' + checkin_re['error_msg'])
    print('====== 【什么值得买】完成签到 ======\n\n')


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
