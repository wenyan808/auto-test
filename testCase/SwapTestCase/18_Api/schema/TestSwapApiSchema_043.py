#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_043:

    @allure.title("获取用户的合约订单信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = currentPrice()
            orderId = user01.swap_order(contract_code=contract_code,
                                        price=round(self.currentPrice * 0.5, 2), direction='buy')['data'][
                'order_id_str']
            time.sleep(1)
            r = user01.swap_order_info(order_id=orderId, contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'data': [{
                    'symbol': symbol,
                    'contract_code': contract_code,
                    'created_at': int,
                    'direction': Or('buy','sell'),
                    'fee': Or(float, int, 0, None),
                    'fee_asset': symbol,
                    'lever_rate': int,
                    'margin_frozen': Or(float, int, 0, None),
                    'offset': Or('open','sell'),
                    'order_id': int,
                    'order_id_str': str,
                    'client_order_id': None,
                    'order_price_type': 'limit',
                    'order_source': 'api',
                    'order_type': Or(float, int, 0, None),
                    'price': Or(float, int, 0, None),
                    'profit': Or(float, int, 0, None),
                    'real_profit': Or(float, int, 0, None),
                    'status': Or(1, 2, 3, 4, 5, 6, 7, 11),
                    'trade_avg_price': Or(float, int, 0, None),
                    'trade_turnover': Or(float, int, 0, None),
                    'trade_volume': Or(float, int, 0, None),
                    'volume': Or(float, int, 0, None),
                    'liquidation_type': str,
                    'canceled_at': int,
                    'update_time':None,
                    "is_tpsl": Or(1, 0)
                }],
                'status': 'ok',
                'ts': int
            }
            Schema(schema).validate(r)
            pass
