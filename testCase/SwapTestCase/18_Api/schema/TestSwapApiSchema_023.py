#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import t


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_023:

    @allure.title("查询母账户下所有子账户资产信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = t.swap_sub_account_list(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "ts": int,
                "data": [
                    {
                        "sub_uid": int,
                        "list": [
                            {
                                "symbol": symbol,
                                "contract_code": contract_code,
                                "margin_balance": Or(int,float,0,None),
                                "liquidation_price": Or(int,float,0,None),
                                "risk_rate": Or(int,None)
                            }
                        ]
                    }
                ]
            }
            Schema(schema).validate(r)
            pass
