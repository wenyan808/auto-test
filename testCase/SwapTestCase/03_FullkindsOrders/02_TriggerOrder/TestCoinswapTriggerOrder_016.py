#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

import time
from decimal import Decimal
import random
import allure
import pytest

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01,user02
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_016:
    ids = [
        "TestCoinswapTriggerOrder_016",
        "TestCoinswapTriggerOrder_018",
    ]
    params = [
        {
            "case_name": "下单区域下止盈止损限价单成交测试",
            "tp_order_price_type": "limit",
        },
        {
            "case_name": "下单区域下止盈止损最优5/10/20档限价单成交测试",
            "tp_order_price_type": "optimal_{}".format(random.choice([5, 10, 20])),
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            user01.swap_tpsl_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params, DB_contract_trade):
        allure.dynamic.title(params['case_name'])
        with allure.step("操作：挂卖盘"):
            user02.swap_order(contract_code=self.contract_code, price=self.latest_price, direction='sell')
            pass
        with allure.step('操作：下限价单并设置止盈'):
            limit_order = user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price, 2),
                                            direction='buy',
                                            tp_order_price=round(self.latest_price * 1.5, 2),
                                            tp_order_price_type=params['tp_order_price_type'],
                                            tp_trigger_price=round(self.latest_price * 1.5, 2))
            pass
        with allure.step('验证：未成交时，止盈单状态未触发'):
            for i in range(5):
                relation_tpsl_order = user01.swap_relation_tpsl_order(contract_code=self.contract_code,
                                                                      order_id=limit_order['data']['order_id'])
                if relation_tpsl_order['data']['tpsl_order_info'] or 1 != relation_tpsl_order['data']['tpsl_order_info'][0]['status']:
                    print(f'触发后数据未更新，第{i+1}次重试')
                    time.sleep(1)
                else:
                    break
            tpsl_order_info = relation_tpsl_order['data']['tpsl_order_info'][0]
            assert 2 == tpsl_order_info['status'], '成交前状态校验失败'
            pass
        with allure.step('验证：未成交时，止盈信息'):
            assert 1.00 == round(tpsl_order_info['volume'], 2)
            assert round(self.latest_price * 1.5, 2) == round(tpsl_order_info['trigger_price'], 2), '触发价校验失败'
            if 'limit' in params['tp_order_price_type']:
                assert round(self.latest_price * 1.5, 2)  == round(tpsl_order_info['order_price'], 2), '止盈价校验失败'
            else:
                assert 0E-18 == round(tpsl_order_info['order_price'], 2), '止盈价校验失败'
            assert params['tp_order_price_type'] == tpsl_order_info['order_price_type'], '订单类型校验失败'
            pass


if __name__ == '__main__':
    pytest.main()
