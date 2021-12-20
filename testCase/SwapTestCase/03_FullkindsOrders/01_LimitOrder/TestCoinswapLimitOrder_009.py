#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 余辉青


import allure
import pytest

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][1])
@allure.tag('Script owner : 陈维', 'Case owner : 吉龙')
class TestCoinswapLimitOrder_009:
    ids = [
        "TestCoinswapLimitOrder_009",
        "TestCoinswapLimitOrder_010"
    ]
    params = [
        {
            "case_name": "对手价 买入开多-无盘口-下单失败",
            "ratio": 1.01,
            "order_price_type": "opponent",
            "direction": "buy"
        },
        {
            "case_name": "对手价 卖出开空-无盘口-下单失败",
            "ratio": 0.99,
            "order_price_type": "opponent",
            "direction": "sell"
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('业务：对手价，无盘口-下单失败'):
            pass
        with allure.step('操作：下单'):
            order_info = user01.swap_order(contract_code=self.contract_code,
                                           price=round(self.latest_price * params['ratio'], 2),
                                           order_price_type=params['order_price_type'], volume=2,
                                           direction=params['direction'])
            pass
        with  allure.step('验证：下单失败'):
            assert "error" in order_info["status"]
            pass


if __name__ == '__main__':
    pytest.main()
