#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_020:

    @allure.title("获取用户的合约持仓信息")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_position_info(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "volume": Or(int,float,0,None),
                        "available": Or(int,float,0,None),
                        "frozen": Or(float,0,None),
                        "cost_open": Or(float,0,None),
                        "cost_hold": Or(float,0,None),
                        "profit_unreal": Or(float,0,None),
                        "profit_rate": Or(float,0,None),
                        "profit": Or(float,0,None),
                        "position_margin": Or(float,0,None),
                        "lever_rate": int,
                        "direction": Or('buy','sell'),
                        "last_price": Or(float,0,None),
                    }
                ],
                "ts": int
            }
            Schema(schema).validate(r)
            pass
