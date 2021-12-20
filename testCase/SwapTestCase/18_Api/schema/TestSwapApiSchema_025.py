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
class TestSwapApiSchema_025:

    @allure.title("查询母账户下的单个子账户持仓信息")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_sub_position_info(contract_code=contract_code, sub_uid='115395803')
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "ts": int,
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "volume": Or(float, None),
                        "available": Or(float, None),
                        "frozen": Or(float, None),
                        "cost_open": Or(float, None),
                        "cost_hold": Or(float, None),
                        "profit_unreal": Or(float, None),
                        "profit_rate": Or(float, None),
                        "profit": Or(float, None),
                        "position_margin": Or(float, None),
                        "lever_rate": Or(int, None),
                        "direction": Or('buy', 'sell'),
                        "last_price": Or(float, None)
                    }
                ]
            }
            Schema(schema).validate(r)
            pass
