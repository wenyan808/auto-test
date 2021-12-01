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
class TestSwapNoti_restful_kline_005:
    ids = [
        'TestSwapNoti_restful_kline_005',
        'TestSwapNoti_restful_kline_014',
        'TestSwapNoti_restful_kline_023',
        'TestSwapNoti_restful_kline_032',
        'TestSwapNoti_restful_kline_041',
        'TestSwapNoti_restful_kline_050',
        'TestSwapNoti_restful_kline_059',
        'TestSwapNoti_restful_kline_068',
        'TestSwapNoti_restful_kline_077',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-只传to不传from不传size', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-只传to不传from不传size', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-只传to不传from不传size', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-只传to不传from不传size', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-只传to不传from不传size', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-只传to不传from不传size', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-只传to不传from不传size', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-只传to不传from不传size', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-只传to不传from不传size', 'period': '1mon'},
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
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'], to=toTime)
            pass
        with allure.step('验证:返回错误提示from cannot be empty'):
            assert 'from cannot be empty' in kLineInfo['err-msg']
            assert 'invalid-request' in kLineInfo['err-code']
            assert 'error' in kLineInfo['status']
            pass


if __name__ == '__main__':
    pytest.main()
