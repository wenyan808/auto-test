#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 余辉青


import allure
import pytest
import time

from common.SwapServiceAPI import user01,user02
from config.case_content import epic, features
from tool.SwapTools import SwapTool
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][3])
@allure.tag('Script owner : 张广南', 'Case owner : 封泰')
class TestCoinswapTrackOrder_005:
    ids = ["TestCoinswapTrackOrder_005",
           ]
    params = [
        {
            "case_name": "跟踪委托单-买入开多-委托单因资金不足委托失败测试",
            "direction": "buy",
            "ratio":0.95,
            "order_price_type": "formula_price",
            "trade_type":1
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
            user01.swap_track_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：下跟踪委托单'):
            active_price = round(self.latest_price*params['ratio'],2)
            track_order = user01.swap_track_order(contract_code=self.contract_code, volume=1, offset='open',
                                                  lever_rate=5, callback_rate=0.01,
                                                  active_price=active_price,
                                                  order_price_type=params['order_price_type'],
                                                  direction=params['direction'])
            order_id = track_order['data']['order_id_str']
            time.sleep(1)#等待数据刷新入库
            pass
        with allure.step('操作：成交操作刷新最新价，使跟踪委托单激活'):
            user02.swap_order(contract_code=self.contract_code,price=active_price,direction='buy')
            user02.swap_order(contract_code=self.contract_code,price=active_price,direction='sell')
            pass
        with allure.step("操作：通过母子划转将钱划到子账号，致使金额不足"):
            pass
        with allure.step("操作：使委托下单"):
            pass
        with allure.step("验证：因金额不足委托失败"):
            pass


if __name__ == '__main__':
    pytest.main()
