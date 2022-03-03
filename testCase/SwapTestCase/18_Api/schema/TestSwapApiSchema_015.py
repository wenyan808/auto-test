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
class TestSwapApiSchema_015:

    @allure.title("查询系统状态")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_api_state(contract_code=contract_code)
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "open": Or(1,0),
                        "close": Or(1,0),
                        "cancel": Or(1,0),
                        "transfer_in": Or(1,0),
                        "transfer_out": Or(1,0),
                        "master_transfer_sub": Or(1,0),
                        "sub_transfer_master": Or(1,0)
                    }
                ],
                "ts": int
            }
            Schema(schema).validate(r)
            pass
