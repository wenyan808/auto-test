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

    @classmethod
    def setup_class(cls):
        with allure.step('*->持仓'):
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            cls.contract_code = DEFAULT_CONTRACT_CODE
            user01.swap_order(contract_code=cls.contract_code, price=cls.currentPrice, direction='buy')
            user01.swap_order(contract_code=cls.contract_code, price=cls.currentPrice, direction='sell')
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['caseName'])
        with allure.step(params['caseName']):
            self.orderInfo = user01.swap_trigger_order(contract_code=self.contract_code,trigger_price=round(self.currentPrice*1.01,2),trigger_type=params['trigger_type'],
                                        direction=params['direction'],offset='close',volume=1)
            pass
        with allure.step('验证:返回结果提示异常err_msg=价格不合理'):
            assert '价格不合理' in self.orderInfo['err_msg']
            pass


if __name__ == '__main__':
    pytest.main()
