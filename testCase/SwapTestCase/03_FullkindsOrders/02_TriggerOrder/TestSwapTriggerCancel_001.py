#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211104
# @Author : HuiQing Yu


import allure
import pytest
import time
from common.SwapServiceAPI import user01
from tool.atp import ATP
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('撤销委托')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCancel_001:

    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->计划委托下单'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            trigger_price = round(cls.currentPrice, 2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= cls.currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            cls.orderInfo = user01.swap_trigger_order(contract_code=cls.contract_code, trigger_price=trigger_price,
                                                       trigger_type=trigger_type,
                                                       order_price=trigger_price, direction='buy', volume=1)
            pass

    def test_execute(self, contract_code):
        with allure.step('*->指定计划委托订单撤单'):
            cancelResult = user01.swap_trigger_cancel(contract_code=contract_code,order_id=self.orderInfo['data']['order_id'])
            pass
        with allure.step('验证撤单订单结果返回'):
            assert cancelResult['status'] == 'ok' and str(self.orderInfo['data']['order_id']) == cancelResult['data']['successes']
            pass



if __name__ == '__main__':
    pytest.main()
