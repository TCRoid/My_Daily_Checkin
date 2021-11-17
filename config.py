import os
import json


# 读取配置文件
def load_config():
    base_path = os.path.abspath(os.path.dirname(__file__))
    # print(base_path)
    config_path = os.path.join(base_path, 'config', 'config.json')
    # print(config_path)
    if not os.path.exists(config_path):
        print('配置文件不存在')
        return 0
    else:
        with open(config_path) as config_file:
            configs = config_file.read()

        # print(configs)
        return configs


def main(checkin_item):
    configs = load_config()
    if not configs == 0:
        configs = json.loads(configs)
        config_item = configs.get(checkin_item)
        # print(config_item)
        return config_item
