#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_027:

    @allure.title("组合查询用户财务记录")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_financial_record_exact(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "financial_record": [
                        {
                            "id": int,
                            "ts": int,
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "type": int,
                            "amount": Or(float, None),
                        }
                    ],
                    "remain_size": int,
                    "next_id": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
