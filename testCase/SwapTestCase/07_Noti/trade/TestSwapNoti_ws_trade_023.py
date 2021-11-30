#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : HuiQing Yu
import allure
import pytest

from common.SwapServiceWS import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_ws_trade_023:
    ids = ['TestSwapNoti_ws_trade_023']
    params = [{'case_name':'请求成交(req)'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行req请求'):
            subs = {
                "req": "market.{}.trade.detail".format(self.contract_code),
                "size": 5,
                "id": "id8",
            }
            trade_info = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:返回结果各字段不为空'):
            for d in trade_info['data']:
                assert d['id']
                assert d['amount']
                assert d['quantity']
                assert d['price']
                assert d['direction']
            pass
