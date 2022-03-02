#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.SwapServiceAPI import user01
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_024:

    @allure.title("查询母账户下的单个子账户资产信息")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            a = user01.swap_sub_account_list(contract_code=contract_code)
            sub_uid = a['data'][0]['sub_uid']
            r = user01.swap_sub_account_info(contract_code=contract_code, sub_uid=sub_uid)
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "margin_balance": Or(int, float, 0, None),
                        "margin_position": Or(int, float, 0, None),
                        "margin_frozen": Or(int, float, 0, None),
                        "margin_available": Or(int, float, 0, None),
                        "profit_real": Or(int, float, 0, None),
                        "profit_unreal": Or(int, float, 0, None),
                        "withdraw_available": Or(int, float, 0, None),
                        "risk_rate": Or(int, float, 0, None),
                        "liquidation_price": Or(int, float, 0, None),
                        "adjust_factor": Or(int, float, 0, None),
                        "lever_rate": Or(int, None),
                        "margin_static": Or(int, float, 0, None),
                        "transfer_profit_ratio": Or(int, float, 0, None),
                    }
                ],
                "ts": int
            }

            Schema(schema).validate(r)
            pass
