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
                "trigger_type":"ge"
              },
              {
                "caseName": "空仓-计划止盈单-不输入买入价",
                "direction": "buy",
                "trigger_type":"ge"
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
        with allure.step('*->持仓'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=cls.currentPrice, direction='buy')
            user01.swap_order(contract_code=cls.contract_code, price=cls.currentPrice, direction='sell')
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step(params['caseName']):
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code,trigger_price=round(self.currentPrice*1.01,2),trigger_type=params['trigger_type'],
                                        direction=params['direction'],offset='close',volume=1)
            pass
        with allure.step('验证:返回结果提示异常err_msg=价格不合理'):
            assert '价格不合理' in self.orderInfo['err_msg']
            pass


if __name__ == '__main__':
    pytest.main()
