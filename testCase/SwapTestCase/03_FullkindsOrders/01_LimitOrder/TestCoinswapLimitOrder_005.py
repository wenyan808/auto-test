#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 余辉青


import time

import allure
import pytest

from common.SwapServiceAPI import user01, user02
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][1])
@allure.tag('Script owner : 陈维', 'Case owner : 吉龙')
class TestCoinswapLimitOrder_005:
    ids = [
        "TestCoinswapLimitOrder_005",
        "TestCoinswapLimitOrder_006",
    ]
    params = [
        {
            "case_name": "IOC 买入开多下单后自动撤单测试",
            "ratio": 1.01,
            "order_price_type": "ioc",
            "direction": "buy"
        }, 
        {
            "case_name": "IOC 卖出开空下单后自动撤单测试",
            "ratio": 0.99,
            "order_price_type": "ioc",
            "direction": "sell"
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass
            with allure.step("挂盘"):
                user02.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 0.99, 2),
                                  direction='buy')
                user02.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 1.01, 2),
                                  direction='sell')
                pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            user02.swap_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('业务：IOC单如果不能全部成交，则未成交部分会被撤单'):
            pass
        with allure.step('操作：下单'):
            orderId = \
            user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price * params['ratio'], 2),
                              order_price_type=params['order_price_type'],volume=2,
                              direction=params['direction'])['data']['order_id']
            pass
        with allure.step('操作：获取订单信息'):
            time.sleep(1)  # 等待数据更新
            order_info = user01.swap_order_info(contract_code=self.contract_code, order_id=orderId)
            pass
        with  allure.step('验证：IOC未全部成交，订单被取消'):
            for data in order_info['data']:
                assert data['status'] == 5
            pass
        with  allure.step('验证：无资产冻结'):
            account_info = user01.swap_account_info(contract_code=self.contract_code)
            for data in account_info['data']:
                assert data['margin_frozen'] == 0E-18
            pass


if __name__ == '__main__':
    pytest.main()
