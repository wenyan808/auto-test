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
class TestSwapApiSchema_030:

    @allure.title("获取用户的合约手续费费率")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_fee(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "fee_asset": symbol,
                        "open_maker_fee": str,
                        "open_taker_fee": str,
                        "close_maker_fee": str,
                        "close_taker_fee": str,
                    }
                ],
                "ts": int
            }
            Schema(schema).validate(r)
            pass
