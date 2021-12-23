#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 余辉青


import allure
import pytest
import time

from common.SwapServiceAPI import user01, user02
from common.redisComm import redisConf
from config.case_content import epic, features
from tool.SwapTools import SwapTool
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][1])
@allure.tag('Script owner : 陈维', 'Case owner : 吉龙')
class TestCoinswapLimitOrder_003:
    ids = [
        "TestCoinswapLimitOrder_003",
        "TestCoinswapLimitOrder_004",
    ]
    params = [
        {
            "case_name": "只做maker 买入开多下单后自动撤单测试",
            "ratio":1.01,
            "order_price_type":"post_only",
            "direction": "buy"
        },
        {
            "case_name": "只做maker 卖出开空下单后自动撤单测试",
            "ratio": 0.99,
            "order_price_type": "post_only",
            "direction": "sell"
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.latest_price = SwapTool.currentPrice()
            cls.redisClient = redisConf('redis6380').instance()
            pass
            with allure.step("挂盘"):
                user02.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 0.98, 2),
                                  direction='buy')
                user02.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price * 1.02, 2),
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
        with allure.step('业务：maker单，下单后如果不能马上成交，因为是maker所以订单会自动撤销'):
            pass
        with allure.step('操作：下单'):
            orderId = \
            user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price * params['ratio'], 2),
                              order_price_type=params['order_price_type'],
                              direction=params['direction'])['data']['order_id']
            pass
        with allure.step('操作：获取订单数据库信息'):
            for i in range(3):
                name = f'RsT:APO:11538483#{self.symbol}'
                key = f'Order:#{orderId}#1'
                redisInfo = self.redisClient.hmget(name=name, keys=key)
                redisInfo = str(redisInfo).split(',')
                if redisInfo[22] ==7:
                    break
                else:
                    print(redisInfo)
                    time.sleep(1)
            pass
        with  allure.step('验证：maker订单被取消'):
            assert redisInfo[22] == 7
            pass
        with  allure.step('验证：无资产冻结'):
            account_info = user01.swap_account_info(contract_code=self.contract_code)
            for data in account_info['data']:
                assert data['margin_frozen'] == 0E-18
            pass


if __name__ == '__main__':
    pytest.main()
