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
class TestSwapNoti_api_017:
    ids = ['TestSwapNoti_api_017']
    params = [{'title': 'TestSwapNoti_api_017', 'case_name': 'WS 历史成交(req)'}]

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
                "req": f"market.{self.contract_code}.trade.detail",
                "id": "test_depth_id",
                "size": 1
            }
            r = user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:schema响应字段校验'):
            schema = {
                "data": [
                    {
                        "amount": str,
                        "quantity": str,
                        "ts": int,
                        "id": int,
                        "price": str,
                        "direction": Or("buy","sell"),
                        "contract_code": self.contract_code
                    }
                ],
                "id": "test_depth_id",
                "rep": f"market.{self.contract_code}.trade.detail",
                "status": "ok",
                "ts": int
            }
            Schema(schema).validate(r)
            pass