#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

import allure
import pytest

from common.SwapServiceAPI import user01 as api_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_depth_025:

    ids = [
        'TestSwapNoti_restful_depth_025'
    ]
    params = [
        {'case_name': 'restful请求最优挂单 传参合约code不存在)', 'contract_code': 'usd-usd'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            result = api_user01.swap_bbo(contract_code=params['contract_code'])
            pass
        with allure.step('验证：返回结果提示invalid-request'):
            assert 'invalid-request' in  result['err-code']
            pass

if __name__ == '__main__':
    pytest.main()
