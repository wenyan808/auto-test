#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211015
# @Author : HuiQing Yu

import allure
import pytest
import time
import random

from common.SwapServiceAPI import t as swap_api
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_kline_003:
    ids = [
        'TestSwapNoti_restful_kline_003',
        'TestSwapNoti_restful_kline_012',
        'TestSwapNoti_restful_kline_021',
        'TestSwapNoti_restful_kline_030',
        'TestSwapNoti_restful_kline_039',
        'TestSwapNoti_restful_kline_048',
        'TestSwapNoti_restful_kline_057',
        'TestSwapNoti_restful_kline_066',
        'TestSwapNoti_restful_kline_075',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-传参from,to,size', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-传参from,to,size', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-传参from,to,size', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-传参from,to,size', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-传参from,to,size', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-传参from,to,size', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-传参from,to,size', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-传参from,to,size', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-传参from,to,size', 'period': '1mon'},
    ]

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, contract_code):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作:执行restful-api请求'):
            toTime = int(time.time())
            fromTime = toTime - 60
            size = random.randint(5,10)
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'], to=toTime, From=fromTime,size=size)
            pass
        with allure.step('验证:返回字段不为空，size与请求一致'):
            assert 'market.{}.kline.{}'.format(contract_code,params['period']) in kLineInfo['ch']
            assert kLineInfo['data']
            assert len(kLineInfo['data'])<=size
            pass


if __name__ == '__main__':
    pytest.main()
