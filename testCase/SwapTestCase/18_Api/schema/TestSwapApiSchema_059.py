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
@allure.feature('18API')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_059:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()

    @classmethod
    def teardown_class(cls):
        user01.swap_tpsl_cancelall(contract_code=DEFAULT_CONTRACT_CODE)
        pass

    @allure.title("获取止盈止损当前委托")
    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：挂单'):
            user01.swap_tpsl_order(contract_code=contract_code, volume=1, direction='sell',
                                   tp_trigger_price=round(self.currentPrice * 1.01, 2),
                                   tp_order_price_type='optimal_5', sl_order_price_type='optimal_5')
            pass
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                r = user01.swap_tpsl_openorders(contract_code=contract_code)
                if r['data']['orders']:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '重试3次未返回预期结果'
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "total_page": int,
                    "total_size": int,
                    "current_page": int,
                    "orders": [{
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "volume": Or(float, int, 0, None),
                        "order_type": int,
                        "tpsl_order_type": str,
                        "direction": Or("buy", "sell"),
                        "order_id": int,
                        "order_id_str": str,
                        "order_source": str,
                        "order_price": Or(float, int, 0, None),
                        "trigger_type": Or("ge", "le"),
                        "trigger_price": Or(float, int, 0, None),
                        "created_at": int,
                        "order_price_type": str,
                        "status": int,
                        "source_order_id": Or(str,None),
                        "relation_tpsl_order_id": str
                    }]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
