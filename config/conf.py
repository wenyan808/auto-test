#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/8/31
# @Author  : Donglin Han
from tool.global_data import GlobalData

ENV = 'Test6'

SYSTEM_TYPE = 'Delivery'  # Delivery, Swap,  LinearSwap
GLOBAL_DATA = GlobalData.get_global_data(ENV, SYSTEM_TYPE)

URL = GLOBAL_DATA['base_url']
URL2 = GLOBAL_DATA['linear_swap_api_base_url']
MULANURL = GLOBAL_DATA['MULANURL']
WSURL = GLOBAL_DATA['WSURL']

DEFAULT_SYMBOL = GLOBAL_DATA['DEFAULT_SYMBOL']
DEFAULT_CONTRACT_CODE = GLOBAL_DATA['DEFAULT_CONTRACT_CODE']

ACCESS_KEY = GLOBAL_DATA['AT_DEFAULT_ACCESS_KEY']
SECRET_KEY = GLOBAL_DATA['AT_DEFAULT_SECRET_KEY']
hbsession = GLOBAL_DATA['AT_DEFAULT_HBSESSION']


COMMON_ACCESS_KEY = GLOBAL_DATA['COMMON_ACCESS_KEY']
COMMON_SECRET_KEY = GLOBAL_DATA['COMMON_SECRET_KEY']

CANCEL_ALL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_ORDER_URL']
SWITCH_LEVER_URL = GLOBAL_DATA['SWITCH_LEVER_URL']
CANCEL_ALL_TRACK_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRACK_ORDER_URL']
CANCEL_ALL_TPSL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TPSL_ORDER_URL']
CANCEL_ALL_TRIGGER_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRIGGER_ORDER_URL']
MARKET_DEPTH_URL = GLOBAL_DATA['MARKET_DEPTH_URL']
POSITION_INFO_URL = GLOBAL_DATA['POSITION_INFO_URL']
PLACE_ORDER_URL = GLOBAL_DATA['PLACE_ORDER_URL']
CONTRACT_INFO_URL = GLOBAL_DATA['CONTRACT_INFO_URL']
REDIS_CONF = GLOBAL_DATA['REDIS_CONF']
MYSQL_CONF = GLOBAL_DATA['MYSQL_CONF']
MQ_INFO = GLOBAL_DATA['MQ_INFO']
USERINFO = GLOBAL_DATA['USERINFO']
MGT_INFO = GLOBAL_DATA['MGT_INFO']


def set_run_env_and_system_type(run_env, system_type):
    global ENV, SYSTEM_TYPE, GLOBAL_DATA, URL, URL2, ACCESS_KEY, SECRET_KEY, hbsession, MULANURL, COMMON_SECRET_KEY, COMMON_ACCESS_KEY, \
        CANCEL_ALL_ORDER_URL, SWITCH_LEVER_URL, DEFAULT_SYMBOL, DEFAULT_CONTRACT_CODE, CANCEL_ALL_TRACK_ORDER_URL, CANCEL_ALL_TPSL_ORDER_URL, \
        CANCEL_ALL_TRIGGER_ORDER_URL, POSITION_INFO_URL, PLACE_ORDER_URL, CONTRACT_INFO_URL, MARKET_DEPTH_URL, WSURL, REDIS_CONF, MYSQL_CONF, USERINFO, MGT_INFO

    ENV = run_env
    SYSTEM_TYPE = system_type
    GLOBAL_DATA = GlobalData.get_global_data(ENV, SYSTEM_TYPE)
    URL = GLOBAL_DATA['base_url']
    URL2 = GLOBAL_DATA['linear_swap_api_base_url']
    ACCESS_KEY = GLOBAL_DATA['AT_DEFAULT_ACCESS_KEY']
    SECRET_KEY = GLOBAL_DATA['AT_DEFAULT_SECRET_KEY']
    hbsession = GLOBAL_DATA['AT_DEFAULT_HBSESSION']
    MULANURL = GLOBAL_DATA['MULANURL']
    WSURL = GLOBAL_DATA['WSURL']
    USERINFO = GLOBAL_DATA['USERINFO']
    REDIS_CONF = GLOBAL_DATA['REDIS_CONF']
    MQ_INFO = GLOBAL_DATA['MQ_INFO']
    MYSQL_CONF = GLOBAL_DATA['MYSQL_CONF']
    MGT_INFO = GLOBAL_DATA['MGT_INFO']
    COMMON_ACCESS_KEY = GLOBAL_DATA['COMMON_ACCESS_KEY']
    COMMON_SECRET_KEY = GLOBAL_DATA['COMMON_SECRET_KEY']
    CANCEL_ALL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_ORDER_URL']
    SWITCH_LEVER_URL = GLOBAL_DATA['SWITCH_LEVER_URL']
    DEFAULT_SYMBOL = GLOBAL_DATA['DEFAULT_SYMBOL']
    DEFAULT_CONTRACT_CODE = GLOBAL_DATA['DEFAULT_CONTRACT_CODE']
    CANCEL_ALL_TRACK_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRACK_ORDER_URL']
    CANCEL_ALL_TPSL_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TPSL_ORDER_URL']
    CANCEL_ALL_TRIGGER_ORDER_URL = GLOBAL_DATA['CANCEL_ALL_TRIGGER_ORDER_URL']
    POSITION_INFO_URL = GLOBAL_DATA['POSITION_INFO_URL']
    PLACE_ORDER_URL = GLOBAL_DATA['PLACE_ORDER_URL']
    CONTRACT_INFO_URL = GLOBAL_DATA['CONTRACT_INFO_URL']
    MARKET_DEPTH_URL = GLOBAL_DATA['MARKET_DEPTH_URL']
