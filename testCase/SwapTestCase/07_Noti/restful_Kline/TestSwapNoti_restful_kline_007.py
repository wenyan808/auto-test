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
class TestSwapNoti_restful_kline_007:
    ids = [
        'TestSwapNoti_restful_kline_007',
        'TestSwapNoti_restful_kline_016',
        'TestSwapNoti_restful_kline_025',
        'TestSwapNoti_restful_kline_034',
        'TestSwapNoti_restful_kline_043',
        'TestSwapNoti_restful_kline_052',
        'TestSwapNoti_restful_kline_061',
        'TestSwapNoti_restful_kline_070',
        'TestSwapNoti_restful_kline_079',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-传无效格式to传from不传size', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-传无效格式to传from不传size', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-传无效格式to传from不传size', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-传无效格式to传from不传size', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-传无效格式to传from不传size', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-传无效格式to传from不传size', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-传无效格式to传from不传size', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-传无效格式to传from不传size', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-传无效格式to传from不传size', 'period': '1mon'},
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
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'], From=toTime, to='*')
            pass
        with allure.step('验证:返回错误提示invalid to'):
            assert 'invalid to' in kLineInfo['err-msg']
            assert 'bad-request' in kLineInfo['err-code']
            assert 'error' in kLineInfo['status']
            pass


if __name__ == '__main__':
    pytest.main()
