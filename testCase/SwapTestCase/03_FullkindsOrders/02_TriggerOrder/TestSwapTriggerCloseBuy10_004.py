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
class TestSwapTriggerCloseBuy10_004:
    ids = [
        "TestSwapTriggerCloseSell5_004",
        "TestSwapTriggerCloseSell5_005",
        "TestSwapTriggerCloseSell5_006",
        "TestSwapTriggerCloseBuy5_004",
        "TestSwapTriggerCloseBuy5_005",
        "TestSwapTriggerCloseBuy5_006",
        "TestSwapTriggerCloseSell10_004",
        "TestSwapTriggerCloseSell10_005",
        "TestSwapTriggerCloseSell10_006",
        "TestSwapTriggerCloseBuy10_004",
        "TestSwapTriggerCloseBuy10_005",
        "TestSwapTriggerCloseBuy10_006",
        "TestSwapTriggerCloseSell20_004",
        "TestSwapTriggerCloseSell20_005",
        "TestSwapTriggerCloseSell20_006",
        "TestSwapTriggerCloseBuy20_004",
        "TestSwapTriggerCloseBuy20_005",
        "TestSwapTriggerCloseBuy20_006"
    ]
    params = [
        {
            "caseName": "平多-计划委托-最优5档触发价大于最新价",
            "order_price_type": "optimal_5",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        }, {
            "caseName": "平多-计划委托-最优5档触发价大于最新价",
            "order_price_type": "optimal_5",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        }, {
            "caseName": "平多-计划委托-最优5档触发价大于最新价",
            "order_price_type": "optimal_5",
            "direction": "sell",
            "trigger_price_ratio": 1.00
        }, {
            "caseName": "平空-计划委托-最优5档触发价大于最新价",
            "order_price_type": "optimal_5",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        }, {
            "caseName": "平空-计划委托-最优5档触发价大于最新价",
            "order_price_type": "optimal_5",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        }, {
            "caseName": "平空-计划委托-最优5档触发价大于最新价",
            "order_price_type": "optimal_5",
            "direction": "buy",
            "trigger_price_ratio": 1.00
        }, {
            "caseName": "平多-计划委托-最优10档触发价大于最新价",
            "order_price_type": "optimal_10",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        }, {
            "caseName": "平多-计划委托-最优10档触发价小于最新价",
            "order_price_type": "optimal_10",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        }, {
            "caseName": "平多-计划委托-最优10档触发价大于最新价",
            "order_price_type": "optimal_10",
            "direction": "sell",
            "trigger_price_ratio": 1.00
        }, {
            "caseName": "平空-计划委托-最优10档触发价大于最新价",
            "order_price_type": "optimal_10",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        }, {
            "caseName": "平空-计划委托-最优10档触发价小于最新价",
            "order_price_type": "optimal_10",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        }, {
            "caseName": "平空-计划委托-最优10档触发价大于最新价",
            "order_price_type": "optimal_10",
            "direction": "buy",
            "trigger_price_ratio": 1.00
        }, {
            "caseName": "平多-计划委托-最优20档触发价大于最新价",
            "order_price_type": "optimal_20",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        }, {
            "caseName": "平多-计划委托-最优20档触发价大于最新价",
            "order_price_type": "optimal_20",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        }, {
            "caseName": "平多-计划委托-最优20档触发价大于最新价",
            "order_price_type": "optimal_20",
            "direction": "sell",
            "trigger_price_ratio": 1.00
        }, {
            "caseName": "平空-计划委托-最优20档触发价大于最新价",
            "order_price_type": "optimal_20",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        }, {
            "caseName": "平空-计划委托-最优20档触发价大于最新价",
            "order_price_type": "optimal_20",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        }, {
            "caseName": "平空-计划委托-最优20档触发价大于最新价",
            "order_price_type": "optimal_20",
            "direction": "buy",
            "trigger_price_ratio": 1.00
        }
    ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->持仓'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            user01.swap_order(contract_code=cls.contract_code,price=cls.currentPrice,direction='buy',volume=20)
            user01.swap_order(contract_code=cls.contract_code,price=cls.currentPrice,direction='sell',volume=20)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消委托'):
            time.sleep(1)
            user01.swap_cancelall(contract_code=cls.contract_code)
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
                                                       trigger_type=trigger_type,offset='close',
                                                       order_price=self.currentPrice,direction=params['direction'],
                                                       volume=1,order_price_type=params['order_price_type'])
            pass
        with allure.step('*->验证'+params['caseName']+'返回，orderId不为空'):
            assert 'ok' in self.orderInfo['status']
            assert self.orderInfo['data']['order_id'] is not None
            pass


if __name__ == '__main__':
    pytest.main()
