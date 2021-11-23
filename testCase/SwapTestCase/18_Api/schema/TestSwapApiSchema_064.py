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
class TestSwapApiSchema_064:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()
        cls.orderId = user01.swap_track_order(contract_code=DEFAULT_CONTRACT_CODE, volume=1, direction='buy',
                                              order_price_type='optimal_5',
                                              offset='open', lever_rate=5, active_price=round(cls.currentPrice*0.99, 2),
                                              callback_rate=0.01)['data']['order_id_str']
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @allure.title("跟踪委托全部撤单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                r = user01.swap_track_cancelall(contract_code=contract_code)
                if r['data']['successes']:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '重试3次未返回预期结果'
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'status': 'ok',
                'ts': int,
                'data': {
                    'errors': [{
                        'err_code': int,
                        'err_msg': str,
                        'order_id': str
                    }],
                    'successes': str
                }
            }
            Schema(schema).validate(r)
            pass
