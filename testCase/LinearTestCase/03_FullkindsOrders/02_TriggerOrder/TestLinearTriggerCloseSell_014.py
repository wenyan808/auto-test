#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211103
# @Author : YuHuiQing

from common.LinearServiceAPI import user01
import pytest
import allure
import time
from tool.atp import ATP
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('正向永续')
@allure.feature('计划委托')
@allure.story('止盈止损单')
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestLinearTriggerCloseSell_014:
    ids = ["TestLinearTriggerCloseSell_014",
           "TestLinearTriggerCloseSell_015",
           "TestLinearTriggerCloseSell_016",
           "TestLinearTriggerCloseSell_017",
           "TestLinearTriggerCloseSell_021",
           "TestLinearTriggerCloseSell_022",
           "TestLinearTriggerCloseSell_023",
           "TestLinearTriggerCloseSell_024",
           "TestLinearTriggerCloseBuy_014",
           "TestLinearTriggerCloseBuy_015",
           "TestLinearTriggerCloseBuy_016",
           "TestLinearTriggerCloseBuy_017",
           "TestLinearTriggerCloseBuy_021",
           "TestLinearTriggerCloseBuy_022",
           "TestLinearTriggerCloseBuy_023",
           "TestLinearTriggerCloseBuy_024"
           ]
    params = [
        {
            "caseName": "多仓-计划止盈单-限价",
            "order_price_type": "limit",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "多仓-计划止盈单-最优5档",
            "order_price_type": "optimal_5",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "多仓-计划止盈单-最优10档",
            "order_price_type": "optimal_10",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "多仓-计划止盈单-最优20档",
            "order_price_type": "optimal_20",
            "direction": "sell",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "多仓-计划止损单-限价",
            "order_price_type": "limit",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "多仓-计划止损单-最优5档",
            "order_price_type": "optimal_5",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "多仓-计划止损单-最优10档",
            "order_price_type": "optimal_10",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "多仓-计划止损单-最优20档",
            "order_price_type": "optimal_20",
            "direction": "sell",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "空仓-计划止盈单-限价",
            "order_price_type": "limit",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "空仓-计划止盈单-最优5档",
            "order_price_type": "optimal_5",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "空仓-计划止盈单-最优10档",
            "order_price_type": "optimal_10",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "空仓-计划止盈单-最优20档",
            "order_price_type": "optimal_20",
            "direction": "buy",
            "trigger_price_ratio": 0.99
        },
        {
            "caseName": "空仓-计划止损单-限价",
            "order_price_type": "limit",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "空仓-计划止损单-最优5档",
            "order_price_type": "optimal_5",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "空仓-计划止损单-最优10档",
            "order_price_type": "optimal_10",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        },
        {
            "caseName": "空仓-计划止损单-最优20档",
            "order_price_type": "optimal_20",
            "direction": "buy",
            "trigger_price_ratio": 1.01
        }
    ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->持仓'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            user01.linear_order(contract_code=cls.contract_code, price=cls.currentPrice, direction='buy')
            user01.linear_order(contract_code=cls.contract_code, price=cls.currentPrice, direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消委托'):
            time.sleep(1)
            user01.linear_trigger_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code, params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*->' + params['caseName']):
            trigger_price = round(self.currentPrice * params['trigger_price_ratio'], 2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= self.currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            self.orderInfo = user01.linear_trigger_order(contract_code=contract_code, trigger_price=trigger_price,
                                                         trigger_type=trigger_type,
                                                         order_price=trigger_price, direction=params['direction'],
                                                         offset='close', volume=1,
                                                         order_price_type=params['order_price_type'])
            pass
        with allure.step('*->验证' + params['caseName'] + '下单成功'):
            assert self.orderInfo['data']['order_id']
            pass


if __name__ == '__main__':
    pytest.main()
