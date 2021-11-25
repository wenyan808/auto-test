#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

import time
import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from common.CommonUtils import currentPrice,opponentExist
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_depth_025:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestSwapNoti_restful_depth_025'
    ]
    params = [
        {'case_name': 'restful请求最优挂单 传参合约code不存在)', 'contract_code': 'usd-usd'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.symbol = DEFAULT_SYMBOL
            cls.currentPrice = currentPrice()  # 最新价
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
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
