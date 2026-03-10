import logging
import os
from configparser import ConfigParser

from .napcat import push_napcat
from .pushplus import push_pushplus
from .qmsg import push_qmsg
from .serverchan3 import push_serverchan3

# 定义可用的推送服务及其对应的函数
__available_pusher = {
    'serverchan3': push_serverchan3,
    'pushplus': push_pushplus,
    'QMSG': push_qmsg,
    'napcat': push_napcat,
}


def load_config_to_env():
    # 从config.ini文件加载配置到环境变量
    config = ConfigParser()

    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    if os.path.exists(config_path):
        config.read(config_path, encoding='utf-8')

        # 遍历配置文件中的所有section（节）和option（键），添加到环境变量
        for section_name in config.sections():
            for option in config.options(section_name):
                value = config.get(section_name, option)  # 值
                # 将配置项添加到环境变量中
                env_key = option.upper()  # 转换为大写作为环境变量名
                if value:  # 只有当值不为空时才设置环境变量
                    os.environ[env_key] = value


# 加载配置到环境变量
load_config_to_env()


# 推送结果
def push(all_logs):
    if isinstance(all_logs, str):
        all_logs = [all_logs]

    for k, v in __available_pusher.items():
        try:
            v(all_logs)
        except Exception as e:
            print(f"[Push] {k}时出现问题: {str(e)}")
    logging.info("推送结束")

