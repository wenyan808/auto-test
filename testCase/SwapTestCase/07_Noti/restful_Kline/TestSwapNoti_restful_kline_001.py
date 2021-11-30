#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211015
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceAPI import t as swap_api
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_kline_001:
    ids = [
        'TestSwapNoti_restful_kline_001',
        'TestSwapNoti_restful_kline_010',
        'TestSwapNoti_restful_kline_019',
        'TestSwapNoti_restful_kline_028',
        'TestSwapNoti_restful_kline_037',
        'TestSwapNoti_restful_kline_046',
        'TestSwapNoti_restful_kline_055',
        'TestSwapNoti_restful_kline_064',
        'TestSwapNoti_restful_kline_073',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-传参from,to不传size', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-传参from,to不传size', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-传参from,to不传size', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-传参from,to不传size', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-传参from,to不传size', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-传参from,to不传size', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-传参from,to不传size', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-传参from,to不传size', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-传参from,to不传size', 'period': '1mon'},
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
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'], to=toTime, From=fromTime)
            assert 'market.{}.kline.{}'.format(contract_code,params['period']) in kLineInfo['ch']
            assert kLineInfo['data']
            pass


if __name__ == '__main__':
    pytest.main()
