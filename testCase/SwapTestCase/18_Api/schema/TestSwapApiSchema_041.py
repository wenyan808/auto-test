#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from tool.SwapTools import SwapTool
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_041:

    @allure.title("撤销全部合约单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = SwapTool.currentPrice()
            user01.swap_order(contract_code=contract_code,price=round(self.currentPrice*0.8,2),direction='buy')
            for i in range(3):
                r = user01.swap_cancelall(contract_code=contract_code)
                if 'ok' in r['status'] and r['data']['successes']:
                    break
                else:
                    print(f'撤销失败，第{i+1}次重试……')
                    time.sleep(1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "errors": [
                        {
                            "order_id": str,
                            "err_code": int,
                            "err_msg": str
                        }
                    ],
                    "successes": str
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
