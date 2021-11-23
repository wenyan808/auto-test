#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_025:

    @allure.title("查询母账户下的单个子账户持仓信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
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
