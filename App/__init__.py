from flask import Flask
import importlib
import sys
import os
import logging
import logging.config
import yaml

importlib.reload(sys)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def create_app(conf_name=None, conf_path=None):
    app = Flask(__name__)
    if not conf_path:
        pwd = os.getcwd()
        conf_path = os.path.join(pwd, 'config/config.yaml')
    if not conf_name:
        conf_name = 'PRODUCTION'
    conf = read_yaml(conf_name, conf_path)
    app.config.update(conf)
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
        logging.config.dictConfig(dict_conf)  # 载入日志配置
    return app


def read_yaml(conf_name, conf_path):
    if conf_name and conf_path:
        with open(conf_path, "r", encoding="utf-8") as f:
            conf = yaml.safe_load(f.read())
            if conf_name in conf.keys():
                return conf[conf_name.upper()]
            else:
                raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError("请输入正确的配置路径或配置名称")


app = create_app(conf_name="DEVELOPMENT")
