#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211103
# @Author : HuiQing Yu

import allure
import pytest

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCloseBuy10_007:
    ids = [ "TestSwapTriggerCloseBuy5_007",
            "TestSwapTriggerCloseSell5_007",
            "TestSwapTriggerCloseBuy10_007",
            "TestSwapTriggerCloseSell10_007",
            "TestSwapTriggerCloseBuy20_007",
            "TestSwapTriggerCloseSell20_007"
            ]
    params = [
              {
                "caseName": "平空-计划委托-最优5档-不输入触发价",
                "order_price_type": "optimal_5",
                "direction":"buy",
              },{
                "caseName": "平多-计划委托-最优5档-不输入触发价",
                "order_price_type": "optimal_5",
                "direction":"sell",
              },{
                "caseName": "平空-计划委托-最优10档-不输入触发价",
                "order_price_type": "optimal_10",
                "direction":"buy",
              },{
                "caseName": "平多-计划委托-最优10档-不输入触发价",
                "order_price_type": "optimal_10",
                "direction":"sell",
              },{
                "caseName": "平空-计划委托-最优20档-不输入触发价",
                "order_price_type": "optimal_20",
                "direction":"buy",
              },{
                "caseName": "平多-计划委托-最优20档-不输入触发价",
                "order_price_type": "optimal_20",
                "direction":"sell",
              }
            ]


    @classmethod
    def setup_class(cls):
        with allure.step('*->获取最新价'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*->'+params['caseName']):
            self.orderInfo = user01.swap_trigger_order(contract_code=self.contract_code,trigger_price=None,
                                                       trigger_type='ge',offset='close',
                                                       order_price=self.currentPrice,direction=params['direction'],
                                                       volume=1,order_price_type=params['order_price_type'])
            pass
        with allure.step('*->验证'+params['caseName']+'返回:报错:triggerPrice字段不能为空,请重新输入'):
            assert 'error' in self.orderInfo['status']
            assert 'triggerPrice字段不能为空,请重新输入' in self.orderInfo['err_msg']
            pass


if __name__ == '__main__':
    pytest.main()
