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
class TestSwapNoti_restful_kline_002:
    ids = [
        'TestSwapNoti_restful_kline_002',
        'TestSwapNoti_restful_kline_011',
        'TestSwapNoti_restful_kline_020',
        'TestSwapNoti_restful_kline_029',
        'TestSwapNoti_restful_kline_038',
        'TestSwapNoti_restful_kline_047',
        'TestSwapNoti_restful_kline_056',
        'TestSwapNoti_restful_kline_065',
        'TestSwapNoti_restful_kline_074',
           ]
    params = [
        {'case_name': 'restful请求K线-1min-只传参size不传from不传to', 'period': '1min'},
        {'case_name': 'restful请求K线-5min-只传参size不传from不传to', 'period': '5min'},
        {'case_name': 'restful请求K线-15min-只传参size不传from不传to', 'period': '15min'},
        {'case_name': 'restful请求K线-30min-只传参size不传from不传to', 'period': '30min'},
        {'case_name': 'restful请求K线-60min-只传参size不传from不传to', 'period': '60min'},
        {'case_name': 'restful请求K线-4hour-只传参size不传from不传to', 'period': '4hour'},
        {'case_name': 'restful请求K线-1day-只传参size不传from不传to', 'period': '1day'},
        {'case_name': 'restful请求K线-1week-只传参size不传from不传to', 'period': '1week'},
        {'case_name': 'restful请求K线-1mon-只传参size不传from不传to', 'period': '1mon'},
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
            size = 10
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=params['period'], size=size)
            pass
        with allure.step('验证:返回结果各字段不为空'):
            assert 'market.{}.kline.{}'.format(contract_code,params['period']) in kLineInfo['ch']
            if 'data' in kLineInfo:
                assert len(kLineInfo['data']) <= size
                for data in kLineInfo['data']:
                    assert data['open']
                    assert data['close']
                    assert data['low']
                    assert data['high']
                    assert data['amount'] >=0
                    assert data['vol'] >=0
                    assert data['count'] >=0
            else:
                assert False , 'data未返回'
                pass
            with allure.step('验证:数据的连续性'):
                if '1min' in params['period']:
                    # 断言24小时k线的连续
                    for i in range(len(kLineInfo['data'])):
                        if i != len(kLineInfo['data']) - 1:
                            assert kLineInfo['data'][i]['id'] + 60 == kLineInfo['data'][i + 1]['id']
            pass


if __name__ == '__main__':
    pytest.main()
