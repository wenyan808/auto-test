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
@allure.story('购买量超过后台限制')
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCloseBuy10_008:
    ids = [ "TestSwapTriggerCloseBuy5_008",
            "TestSwapTriggerCloseSell5_008",
            "TestSwapTriggerCloseBuy10_008",
            "TestSwapTriggerCloseSell10_008",
            "TestSwapTriggerCloseBuy20_008",
            "TestSwapTriggerCloseSell20_008"
            ]
    params = [
              {
                "caseName": "平空-计划委托-最优5档-购买量超过后台限制",
                "order_price_type": "optimal_5",
                "direction":"buy",
              },{
                "caseName": "平多-计划委托-最优5档-购买量超过后台限制",
                "order_price_type": "optimal_5",
                "direction":"sell",
              },{
                "caseName": "平空-计划委托-最优10档-购买量超过后台限制",
                "order_price_type": "optimal_10",
                "direction":"buy",
              },{
                "caseName": "平多-计划委托-最优10档-购买量超过后台限制",
                "order_price_type": "optimal_10",
                "direction":"sell",
              },{
                "caseName": "平空-计划委托-最优20档-购买量超过后台限制",
                "order_price_type": "optimal_20",
                "direction":"buy",
              },{
                "caseName": "平多-计划委托-最优20档-购买量超过后台限制",
                "order_price_type": "optimal_20",
                "direction":"sell",
              }
            ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->获取最新价'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            cls.volume_limit = 4000
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*->'+params['caseName']):
            trigger_price = round(self.currentPrice , 2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= self.currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code, trigger_price=trigger_price,
                                                       trigger_type=trigger_type,
                                                       order_price=self.currentPrice, direction=params['direction'],
                                                       volume=int(self.volume_limit+1), order_price_type=params['order_price_type'])
            pass
        with allure.step('*->验证'+params['caseName']+'返回:报错:volume字段不能为空,请重新输入'):
            assert 'error' in self.orderInfo['status']
            assert '下单数量超出限制' in self.orderInfo['err_msg']
            pass


if __name__ == '__main__':
    pytest.main()
