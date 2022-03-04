#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
import time
from pprint import pprint

import allure
import pytest
from common.SwapServiceAPI import user01
from schema import Schema, Or
from config.case_content import epic, features
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_050:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))
        ATP.make_market_depth(volume=2, depth_count=5)

    @classmethod
    def teardown(self):
        with allure.step('恢复环境:取消挂单'):
            print(ATP.cancel_all_types_order())
            print(ATP.close_all_position())
            pass

    @allure.title("合约闪电平仓下单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            price = ATP.get_current_price()
            buy_order = user01.swap_order(contract_code=contract_code, price=price, direction='buy')
            pprint(buy_order)
            sell_order = user01.swap_order(contract_code=contract_code, price=price, direction='sell')
            pprint(sell_order)
            time.sleep(5)
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1):
                r = user01.swap_lightning_close_position(contract_code=contract_code, volume=1,
                                                         direction="sell", order_price_type="lightning")
                if 'ok' in r['status'] and r['data']['order_id']:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i + 1}次重试………………………………')
            assert flag, '重试3次未返回预期结果'
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "order_id": int,
                    "order_id_str": str
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
