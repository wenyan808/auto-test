#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211103
# @Author : HuiQing Yu

from common.SwapServiceAPI import user01
import pytest
import allure
import time
from tool.atp import ATP
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features

@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerOpenBuy10_004:
    ids = [ "TestSwapTriggerOpenBuy5_004",
            "TestSwapTriggerOpenBuy5_005",
            "TestSwapTriggerOpenBuy5_006",
            "TestSwapTriggerOpenSell5_004",
            "TestSwapTriggerOpenSell5_005",
            "TestSwapTriggerOpenSell5_006",
            "TestSwapTriggerOpenBuy10_004",
            "TestSwapTriggerOpenBuy10_005",
            "TestSwapTriggerOpenBuy10_006",
            "TestSwapTriggerOpenSell10_004",
            "TestSwapTriggerOpenSell10_005",
            "TestSwapTriggerOpenSell10_006",
            "TestSwapTriggerOpenBuy20_004",
            "TestSwapTriggerOpenBuy20_005",
            "TestSwapTriggerOpenBuy20_006",
            "TestSwapTriggerOpenSell20_004",
            "TestSwapTriggerOpenSell20_005",
            "TestSwapTriggerOpenSell20_006"
            ]
    params = [
              {
                "caseName": "开多-计划委托-最优5档触发价大于最新价",
                "order_price_type": "optimal_5",
                "direction":"buy",
                "trigger_price_ratio": 1.01
              },{
                "caseName": "开多-计划委托-最优5档触发价大于最新价",
                "order_price_type": "optimal_5",
                "direction": "buy",
                "trigger_price_ratio": 0.99
              },{
                "caseName": "开多-计划委托-最优5档触发价大于最新价",
                "order_price_type": "optimal_5",
                "direction": "buy",
                "trigger_price_ratio": 1.00
              },{
                "caseName": "开空-计划委托-最优5档触发价大于最新价",
                "order_price_type": "optimal_5",
                "direction": "sell",
                "trigger_price_ratio": 1.01
              }, {
                "caseName": "开空-计划委托-最优5档触发价大于最新价",
                "order_price_type": "optimal_5",
                "direction": "sell",
                "trigger_price_ratio": 0.99
              }, {
                "caseName": "开空-计划委托-最优5档触发价大于最新价",
                "order_price_type": "optimal_5",
                "direction": "sell",
                "trigger_price_ratio": 1.00
              },{
                "caseName": "开多-计划委托-最优10档触发价大于最新价",
                "order_price_type": "optimal_10",
                "direction":"buy",
                "trigger_price_ratio": 1.01
              },{
                "caseName": "开多-计划委托-最优10档触发价小于最新价",
                "order_price_type": "optimal_10",
                "direction": "buy",
                "trigger_price_ratio": 0.99
              },{
                "caseName": "开多-计划委托-最优10档触发价大于最新价",
                "order_price_type": "optimal_10",
                "direction": "buy",
                "trigger_price_ratio": 1.00
              },{
                "caseName": "开空-计划委托-最优10档触发价大于最新价",
                "order_price_type": "optimal_10",
                "direction": "sell",
                "trigger_price_ratio": 1.01
              }, {
                "caseName": "开空-计划委托-最优10档触发价小于最新价",
                "order_price_type": "optimal_10",
                "direction": "sell",
                "trigger_price_ratio": 0.99
              }, {
                "caseName": "开空-计划委托-最优10档触发价大于最新价",
                "order_price_type": "optimal_10",
                "direction": "sell",
                "trigger_price_ratio": 1.00
              },{
                "caseName": "开多-计划委托-最优20档触发价大于最新价",
                "order_price_type": "optimal_20",
                "direction":"buy",
                "trigger_price_ratio": 1.01
              },{
                "caseName": "开多-计划委托-最优20档触发价大于最新价",
                "order_price_type": "optimal_20",
                "direction": "buy",
                "trigger_price_ratio": 0.99
              },{
                "caseName": "开多-计划委托-最优20档触发价大于最新价",
                "order_price_type": "optimal_20",
                "direction": "buy",
                "trigger_price_ratio": 1.00
              },{
                "caseName": "开空-计划委托-最优20档触发价大于最新价",
                "order_price_type": "optimal_20",
                "direction": "sell",
                "trigger_price_ratio": 1.01
              }, {
                "caseName": "开空-计划委托-最优20档触发价大于最新价",
                "order_price_type": "optimal_20",
                "direction": "sell",
                "trigger_price_ratio": 0.99
              }, {
                "caseName": "开空-计划委托-最优20档触发价大于最新价",
                "order_price_type": "optimal_20",
                "direction": "sell",
                "trigger_price_ratio": 1.00
              }
            ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->持仓'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消委托'):
            time.sleep(1)
            user01.swap_trigger_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*->'+params['caseName']):
            trigger_price = round(self.currentPrice * params['trigger_price_ratio'], 2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= self.currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code,trigger_price=trigger_price,
                                                       trigger_type=trigger_type,offset='open',
                                                       order_price=self.currentPrice,direction=params['direction'],
                                                       volume=1,order_price_type=params['order_price_type'])
            pass
        with allure.step('*->验证'+params['caseName']+'返回，orderId不为空'):
            assert 'ok' in self.orderInfo['status']
            assert self.orderInfo['data']['order_id'] is not None
            pass


if __name__ == '__main__':
    pytest.main()
