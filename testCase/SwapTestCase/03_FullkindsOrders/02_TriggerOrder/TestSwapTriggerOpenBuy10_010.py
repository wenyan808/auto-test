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
@allure.story('下单后切换杠杆')
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerOpenBuy10_010:
    ids = [ "TestSwapTriggerOpenBuy5_010",
            "TestSwapTriggerOpenSell5_010",
            "TestSwapTriggerOpenBuy10_010",
            "TestSwapTriggerOpenSell10_010",
            "TestSwapTriggerOpenBuy20_010",
            "TestSwapTriggerOpenSell20_010"
            ]
    params = [
              {
                "caseName": "开多-计划委托-最优5档-下单后切换杠杆",
                "order_price_type": "optimal_5",
                "direction":"buy",
              },{
                "caseName": "开空-计划委托-最优5档-下单后切换杠杆",
                "order_price_type": "optimal_5",
                "direction":"sell",
              },{
                "caseName": "开多-计划委托-最优10档-下单后切换杠杆",
                "order_price_type": "optimal_10",
                "direction":"buy",
              },{
                "caseName": "开空-计划委托-最优10档-下单后切换杠杆",
                "order_price_type": "optimal_10",
                "direction":"sell",
              },{
                "caseName": "开多-计划委托-最优20档-下单后切换杠杆",
                "order_price_type": "optimal_20",
                "direction":"buy",
              },{
                "caseName": "开空-计划委托-最优20档-下单后切换杠杆",
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

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消委托'):
            time.sleep(1)
            user01.swap_trigger_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*-> 取消所有挂单'):
            user01.swap_trigger_cancelall(contract_code=self.contract_code)
            user01.swap_cancelall(contract_code=self.contract_code)
            pass
        with allure.step('*->'+params['caseName']):
            trigger_price = round(self.currentPrice , 2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= self.currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code, trigger_price=trigger_price,
                                                       trigger_type=trigger_type,volume=1,
                                                       order_price=self.currentPrice, direction=params['direction'],
                                                        order_price_type=params['order_price_type'])
            pass
        with allure.step('*->验证 '+params['caseName']+'返回，下单正确'):
            assert 'ok' in self.orderInfo['status']
            pass
        with allure.step('*->切换杠杆 '+params['caseName']+' 执行切换'):
            self.switch_lever_result = user01.swap_switch_lever_rate(contract_code=contract_code, lever_rate=10)
            pass
        with allure.step('*->验证切换结果 '+params['caseName']+''):
            assert 'error' in self.switch_lever_result['status']
            assert '当前有挂单,无法切换倍数' or '访问次数超出限制' in self.switch_lever_result['err_msg']
            pass

if __name__ == '__main__':
    pytest.main()