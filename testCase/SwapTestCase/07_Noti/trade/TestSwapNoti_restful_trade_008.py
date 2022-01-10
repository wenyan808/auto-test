#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2022/1/4 5:40 下午
# @Author  : HuiQing Yu

import pytest, allure, time
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_restful_trade_008:
    ids = ['TestSwapNoti_restful_trade_008']
    params = [{'title': 'TestSwapNoti_restful_trade_008', 'case_name': '批量获取市场最近成交记录-合约已下市'}]

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
            contract_info = SwapTool.getContractStatus(instrument_status=0)
            if contract_info['isSkip']:
                assert False, '未找到下市合约'
            r=user01.swap_history_trade(contract_code=contract_info['data']['instrument_id'],size=1)
            pass
        with allure.step('验证:返回各字段不为空'):
            assert 'invalid contract code' in r['err-msg']
            pass
