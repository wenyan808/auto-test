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
class TestSwapNoti_restful_kline_009:
    ids = [
        'TestSwapNoti_restful_kline_009',
        'TestSwapNoti_restful_kline_018',
        'TestSwapNoti_restful_kline_027',
        'TestSwapNoti_restful_kline_036',
        'TestSwapNoti_restful_kline_045',
        'TestSwapNoti_restful_kline_054',
        'TestSwapNoti_restful_kline_063',
        'TestSwapNoti_restful_kline_072',
        'TestSwapNoti_restful_kline_081',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-不传to不传from不传size', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-不传to不传from不传size', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-不传to不传from不传size', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-不传to不传from不传size', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-不传to不传from不传size', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-不传to不传from不传size', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-不传to不传from不传size', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-不传to不传from不传size', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-不传to不传from不传size', 'period': '1mon'},
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
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'])
            pass
        with allure.step('验证:返回错误提示invalid to'):
            assert 'from cannot be empty' in kLineInfo['err-msg']
            assert 'invalid-request' in kLineInfo['err-code']
            assert 'error' in kLineInfo['status']
            pass


if __name__ == '__main__':
    pytest.main()
