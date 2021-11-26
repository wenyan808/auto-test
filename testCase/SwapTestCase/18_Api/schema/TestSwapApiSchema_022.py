#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import t
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_022:

    @allure.title("批量获取子账户资产信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = t.swap_sub_account_info_list(contract_code=contract_code, page_index=1, page_size=1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "ts": int,
                "data": {
                    "current_page": int,
                    "total_page": int,
                    "total_size": int,
                    "sub_list": [{
                        "sub_uid": int,
                        "account_info_list": [{
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "margin_balance": Or(int,float,None),
                            "liquidation_price": Or(int,float,None),
                            "risk_rate": Or(int,None)
                        }
                        ]
                    }]
                }
            }
            Schema(schema).validate(r)
            pass
