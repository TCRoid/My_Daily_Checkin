import requests
import time

import config

name = 'huluxia'
headers = {
    'User-Agent': 'okhttp/3.8.1',
    'Accept-Encoding': 'gzip'
}
phone_brand_type = 'HW'  # 手机品牌
cat_ids = ["6", "1", "58", "3", "56", "45", "4", "70", "111", "96", "44", "16", "81", "43", "2", "77", "108", "82",
           "98", "92", "57", "76", "107", "29", "23", "22", "21", "116", "113", "63", "115", "11", "88", "101", "112",
           "90", "103", "110", "105", "71"]


# 签到
def checkin(key, device_code, user_id, cat_id):
    url = 'http://floor.huluxia.com/user/signin/check/ANDROID/2.0?user_id=' + user_id + '&cat_id=' + cat_id + '&platform=2&gkey=000000&app_version=4.1.0.6&versioncode=20141455&market_id=floor_web&_key=' + key + '&device_code=' + device_code + '&phone_brand_type=' + phone_brand_type
    response = requests.get(url, headers=headers)
    # print(response.json())
    return response


# 获取签到信息
def check_info(key, device_code, cat_id):
    url = 'http://floor.huluxia.com/user/signin/ANDROID/4.0?platform=2&gkey=000000&app_version=4.1.0.6&versioncode=20141455&market_id=floor_web&_key=' + key + '&device_code=' + device_code + '&phone_brand_type=' + phone_brand_type + '&cat_id=' + cat_id
    response = requests.get(url, headers=headers)
    # print(response.json())
    return response


# 获取用户信息
def user_info(key, device_code, user_id):
    url = 'http://floor.huluxia.com/user/info/ANDROID/2.1?platform=2&gkey=000000&app_version=4.1.0.6&versioncode=20141455&market_id=floor_web&_key=' + key + '&device_code=' + device_code + '&phone_brand_type=' + phone_brand_type + '&user_id=' + user_id
    response = requests.get(url, headers=headers)
    # print(response.json())
    return response


def main(key, device_code, user_id):
    print('====== 【葫芦侠三楼】开始签到 ======')
    for cat_id in cat_ids:
        checkin_re = checkin(key, device_code, user_id, cat_id)
        if checkin_re.json()['status'] == 1:

            if checkin_re.json()['signin'] == 1:
                print('版块ID：' + cat_id + '	已经签到了')
                print('连续签到天数：' + str(checkin_re.json()['continueDays']) + '\n\n')
            else:
                check_info_re = check_info(key, device_code, cat_id)
                if check_info_re.json()['signin'] == 1:
                    print('版块ID：' + cat_id + '	签到成功')
                    print('获得经验：' + str(check_info_re.json()['experienceVal']) + '，连续签到天数：' + str(
                        check_info_re.json()['continueDays']) + '\n\n')
                else:
                    print('出错')
                    print(check_info_re.json())

        else:
            print('出错')
            print(checkin_re.json())

        time.sleep(1)  # 等待1秒

    # 获取用户信息
    user_info_re = user_info(key, device_code, user_id)
    if user_info_re.json()['status'] == 1:
        print('用户昵称：' + user_info_re.json()['nick'])
        print('等级：' + str(user_info_re.json()['level']) + '	经验：' + str(user_info_re.json()['exp']) + '/' + str(
            user_info_re.json()['nextExp']))
    else:
        print('出错')
        print(user_info_re.json())

    print('====== 【葫芦侠三楼】完成签到 ======\n\n')


def start_run():
    configs = config.main(name)

    if 'dict' in str(type(configs)):
        # 单账号
        key = configs.get('key')
        device_code = configs.get('device_code')
        user_id = configs.get('user_id')
        main(key, device_code, user_id)
    else:
        # 多账号
        for config_item in configs:
            key = config_item.get('key')
            device_code = configs.get('device_code')
            user_id = configs.get('user_id')
            main(key, device_code, user_id)
            time.sleep(3)  # 等待3秒


if __name__ == '__main__':
    start_run()
