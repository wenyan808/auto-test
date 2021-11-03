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
class TestSwapTriggerCloseSell_019:
    ids = [ "TestSwapTriggerCloseSell_019",
            "TestSwapTriggerCloseSell_026",
            "TestSwapTriggerCloseBuy_019",
            "TestSwapTriggerCloseBuy_026"
            ]
    params = [
              {
                "caseName": "多仓-计划止盈单-不输入卖出价",
                "direction": "sell",
                "trigger_type":"ge"
              },
              {
                "caseName": "多仓-计划止损单-不输入卖出价",
                "direction": "sell",
                "trigger_type":"le"
              },
              {
                "caseName": "空仓-计划止盈单-不输入买入价",
                "direction": "buy",
                "trigger_type":"le"
              },
              {
                "caseName": "空仓-计划止损单-不输入买入价",
                "direction": "buy",
                "trigger_type":"ge"
              }
            ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        currentPrice = ATP.get_current_price()  # 最新价
        user01.swap_order(contract_code=cls.contract_code, price=currentPrice, direction='buy')
        user01.swap_order(contract_code=cls.contract_code, price=currentPrice, direction='sell')

    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('1、持仓'):
            currentPrice = ATP.get_current_price()  # 最新价
            pass
        with allure.step('2、'+params['caseName']):
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code,trigger_price=currentPrice,trigger_type=params['trigger_type'],
                                        order_price=None,direction=params['direction'],offset='close',volume=1)
            pass
        with allure.step('3、验证计划委托止盈下单返回，参数有校验：系统异常'):
            assert '系统异常' in self.orderInfo['err_msg']
            pass
        with allure.step('4、取消委托，恢复环境'):
            pass

if __name__ == '__main__':
    pytest.main()
