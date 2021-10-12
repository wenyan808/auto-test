#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan
from tool.global_data import GlobalData

ENV = 'Test6'
SYSTEM_TYPE = 'LinearSwap'
GLOBAL_DATA = GlobalData.get_global_data(ENV, SYSTEM_TYPE)

URL = GLOBAL_DATA['base_url']
URL2 = GLOBAL_DATA['linear_swap_api_base_url']
MULANURL = GLOBAL_DATA['MULANURL']

DEFAULT_SYMBOL = GLOBAL_DATA['DEFAULT_SYMBOL']
DEFAULT_CONTRACT_CODE = GLOBAL_DATA['DEFAULT_CONTRACT_CODE']

ACCESS_KEY = 'mk0lklo0de-7e9e53ef-851e1b70-d9355'#GLOBAL_DATA['AT_DEFAULT_ACCESS_KEY']
SECRET_KEY = '7202ec23-fd8faf72-604b782b-c3eca'#GLOBAL_DATA['AT_DEFAULT_SECRET_KEY']

hbsession = '8365b21e-bc25-4f40-9b72-bc4f73802c67'#GLOBAL_DATA['AT_DEFAULT_HBSESSION']

COMMON_ACCESS_KEY = GLOBAL_DATA['COMMON_ACCESS_KEY']
COMMON_SECRET_KEY = GLOBAL_DATA['COMMON_SECRET_KEY']

CANCEL_ALL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_ORDER_URL']
SWITCH_LEVER_URL = GLOBAL_DATA['SWITCH_LEVER_URL']
CANCEL_ALL_TRACK_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRACK_ORDER_URL']
CANCEL_ALL_TPSL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TPSL_ORDER_URL']
CANCEL_ALL_TRIGGER_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRIGGER_ORDER_URL']


def set_run_env_and_system_type(run_env, system_type=None):
    global ENV, SYSTEM_TYPE, GLOBAL_DATA, URL, URL2, ACCESS_KEY, SECRET_KEY, hbsession, MULANURL, COMMON_SECRET_KEY, COMMON_ACCESS_KEY, \
        CANCEL_ALL_ORDER_URL, SWITCH_LEVER_URL, DEFAULT_SYMBOL, DEFAULT_CONTRACT_CODE, CANCEL_ALL_TRACK_ORDER_URL, CANCEL_ALL_TPSL_ORDER_URL, \
        CANCEL_ALL_TRIGGER_ORDER_URL
    ENV = run_env
    SYSTEM_TYPE = system_type
    GLOBAL_DATA = GlobalData.get_global_data(ENV, SYSTEM_TYPE)
    URL = GLOBAL_DATA['base_url']
    URL2 = GLOBAL_DATA['linear_swap_api_base_url']
    ACCESS_KEY = GLOBAL_DATA['AT_DEFAULT_ACCESS_KEY']
    SECRET_KEY = GLOBAL_DATA['AT_DEFAULT_SECRET_KEY']
    hbsession = GLOBAL_DATA['AT_DEFAULT_HBSESSION']
    MULANURL = GLOBAL_DATA['MULANURL']
    COMMON_ACCESS_KEY = GLOBAL_DATA['COMMON_ACCESS_KEY']
    COMMON_SECRET_KEY = GLOBAL_DATA['COMMON_SECRET_KEY']
    CANCEL_ALL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_ORDER_URL']
    SWITCH_LEVER_URL = GLOBAL_DATA['SWITCH_LEVER_URL']
    DEFAULT_SYMBOL = GLOBAL_DATA['DEFAULT_SYMBOL']
    DEFAULT_CONTRACT_CODE = GLOBAL_DATA['DEFAULT_CONTRACT_CODE']
    CANCEL_ALL_TRACK_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRACK_ORDER_URL']
    CANCEL_ALL_TPSL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TPSL_ORDER_URL']
    CANCEL_ALL_TRIGGER_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRIGGER_ORDER_URL']

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
