#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
import time
from schema import Schema, Or

from common.SwapServiceAPI import user01
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_048:

    @allure.title("获取用户的合约历史成交记录")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_matchresults(contract_code=contract_code, trade_type=0, create_date=7)
                if 'ok' in r['status'] and r['data']['trades']:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i + 1}次重试………………………………')
            assert flag, '重试3次未返回预期结果'
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "data": {
                    "current_page": int,
                    "total_page": int,
                    "total_size": int,
                    "trades": [{
                        "contract_code": contract_code,
                        "create_date": int,
                        "direction": Or("sell", "buy"),
                        "match_id": int,
                        "id": str,
                        "offset": Or("close", "open"),
                        "offset_profitloss": Or(int, float, 0, None),
                        "real_profit": Or(int, float, 0, None),
                        "order_id": int,
                        "order_id_str": str,
                        "symbol": symbol,
                        "order_source": str,
                        "trade_fee": Or(int, float, 0, None),
                        "fee_asset": symbol,
                        "trade_price": Or(int, float, 0, None),
                        "trade_turnover": Or(int, float, 0, None),
                        "role": str,
                        "trade_volume": Or(int, float, 0, None)
                    }]
                },
                "status": "ok",
                "ts": int
            }
            Schema(schema).validate(r)
            pass
