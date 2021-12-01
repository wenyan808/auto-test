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
class TestSwapNoti_restful_kline_008:
    ids = [
        'TestSwapNoti_restful_kline_008',
        'TestSwapNoti_restful_kline_017',
        'TestSwapNoti_restful_kline_026',
        'TestSwapNoti_restful_kline_035',
        'TestSwapNoti_restful_kline_044',
        'TestSwapNoti_restful_kline_053',
        'TestSwapNoti_restful_kline_062',
        'TestSwapNoti_restful_kline_071',
        'TestSwapNoti_restful_kline_080',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-传参size=2001不传from不传to', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-传参size=2001不传from不传to', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-传参size=2001不传from不传to', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-传参size=2001不传from不传to', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-传参size=2001不传from不传to', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-传参size=2001不传from不传to', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-传参size=2001不传from不传to', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-传参size=2001不传from不传to', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-传参size=2001不传from不传to', 'period': '1mon'},
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
            size = 2001
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'], size=size)
            pass
        with allure.step('验证:返回结果提示invalid size, valid range: [1,2000]'):
            assert 'invalid size, valid range: [1,2000]' in kLineInfo['err-msg']
            assert 'bad-request' in kLineInfo['err-code']
            assert 'error' in kLineInfo['status']

            pass


if __name__ == '__main__':
    pytest.main()
