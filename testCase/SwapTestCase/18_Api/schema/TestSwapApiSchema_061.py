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
class TestSwapApiSchema_061:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()
        pass

    @classmethod
    def teardown_class(cls):
        user01.swap_cancelall(contract_code=DEFAULT_CONTRACT_CODE)
        pass

    @allure.title("查询开仓单关联的止盈止损订单详情")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：开仓'):
            orderInfo = user01.swap_order(contract_code=contract_code, price=self.currentPrice, direction='buy',
                                          tp_trigger_price=round(self.currentPrice * 1.03, 2),
                                          tp_order_price=round(self.currentPrice * 1.02, 2),
                                          tp_order_price_type='limit')
            orderId = orderInfo['data']['order_id']
            pass
        with allure.step('操作：执行api'):
            r = user01.swap_relation_tpsl_order(contract_code=contract_code, order_id=orderId)
            pass
        schema = {
            "status": "ok",
            "data": {
                "symbol": symbol,
                "contract_code": contract_code,
                "volume": int,
                "price": Or(int, float, 0, None),
                "order_price_type": str,
                "direction": Or("buy", "sell"),
                "offset": Or("open", "close"),
                "lever_rate": int,
                "order_id": int,
                "order_id_str": str,
                "client_order_id": Or(int, float, 0, None),
                "created_at": int,
                "trade_volume": Or(int, float, 0, None),
                "trade_turnover": Or(int, float, 0, None),
                "fee": Or(int, float, 0, None),
                "trade_avg_price": Or(int, float, 0, None),
                "margin_frozen": Or(int, float, 0, None),
                "profit": Or(int, float, 0, None),
                "status": int,
                "order_type": int,
                "order_source": str,
                "fee_asset": symbol,
                # "liquidation_type": str,
                "canceled_at": Or(int, float, 0, None),
                "tpsl_order_info": [{
                    "volume": Or(int, float, 0, None),
                    "direction": Or("sell", "buy"),
                    "tpsl_order_type": str,
                    "order_id": int,
                    "order_id_str": str,
                    "trigger_type": Or("le", "ge"),
                    "trigger_price": Or(int, float, 0, None),
                    "order_price": Or(int, float, 0, None),
                    "created_at": int,
                    "order_price_type": str,
                    "relation_tpsl_order_id": str,
                    "status": int,
                    "canceled_at": int,
                    "fail_code": Or(int, float, 0, None),
                    "fail_reason": Or(int, float, 0, None),
                    "triggered_price": Or(int, float, 0, None),
                    "relation_order_id": Or(str, None)
                }],
            },
            "ts": int
        }
        with allure.step('验证：schema响应字段校验'):
            Schema(schema).validate(r)
            pass
