#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2022/1/4 5:40 下午
# @Author  : HuiQing Yu

import pytest, allure, time
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_restful_trade_002:
    ids = ['TestSwapNoti_restful_trade_002']
    params = [{'title': 'TestSwapNoti_restful_trade_002', 'case_name': '获取市场最近成交记录-不传合约'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['title'])
        with allure.step('操作:执行请求'):
            r=user01.swap_trade(contract_code=None)
            pass
        with allure.step('验证:返回报错invalid contract code'):
            assert 'invalid contract code' in r['err-msg']
            pass
