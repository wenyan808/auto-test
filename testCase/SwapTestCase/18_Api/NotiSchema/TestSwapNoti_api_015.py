#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 2:09 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

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
class TestSwapNoti_api_015:
    ids = ['TestSwapNoti_api_015']
    params = [{'title': 'TestSwapNoti_api_015', 'case_name': 'WS 聚合行情'}]

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
                "sub": "market.{}.detail".format(self.contract_code),
                "id": "id6"
            }
            r = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                "ch": f"market.{self.contract_code}.detail",
                "ts": int,
                "tick": {
                    "id": int,
                    "mrid": Or(int,float),
                    "open": Or(int,float),
                    "close": Or(int,float),
                    "high": Or(int,float),
                    "low": Or(int,float),
                    "amount": Or(int,float),
                    "vol": Or(int,float),
                    "count": int,
                    "ask": list,
                    "bid": list
                }
            }
            Schema(schema).validate(r)
            pass