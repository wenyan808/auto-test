#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_045:

    @classmethod
    def teardown_class(cls):
        user01.swap_cancelall(contract_code=DEFAULT_CONTRACT_CODE)
        pass

    @allure.title("获取用户的合约当前未成交委托")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = currentPrice()
            user01.swap_order(contract_code=contract_code, price=round(self.currentPrice * 0.5, 2), direction='buy')
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                r = user01.swap_openorders(contract_code=contract_code)
                if r['data']['orders']:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '重试3次未返回预期结果'
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'data': {
                    'current_page': int,
                    'orders': [{
                        'canceled_at': Or(int, float, 0, None),
                        'client_order_id': None,
                        'contract_code': contract_code,
                        'created_at': int,
                        'direction': Or('buy', 'sell'),
                        'fee': Or(int, float, 0, None),
                        'fee_asset': symbol,
                        'is_tpsl': Or(0, 1),
                        'lever_rate': int,
                        'liquidation_type': Or(int, float, 0, None),
                        'margin_frozen': Or(int, float, 0, None),
                        'offset': Or('open', 'close'),
                        'order_id': int,
                        'order_id_str': str,
                        'order_price_type': str,
                        'order_source': str,
                        'order_type': int,
                        'price': Or(int, float, 0, None),
                        'profit': Or(int, float, 0, None),
                        'real_profit': Or(int, float, 0, None),
                        'status': int,
                        'symbol': symbol,
                        'trade_avg_price': Or(int, float, 0, None),
                        'trade_turnover': Or(int, float, 0, None),
                        'trade_volume': Or(int, float, 0, None),
                        'update_time': int,
                        'volume': Or(int, float, 0, None)
                    }],
                    'total_page': int,
                    'total_size': int
                },
                'status': 'ok',
                'ts': int
            }
            Schema(schema).validate(r)
            pass
