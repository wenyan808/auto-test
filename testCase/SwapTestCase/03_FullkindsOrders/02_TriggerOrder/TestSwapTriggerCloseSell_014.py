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
@allure.story('止盈止损单')
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCloseSell_014:
    ids = [ "TestSwapTriggerCloseSell_014",
            "TestSwapTriggerCloseSell_015",
            "TestSwapTriggerCloseSell_016",
            "TestSwapTriggerCloseSell_017",
            "TestSwapTriggerCloseSell_021",
            "TestSwapTriggerCloseSell_022",
            "TestSwapTriggerCloseSell_023",
            "TestSwapTriggerCloseSell_024",
            "TestSwapTriggerCloseBuy_014",
            "TestSwapTriggerCloseBuy_015",
            "TestSwapTriggerCloseBuy_016",
            "TestSwapTriggerCloseBuy_017",
            "TestSwapTriggerCloseBuy_021",
            "TestSwapTriggerCloseBuy_022",
            "TestSwapTriggerCloseBuy_023",
            "TestSwapTriggerCloseBuy_024"
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
        currentPrice = ATP.get_current_price()  # 最新价
        user01.swap_order(contract_code=cls.contract_code, price=currentPrice, direction='buy')
        user01.swap_order(contract_code=cls.contract_code, price=currentPrice, direction='sell')

    @classmethod
    def teardown_class(cls):
        time.sleep(1)
        user01.swap_trigger_cancelall(contract_code=cls.contract_code)

    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('1、持仓'):
            currentPrice = ATP.get_current_price()  # 最新价
            pass
        with allure.step('2、'+params['caseName']):
            trigger_price = round(currentPrice*params['trigger_price_ratio'],2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code,trigger_price=trigger_price,trigger_type=trigger_type,
                                        order_price=trigger_price,direction=params['direction'],offset='close',volume=1,
                                        order_price_type=params['order_price_type'])
            pass
        with allure.step('3、验证计划委托止盈下单成功'):
            assert self.orderInfo['data']['order_id']
            pass
        with allure.step('4、取消委托，恢复环境'):
            pass


if __name__ == '__main__':
    pytest.main()
