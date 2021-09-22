#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan

from tool.atp import ATP

ENV = 'Test5'
SYSTEM_TYPE = None
GLOBAL_DATA = ATP.get_global_data(ENV, SYSTEM_TYPE)

URL = GLOBAL_DATA['base_url']
URL2 = GLOBAL_DATA['linear_swap_api_base_url']
# ACCESS_KEY = GLOBAL_DATA['AT_DEFAULT_ACCESS_KEY']
# SECRET_KEY = GLOBAL_DATA['AT_DEFAULT_SECRET_KEY']
ACCESS_KEY = "ddde0717-c71a2fa2-ntmuw4rrsr-2c562"
SECRET_KEY = "9e090305-11ffacb5-cfd55719-8cffa"
hbsession = GLOBAL_DATA['AT_DEFAULT_HBSESSION']
MULANURL = "http://mulan-asset.test-5.huobiapps.com"


def set_run_env_and_system_type(run_env, system_type=None):
    global ENV, SYSTEM_TYPE, GLOBAL_DATA
    ENV = run_env
    SYSTEM_TYPE = system_type
    GLOBAL_DATA = ATP.get_global_data(ENV, SYSTEM_TYPE)

# path = os.path.abspath(os.path.dirname(__file__))
# with open('{}/application.yml'.format(path), 'rb') as f:
#     conf = yaml.load(stream=f, Loader=yaml.FullLoader)
#     URL = conf['URL']
#     URL2 = conf['URL2']
#     ACCESS_KEY = conf['ACCESS_KEY']
#     SECRET_KEY = conf['SECRET_KEY']
#     hbsession = conf['hbsession']
#     ATPHost = conf['ATPHost']
#     f.close()
