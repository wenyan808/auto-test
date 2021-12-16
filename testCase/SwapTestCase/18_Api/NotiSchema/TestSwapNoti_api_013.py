#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 2:09 下午
# @Author  : HuiQing Yu

import pytest, allure, time
from schema import Or, Schema

from common.SwapServiceWS import user01
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_api_013:
    ids = ['TestSwapNoti_api_013']
    params = [{'title': 'TestSwapNoti_api_013', 'case_name': 'WS K线(sub)'}]

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
            subs = {
                "sub": "market.{}.kline.1min".format(self.contract_code),
                "id": "id1"
            }
            r = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                "ch": f"market.{self.contract_code}.kline.1min",
                "ts": int,
                "tick": {
                    "id": int,
                    "mrid": int,
                    "open": Or(int,float),
                    "close": Or(int,float),
                    "high": Or(int,float),
                    "low":  Or(int,float),
                    "amount":  Or(int,float),
                    "vol":  Or(int,float),
                    "count": int
                }
            }
            Schema(schema).validate(r)
            pass