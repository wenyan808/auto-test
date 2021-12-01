#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu


import allure
import pytest
import time
import random

from config.case_content import epic, features
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from common.CommonUtils import currentPrice


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestCoinswapTriggerOrder_001:
    ids = [
        "TestCoinswapTriggerOrder_001",
        "TestCoinswapTriggerOrder_003",
    ]
    params = [
        {
            "case_name": "计划委托 正常限价开仓测试",
            "order_price_type": "limit",
        },
        {
            "case_name": "计划委托 最优5挡开仓测试",
            "order_price_type": "optimal_5",
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
            user01.swap_trigger_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：下单'):
            order_reps = user01.swap_trigger_order(contract_code=self.contract_code, trigger_type='ge',
                                                trigger_price=round(self.latest_price * 1.01, 2),volume=1,
                                                order_price=round(self.latest_price*0.99,2),direction='buy',
                                                offset='open',order_price_type=params['order_price_type'] )

            pass
        with allure.step('验证：下单成功'):
            orderId = order_reps['data']['order_id']
            assert 'ok' in order_reps['status'] and orderId
            pass
        with allure.step('验证：订单信息与下单数据一致'):
            time.sleep(1)  # 等待数据更新
            orders = user01.swap_trigger_openorders(contract_code=self.contract_code,page_size=1,page_index=1)['data']['orders']
            assert orders[0]['order_id'] == orderId,'订单校验未存在'
            assert self.contract_code in orders[0]['contract_code'],'合约校验失败'
            assert orders[0]['volume'] == 1,'合约数量校验失败'
            assert orders[0]['lever_rate'] == 5,'合约倍数校验失败'
            assert orders[0]['trigger_price'] == round(self.latest_price * 1.01, 2),'触发价格校验失败'
            if "optimal" in params['order_price_type']:
                assert orders[0]['order_price'] == 0E-18,'订单价格校验失败'
            else:
                assert orders[0]['order_price'] == round(self.latest_price * 0.99, 2), '订单价格校验失败'
            assert 'open' in orders[0]['offset'],'订单 平|开 校验失败'
            assert 'buy' in orders[0]['direction'],'订单 买|卖 校验失败'
            assert params['order_price_type'] in orders[0]['order_price_type'],'订单类型校验失败'


            pass


if __name__ == '__main__':
    pytest.main()
