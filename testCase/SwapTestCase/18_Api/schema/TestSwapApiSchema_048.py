#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_048:

    @allure.title("获取用户的合约历史成交记录")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_matchresults(contract_code=contract_code, trade_type=0, page_size=3, page_index=1,
                                         create_date=7)
            pass
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
