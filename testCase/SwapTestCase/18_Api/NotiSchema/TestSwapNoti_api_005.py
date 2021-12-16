#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/16 2:09 下午
# @Author  : HuiQing Yu

import pytest, allure, time
from schema import Or, Schema

from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_api_005:
    ids = ['TestSwapNoti_api_005']
    params = [{'title': 'TestSwapNoti_api_005', 'case_name': 'restful获取市场成交记录'}]

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
            r = user01.swap_trade(contract_code=self.contract_code)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                "ch": f"market.{self.contract_code}.trade.detail",
                "status": "ok",
                "tick": {
                    "data": [
                        {
                            "amount": str,
                            "quantity": str,
                            "direction": Or('buy','sell'),
                            "id": int,
                            "price": str,
                            "ts": int,
                            "contract_code": self.contract_code
                        }
                    ],
                    "id": int,
                    "ts": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass