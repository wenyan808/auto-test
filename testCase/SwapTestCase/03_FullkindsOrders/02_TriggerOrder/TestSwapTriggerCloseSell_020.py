#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211103
# @Author : HuiQing Yu

import allure
import pytest

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCloseSell_020:
    ids = [ "TestSwapTriggerCloseSell_020",
            "TestSwapTriggerCloseSell_027",
            "TestSwapTriggerCloseBuy_020",
            "TestSwapTriggerCloseBuy_027"
            ]
    params = [
              {
                "caseName": "多仓-计划止盈单-不输入卖出量",
                "direction": "sell",
                "trigger_type":"ge"
              },
              {
                "caseName": "多仓-计划止损单-不输入卖出量",
                "direction": "sell",
                "trigger_type":"le"
              },
              {
                "caseName": "空仓-计划止盈单-不输入买入量",
                "direction": "buy",
                "trigger_type":"le"
              },
              {
                "caseName": "空仓-计划止损单-不输入买入量",
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

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, contract_code,params):
        allure.dynamic.title(params['caseName'])
        with allure.step('*->'+params['caseName']):
            self.orderInfo = user01.swap_trigger_order(contract_code=contract_code,trigger_price=self.currentPrice,
                                                       trigger_type=params['trigger_type'],order_price=self.currentPrice,
                                                       direction=params['direction'],offset='close',volume=None)
            pass
        with allure.step('*->验证'+params['caseName']+'下单返回，下单失败；参数有校验：volume字段不能为空'):
            assert 'volume字段不能为空' in self.orderInfo['err_msg']
            pass

if __name__ == '__main__':
    pytest.main()
