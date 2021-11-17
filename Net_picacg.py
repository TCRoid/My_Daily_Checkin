# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import random
import string
import time
import requests

import config

name = "picacg"


def generate_headers(path, data=None, token=None):
    api_key = "C69BAF41DA5ABD1FFEDC6D2FEA56B"
    api_secret = "~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn"
    headers = {
        "api-key": api_key,
        "accept": "application/vnd.picacomic.com.v1+json",
        "app-channel": "2",
        "app-version": "2.2.1.2.3.3",
        "app-uuid": "defaultUuid",
        "app-platform": "android",
        "app-build-version": "44",
        "User-Agent": "okhttp/3.8.1",
        "image-quality": "original",
    }
    current_time = str(int(time.time()))
    nonce = "".join(random.choices(string.ascii_lowercase + string.digits, k=32))
    raw = path + current_time + nonce + "POST" + api_key
    raw = raw.lower()
    h = hmac.new(api_secret.encode(), digestmod=hashlib.sha256)
    h.update(raw.encode())
    signature = h.hexdigest()
    headers["time"] = current_time
    headers["nonce"] = nonce
    headers["signature"] = signature
    if data is not None:
        headers["Content-Type"] = "application/json; charset=UTF-8"
    if token is not None:
        headers["authorization"] = token
    return headers


def sign(email, password):
    try:
        data = {"email": email, "password": password}
        sign_headers = generate_headers(path="auth/sign-in", data=data)
        sign_response = requests.post(
            url="https://picaapi.picacomic.com/auth/sign-in",
            data=json.dumps(data),
            headers=sign_headers,
            timeout=60,
        ).json()
        token = sign_response.get("data", {}).get("token")
        punch_headers = generate_headers(path="users/punch-in", token=token)
        response = requests.post(
            url="https://picaapi.picacomic.com/users/punch-in", headers=punch_headers, timeout=60
        ).json()
        if response.get("data", {}).get("res", {}).get("status", {}) == "ok":
            msg = "打卡成功"
        else:
            msg = "重复签到"
    except Exception as e:
        msg = str(e)
    return msg


def main(email, password):
    print('====== 【PicACG】开始签到 ======')
    sign_msg = sign(email=email, password=password)
    msg = [
        {"name": "帐号信息", "value": f"{email}"},
        {"name": "签到信息", "value": f"{sign_msg}"},
    ]
    msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
    print(msg)
    print('====== 【PicACG】完成签到 ======\n\n')


def start_run():
    configs = config.main(name)

    if 'dict' in str(type(configs)):
        # 单账号
        username = configs.get('username')
        password = configs.get('password')
        # print(username,password)
        main(username, password)
    else:
        # 多账号
        for config_item in configs:
            username = config_item.get('username')
            password = config_item.get('password')
            # print(username,password)
            main(username, password)
            time.sleep(3)  # 等待3秒


if __name__ == '__main__':
    start_run()
