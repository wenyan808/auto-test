#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211103
# @Author : YuHuiQing

from common.SwapServiceAPI import user01
import pytest
import allure
import time
from tool.atp import ATP
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')
@allure.feature('计划委托')
@allure.story('不输入触发价')
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
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->获取最新价'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*->'+params['caseName']):
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code,trigger_price=None,
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
